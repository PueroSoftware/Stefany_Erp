# sync_r2 — Pipeline: assets → WebP → Cloudflare R2 → tabla objectstorage
import hashlib
import mimetypes
import os
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from core.models import ObjectStorage

# -- Rutas base -----------------------------------------------------------------
# parents[3] desde este archivo = backend/. Derivamos todo desde ahí (una sola vez).
BASE_BACKEND = Path(__file__).resolve().parents[3]
# Assets del frontend: SOLO LECTURA (raiz_proyecto/frontend/src/assets)
ASSETS_DIR = BASE_BACKEND.parent / "frontend" / "src" / "assets"
# Espejo local WebP que crea el pipeline: backend/media_webp/
MEDIA_WEBP = BASE_BACKEND / "media_webp"

# Clasificación de extensiones: qué hacer con cada tipo de archivo
CONVERTIR = {".png", ".jpg", ".jpeg"}  # Fase A: transformar a WebP
SUBIR_TAL_CUAL = {".svg", ".webp"}  # ya son formatos web
IGNORAR = {".eps"}  # formato vectorial de imprenta

# MIME correctos para Content-Type en R2 (buenas prácticas de caché/navegador)
MIME_EXTRA = {".webp": "image/webp", ".svg": "image/svg+xml"}


class Command(BaseCommand):
    help = "Imágenes de frontend/src/assets -> WebP -> Cloudflare R2 -> objectstorage"

    def add_arguments(self, parser):
        # --dry-run: valida y lista lo que haría, sin tocar disco/red/BD.
        # Siempre se ejecuta PRIMERO en seco: regla de oro de scripts destructivos/costosos.
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simula todo el pipeline sin escribir nada",
        )
        # --grupo: filtra por carpeta (nombre legible original, ej: 'img de jabones sin fondo')
        parser.add_argument(
            "--grupo",
            type=str,
            default=None,
            help="Procesa solo una carpeta de assets (ej: sliders)",
        )

    def handle(self, *args, **options):
        # Registro de claves R2 ya asignadas en esta ejecución (detección de colisiones)
        self._claves_vistas = set()
        self.dry_run = options["dry_run"]
        self.grupo_filtro = options["grupo"]

        # --- Validación temprana (fail fast): si falta una credencial,
        # mejor abortar ANTES de haber convertido 160 imágenes en vano ---
        faltantes = [
            v
            for v in (
                "R2_ENDPOINT",
                "R2_ACCESS_KEY_ID",
                "R2_SECRET_ACCESS_KEY",
                "R2_BUCKET",
                "R2_PUBLIC_BASE_URL",
            )
            if not os.environ.get(v)
        ]
        if faltantes:
            raise CommandError(f"Faltan variables en .env: {faltantes}")

        if not ASSETS_DIR.exists():
            raise CommandError(f"No existe la carpeta de assets: {ASSETS_DIR}")

        # Recolecta: agrupa archivos por carpeta (cada carpeta = un "grupo" lógico)
        carpetas = {}  # {Path carpeta: [Path archivos...]}
        for ruta in sorted(ASSETS_DIR.rglob("*")):
            if ruta.is_file():
                carpetas.setdefault(ruta.parent, []).append(ruta)

        total_convertidos = total_subidos = total_registrados = 0
        for carpeta in sorted(carpetas):
            archivos = carpetas[carpeta]
            # grupo legible: nombre ORIGINAL de la subcarpeta relativa a assets
            # ('img de jabones sin fondo'), mientras la clave R2 usa slug limpio.
            rel = carpeta.relative_to(ASSETS_DIR)
            grupo_legible = str(rel) if str(rel) != "." else ""

            if self.grupo_filtro and grupo_legible != self.grupo_filtro:
                continue

            self.stdout.write(
                self.style.MIGRATE_HEADING(
                    f"\n=== Grupo: '{grupo_legible or '(raíz)'}' ({len(archivos)} archivos) ==="
                )
            )

            # 'orden' = índice alfabético dentro de su carpeta/grupo
            for orden, origen in enumerate(sorted(archivos)):
                resultado = self._procesar_archivo(origen, grupo_legible, orden)
                if resultado:
                    conv, sub, reg = resultado
                    total_convertidos += conv
                    total_subidos += sub
                    total_registrados += reg

        self.stdout.write(
            self.style.SUCCESS(
                f"\nRESUMEN -> convertidos: {total_convertidos} | "
                f"subidos a R2: {total_subidos} | registrados en BD: {total_registrados}"
                + ("  [DRY-RUN: nada fue escrito]" if self.dry_run else "")
            )
        )

    # ------------------------------------------------------------------ #
    def _procesar_archivo(self, origen, grupo, orden):
        """Pipeline completo para UN archivo. Devuelve (conv, sub, reg)."""
        ext = origen.suffix.lower()

        if ext in IGNORAR:
            self.stdout.write(f"  OMITIDO (eps): {origen.name}")
            return None

        # Clave R2: ruta espejo con nombres slugged -> URLs seguras e idempotentes
        clave_r2 = self._clave_r2(origen)

        if self.dry_run:
            accion = "CONVERTIR+SUBIR" if ext in CONVERTIR else "SUBIR TAL CUAL"
            self.stdout.write(f"  [{accion}] {origen.name} -> {clave_r2}")
            return None

        # ---------- FASE A: conversión local ----------
        if ext in CONVERTIR:
            destino = MEDIA_WEBP / origen.relative_to(ASSETS_DIR).with_suffix(".webp")
            self._convertir_a_webp(origen, destino)
            fuente, tipo_contenido = destino, MIME_EXTRA[".webp"]
            convertido = 1
        else:
            fuente, tipo_contenido = (
                origen,
                (
                    MIME_EXTRA.get(ext)
                    or mimetypes.guess_type(origen.name)[0]
                    or "application/octet-stream"
                ),
            )
            convertido = 0

        # ---------- FASE B: subida a R2 ----------
        tamano = self._subir_a_r2(fuente, clave_r2, tipo_contenido)
        url_publica = f"{os.environ['R2_PUBLIC_BASE_URL'].rstrip('/')}/{clave_r2}"

        # ---------- FASE C: registro en BD (ORM, no SQL crudo) ----------
        # update_or_create sobre clave_r2 (unique) => re-ejecutar NO duplica.
        obj, creado = ObjectStorage.objects.update_or_create(
            clave_r2=clave_r2,
            defaults={
                "url_publica": url_publica,
                "grupo": grupo,
                "orden": orden,
                "tipo_contenido": tipo_contenido,
                "tamano_bytes": tamano,
                "activo": True,
            },
        )
        self.stdout.write(
            self.style.SUCCESS(f"  {'CREADO' if creado else 'ACTUALIZADO'}: {clave_r2}")
        )
        return (convertido, 1, 1)

    def _clave_r2(self, origen):
        """Slugifica cada tramo de la ruta: 'Qr's/pago.jpeg' -> 'qrs/pago.webp'.
        slugify elimina tildes, espacios y apóstrofes => claves URL-safe."""
        rel = origen.relative_to(ASSETS_DIR)
        partes = [slugify(p) for p in rel.parts[:-1]]
        ext_destino = (
            ".webp" if origen.suffix.lower() in CONVERTIR else rel.suffix.lower()
        )
        clave = "/".join(partes + [slugify(rel.stem) + ext_destino])
        # Colisión: archivos distintos pueden slugificar a la MISMA clave
        # (ej: 'X.jpeg' y 'X.png' -> ambos a 'x.webp'); el segundo PISARÍA al
        # primero en R2 (pérdida silenciosa). Sufijo determinista md5 del path
        # original: misma entrada => misma clave siempre => idempotente.
        if clave in self._claves_vistas:
            huella = hashlib.md5(str(rel).encode()).hexdigest()[:8]
            clave = "/".join(partes + [f"{slugify(rel.stem)}-{huella}{ext_destino}"])
        self._claves_vistas.add(clave)
        return clave

    def _convertir_a_webp(self, origen, destino):
        """PNG/JPG -> WebP. quality=80 equilibra peso/calidad visual;
        method=6 es el esfuerzo máximo de compresión (lento pero óptimo).
        WebP conserva transparencia RGBA sin trabajo extra."""
        from PIL import Image

        destino.parent.mkdir(parents=True, exist_ok=True)
        if destino.exists():  # idempotente: no reconvierte lo ya hecho
            return
        with Image.open(origen) as img:
            img.save(destino, "WEBP", quality=80, method=6)

    def _subir_a_r2(self, fuente, clave_r2, content_type):
        """Sube el binario a R2. boto3 cliente S3 apuntando al endpoint R2.
        Content-Type correcto => el navegador renderiza en vez de descargar."""
        import boto3

        cliente = boto3.client(
            "s3",
            endpoint_url=os.environ["R2_ENDPOINT"],
            aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        )
        datos = fuente.read_bytes()
        cliente.put_object(
            Bucket=os.environ["R2_BUCKET"],
            Key=clave_r2,
            Body=datos,
            ContentType=content_type,
        )
        return len(datos)
