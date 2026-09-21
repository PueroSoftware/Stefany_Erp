from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import ObjectStorage, Usuario


class ObjectStorageAPITests(TestCase):
    """Tests del catálogo público de imágenes R2 (GET /api/storage/imagenes/)."""

    def setUp(self):
        self.client = APIClient()
        self.usuario_cliente = Usuario.objects.create_user(
            correo="cliente@tiendaweb.com",
            password="secreta123",
            nombre="Cliente",
            tipo="cliente",
        )
        self.usuario_fabril = self.crear_usuario(
            correo="fabril@tiendaweb.com",
            tipo="fabril",
        )
        ObjectStorage.objects.create(
            clave_r2="grupos/jabones.webp",
            url_publica="https://pub-test.r2.dev/grupos/jabones.webp",
            grupo="grupos",
            orden=1,
        )
        ObjectStorage.objects.create(
            clave_r2="esencias/lavanda.webp",
            url_publica="https://pub-test.r2.dev/esencias/lavanda.webp",
            grupo="esencias",
            orden=1,
        )
        # Imagen inactiva: NO debe aparecer en el catálogo público
        ObjectStorage.objects.create(
            clave_r2="esencias/rebasadas.webp",
            url_publica="https://pub-test.r2.dev/esencias/rebasadas.webp",
            grupo="esencias",
            orden=2,
            activo=False,
        )

    def crear_usuario(self, **kwargs):
        datos = {"nombre": "Test", "correo": "test@tiendasoap.com", "password": "clave123", "tipo": "cliente"}
        datos.update(kwargs)
        return Usuario.objects.create_user(**datos)

    # --- Acceso público --------------------------------------------------

    def test_listado_publico_sin_token(self):
        # GET sin autenticación debe funcionar: el catálogo de imágenes es público.
        response = self.client.get("/api/storage/imagenes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

    def test_ordena_por_grupo_y_orden(self):
        # Meta.ordering = ["grupo", "orden"] → alfabético por grupo: "esencias" antes que "grupos".
        response = self.client.get("/api/storage/imagenes/")
        claves = [item["clave_r2"] for item in response.data["results"]]
        self.assertEqual(claves, ["esencias/lavanda.webp", "grupos/jabones.webp"])

    def test_excluye_inactivas(self):
        # activo=False nunca se expone aunque el cliente lo pida por grupo.
        response = self.client.get("/api/storage/imagenes/")
        claves = [item["clave_r2"] for item in response.data["results"]]
        self.assertNotIn("esencias/rebasadas.webp", claves)

    # --- Filtro por grupo ------------------------------------------------

    def test_filtra_por_grupo(self):
        response = self.client.get("/api/storage/imagenes/?grupo=esencias")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["clave_r2"], "esencias/lavanda.webp")

    def test_grupo_sin_resultados(self):
        response = self.client.get("/api/storage/imagenes/?grupo=no-existe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    # --- Estructura de la respuesta --------------------------------------

    def test_campos_esperados_y_privacidad(self):
        # La respuesta expone lo mínimo: URL + metadata. Nunca datos de usuarios.
        response = self.client.get("/api/storage/imagenes/")
        item = response.data["results"][0]
        self.assertEqual(
            set(item.keys()),
            {"id_archivo", "clave_r2", "url_publica", "grupo", "orden", "tipo_contenido", "tamano_bytes"},
        )

    def test_detalle_por_id(self):
        item = ObjectStorage.objects.get(clave_r2="grupos/jabones.webp")
        response = self.client.get(f"/api/storage/imagenes/{item.id_archivo}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["url_publica"], item.url_publica)

    # --- Seguridad: solo lectura ------------------------------------------

    def test_no_se_puede_crear_via_api(self):
        # El ViewSet es read-only (ReadOnlyModelViewSet): ni siquiera un usuario
        # fabril autenticado puede crear. El permiso check pasa por ser fabril
        # y después el dispatcher responde 405 porque no existe acción "create".
        self.client.force_authenticate(self.usuario_fabril)
        response = self.client.post(
            "/api/storage/imagenes/",
            {"clave_r2": "hack.webp", "url_publica": "https://evil.example/", "grupo": "hack"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_no_se_puede_modificar_via_api(self):
        item = ObjectStorage.objects.get(clave_r2="grupos/jabones.webp")
        self.client.force_authenticate(self.usuario_fabril)
        response = self.client.delete(f"/api/storage/imagenes/{item.id_archivo}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        # Y el registro sigue en la base de datos (ni borrado ni alterado).
        self.assertTrue(ObjectStorage.objects.filter(id_archivo=item.id_archivo).exists())


class AuthTests(TestCase):
    """Smoke test: registro y login con JWT siguen funcionando tras los cambios."""

    def setUp(self):
        self.client = APIClient()

    def test_registro_y_login(self):
        registro = self.client.post(
            "/api/auth/register/",
            {"nombre": "Ana", "correo": "ana@tiendasoap.com", "password": "secreta123", "tipo": "cliente"},
        )
        self.assertEqual(registro.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", registro.data)

        login = self.client.post(
            "/api/auth/login/",
            {"correo": "ana@tiendasoap.com", "password": "secreta123"},
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn("access", login.data)