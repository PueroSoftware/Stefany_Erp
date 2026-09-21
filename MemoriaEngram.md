# MemoriaEngram — Proyecto ERP TiendaSoap

> Documento generado a partir de la base de memoria **Engram** (`~/.engram/engram.db`) para el proyecto `erp_stefanny_django`.
> **Fecha de extracción:** 2026-08-25
> **Total de observaciones activas:** 24 · **Sesiones:** 1

---

## 📊 Resumen por tipo de memoria

| Tipo | Cantidad | Descripción |
|------|----------|-------------|
| `config` | 8 | Configuración del entorno, .env, MCP, catálogo de imágenes |
| `bugfix` | 5 | Correcciones de bugs (rutas, JWT, typos DRF, colisiones) |
| `architecture` | 4 | Modelos, backend completo, pipeline R2 |
| `decision` | 3 | Decisiones del usuario (esencias, SVG, layout frontend) |
| `session_summary` | 1 | Resumen completo de sesión |
| `pattern` | 1 | Ubicación de management commands |
| `learning` | 1 | Documento docente backend |
| `discovery` | 1 | Estado del backend |

---

## 🏗️ Estado del Proyecto

```
✅ Backend API Django (Fases 0-6 + Roles + Calidad A/B)
   → JWT, Inventario, Compras, Producción, Ventas
✅ Pipeline R2 (162 imágenes → Cloudflare CDN + tabla objectstorage)
🔨 Frontend React Native/Expo (Tienda Jabones) — EN CONSTRUCCIÓN
   → Fase 1 (App.tsx + ThemeProvider) en proceso
   → Pendientes: Fases 2-4 (API layer, componentes UI, pantalla Inicio)
```

---

## 📌 Observaciones detalladas

### Configuración y Arquitectura

#### [1387] architecture — Pipeline R2: imágenes→WebP→Cloudflare R2→objectstorage
- **What:** Convertir TODAS las imágenes de `frontend/src/assets/` (165 archivos: 72 PNG + 87 JPG/JPEG → WebP; 4 SVG + 1 WebP tal cual; 1 EPS omitido) y subir a Cloudflare R2, luego poblar tabla `objectstorage` vía ORM.
- **Where:**
  - `backend/core/management/commands/sync_r2.py` (management command fases A/B/C)
  - `backend/media_webp/` (espejo de assets en WebP)
  - `frontend/src/assets/` (SOLO LECTURA)
  - `backend/core/models.py:65` modelo ObjectStorage
- **Learned:**
  - R2 es API-compatible S3 → boto3 con `endpoint_url=R2_ENDPOINT`
  - Idempotencia: `update_or_create(clave_r2=...)` porque clave_r2 es unique
  - Flags: `--dry-run` y `--grupo=<carpeta>`
  - Pendiente futuro: borrado de objetos huérfanos en R2

#### [1394] config — Pipeline R2 COMPLETADO: 162 imágenes verificadas en 3 capas
- **What:** Las 162 imágenes están en las 3 capas. BD `objectstorage`: **162 filas** (raíz=3, esencia=21, Etiquetas=2, jabones sin fondo=40, marca=3, product=6, Qr's=3, sliders=84). Espejo `media_webp`: 157 webp. URLs reales responden HTTP 200. Peso total: **31.8 MB**, promedio 201 KB/imagen.
- **Learned:** Verificación por capas disco→red→BD + muestreo de URLs **desde la BD** es el método correcto. `banner.svg` pesa 6.5 MB (candidato a optimizar).

#### [1388] config — Pipeline R2: prerrequisitos completos (R2_PUBLIC_BASE_URL real)
- URL pública activada: `https://pub-8892b0ff54a14d2e91c70f633f3d6d6a.r2.dev`
- Las 6 variables `R2_*` en `backend/.env` con valores reales.
- El dominio `r2.dev` tiene rate-limiting; para producción se recomienda Custom Domain.

#### [1397] config — MCP config: -mcp-vision-gratuito, +context7 con API key
- Eliminado `mcp-vision-gratuito`, instalado **context7** en `~/.config/opencode/opencode.json`.
- Servidores finales: `engram`, `playwright-testing`, `context7`.
- ⚠ La config NO se recarga en caliente: hay que reiniciar opencode.

#### [1377] config — Frontend Tienda Jabones: Expo 52 env config
- Frontend React como Expo 52 + React Native + react-native-web + TypeScript.
- `frontend/package.json` (deps limpias) + `frontend/tsconfig.json`.

#### [1343] config — Config opencode MCP + OpenRouter
- Configuración de opencode con MCP servers y provider OpenRouter para modelos gratuitos.

#### [1328] config — AGENTS.md reglas agente full stack + modo plan
- Regla Oro (educar), Regla Plata (lógica), Regla Bronce (seguridad).
- Incluye flujo Request→URL→View→Serializer→Model→DB.

#### [1392] config — Catálogo imágenes final: 162 archivos, 0 colisiones
- Tras borrar 2 JPEG duplicados de Qr's, catálogo final = **162 archivos procesables**, 0 colisiones de clave_r2.

#### [1393] config — Pipeline R2 prueba marca OK: 3 imágenes en las 3 capas
- Prueba real con `--grupo=marca` exitosa en disco, R2 (HTTP 200 + image/webp), y BD (ids 1-3, orden alfabético 0/1/2).

---

### Bugs corregidos

#### [1390/1391] bugfix — Rutas sync_r2.py + colisiones md5
- **Bug 1:** `path.parents` off-by-one → `ASSETS_DIR` apuntaba a `StackWeb/` fuera del proyecto. Fix: `BASE_BACKEND = Path(__file__).resolve().parents[3]`.
- **Bug 2:** `.resolve` sin paréntesis → TypeError al importar.
- **Bug 3:** Colisión slugify: pares gemelos `'X.jpeg'+'X.png'` → misma clave webp. Fix: sufijo determinista `md5[:8]` del path original solo si hay colisión.
- **Aprendizaje:** `parents[3]` desde `commands/X.py` = backend/. `rglob()` sobre ruta inexistente NO falla (devuelve vacío silencioso).

#### [1372] bugfix — SimpleJWT USER_ID_FIELD + Zed venv_path
- `Usuario` usa `id_usuario` como PK y `correo` como `USERNAME_FIELD`, NO `id`.
- SimpleJWT por defecto lee `user.id` → corregir `USER_ID_FIELD` para firmar el token.

#### [1373] bugfix — Typos silenciosos DRF: REST__FRAMEWORK y permission_class
- `REST__FRAMEWORK` (doble guion) en settings → DRF ignoraba config → TODA request autenticada devolvía 401.
- `permission_class` (singular) vs `permission_classes`.

#### [1341] bugfix — BD recreada + migraciones OK + superusuario
- BD TiendaSoap recreada desde cero, migraciones aplicadas (33 tablas), superusuario creado.
- Login por **correo**: `admin@tiendasoap.com` (USERNAME_FIELD='correo').

---

### Decisiones del usuario

#### [1385] decision — Esencias: kaiaks fuera, 3 nuevas + tabla objectstorage
- Eliminados 2 aromas kaiak, añadidos 3 nuevos (carbon_activo, matico, lumbre).
- La "tabla de esencias" era CharField.choices hardcodeada (no existía como tabla).
- Creado modelo `ObjectStorage` para future R2 paths.

#### [1396] decision — SVG permanecen tal cual: materiales de imprenta
- Los 4 SVG (ids 5-8) se quedan COMO ESTÁN, sin optimizar ni limpiar.
- Son materiales de imprenta → vector puro, sin pérdida.
- Clasificación final: `CONVERTIR={png,jpg,jpeg}` | `SUBIR_TAL_CUAL={svg,webp}` | `IGNORAR={eps}`.

#### [1376] decision — Frontend: mantener solo el layout visual, limpiar el resto
- Conservar ÚNICAMENTE el diseño/layout visual del frontend, descartar el resto.
- Se conservaron carpetas `assets`, `src/tema`, `src/navegacion`.

---

### Patrones y aprendizajes

#### [1389] pattern — sync_r2.py ubicación: backend/core/management/commands/
- Los management commands de Django se registran por **convención de carpetas**: `backend/core/management/commands/sync_r2.py` + dos `__init__.py` vacíos.

#### [1375] learning — Documento ApuntesDocentes_Back.md
- Teoría del backend Django: flujo, ORM, "sin vacíos", serializers, viewsets/routers, permisos de rol, JWT, DRF/CORS.

#### [1374] discovery — Estado backend ERP TiendaSoap (completo)
- Backend completo (Fases 0-6 + Roles + A+B de calidad) y verificado.

#### [1342] architecture — Backend Fase 0+1+2 completada
- JWT, Inventario API, Compras API + stored procedure transaccional.

#### [1386] architecture — Catálogos aroma/presentacion/color: choices→FK + CRUD
- Reemplazados choices hardcodeadas con tablas catálogo (Aroma/Presentacion/Color).

#### [1327] architecture — Modelos Django completos y migraciones generadas
- TODOS los modelos completos, migraciones limpias en las 5 apps.

---

## 🔑 Credenciales y config clave

| Item | Valor |
|------|-------|
| BD PostgreSQL | `admin` / `admin123` @ localhost `TiendaSoap` |
| Superusuario admin login | `admin@tiendasoap.com` (por correo) |
| Bucket R2 | `stefanny-soap` |
| R2 Public Base URL | `https://pub-8892b0ff54a14d2e91c70f633f3d6d6a.r2.dev` |
| R2 Account ID | `faaa1573a34da36e54a1d8a70e8c59a2` |
| psql local | requiere `PGPASSWORD=admin123` + `-h localhost` (peer auth por socket falla) |

---

## 📋 Pendientes (roadmap)

1. **Backend:** Endpoint API de imágenes (ViewSet + Serializer) → `GET /api/storage/imagenes/?grupo=...`
2. **Backend:** Consumo de `url_publica` desde React
3. **Frontend (Tienda Jabones):**
   - ⏳ Fase 1: `App.tsx` ✅ + `app.json` ✅ + `ThemeProvider.tsx` (pendiente)
   - Fase 2: Capa de datos R2 (`api/client.ts` + `storage.ts`)
   - Fase 3: Componentes UI (`CategoryCard`, `Carousel`, `BottomBar`, `Header`)
   - Fase 4: Pantalla Inicio + estilos del XML (`gemini-code-5.xml`)
4. **Optimización:** `banner.svg` (6.5 MB)
5. **Producción:** Custom Domain R2 (rate-limiting en r2.dev)
6. **Futuro:** Borrado de huérfanos en R2
