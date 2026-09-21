from django.test import TestCase
from core.models import Usuario
from produccion.models import ProductoTerminado
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def auth_client(user):
    """Devuelve un APIClient con el token JWT del usuario inyectado."""
    client = APIClient()
    token = str(RefreshToken.for_user(user).access_token)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


class ApiSeguridadYStockTests(TestCase):
    def setUp(self):
        self.cliente_a = Usuario.objects.create_user(
            correo="a@test.com", password="123456",
            nombre="A", tipo="cliente",
        )
        self.cliente_b = Usuario.objects.create_user(
            correo="b@test.com", password="123456",
            nombre="B", tipo="cliente",
        )
        self.fabril = Usuario.objects.create_user(
            correo="f@test.com", password="123456",
            nombre="F", tipo="fabril",
        )
        self.producto = ProductoTerminado.objects.create(
            nombre="Jabon Test", aroma="arroz",
            peso="100gr", tipo="jabon", stock_disponible=10,
            precio_costo=1, precio_venta=5,
        )

    # --- B2: catálogo público (anon puede leer) ---
    def test_catalogo_publico(self):
        resp = self.client.get("/api/produccion/productos-terminados/")
        self.assertEqual(resp.status_code, 200)

    # --- B2: endpoint de pedidos exige token ---
    def test_auth_requerida(self):
        resp = self.client.get("/api/ventas/pedidos/")
        self.assertEqual(resp.status_code, 401)

    # --- A1: cliente bloqueado en tablas fabriles ---
    def test_cliente_bloqueado_inventario(self):
        c = auth_client(self.cliente_a)
        resp = c.get("/api/inventario/stock-materias-primas/")
        self.assertEqual(resp.status_code, 403)

    # --- A1: cliente solo ve SUS pedidos (aislamiento por dueño) ---
    def test_aislamiento_dueno_pedidos(self):
        ca = auth_client(self.cliente_a)
        crear = ca.post("/api/ventas/pedidos/", {"numero_pedido": "P-A1"}, format="json")
        self.assertEqual(crear.status_code, 201)
        pid = crear.json()["id_pedido"]
        # cliente B intenta leer el pedido de A -> no debe existir para él
        cb = auth_client(self.cliente_b)
        resp = cb.get(f"/api/ventas/pedidos/{pid}/")
        self.assertEqual(resp.status_code, 404)

    # --- A3: confirmar pedido descuenta stock (una sola vez) ---
    def test_descuento_stock_al_confirmar(self):
        ca = auth_client(self.cliente_a)
        ped = ca.post("/api/ventas/pedidos/", {"numero_pedido": "P-A2"}, format="json")
        pid = ped.json()["id_pedido"]
        ca.post("/api/ventas/carritos/", {
            "id_pedido": pid, "id_producto": self.producto.id_producto,
            "cantidad": 3, "precio_unitario": "5.00",
        }, format="json")
        # confirmar
        resp = ca.patch(f"/api/ventas/pedidos/{pid}/", {"estado": "confirmado"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_disponible, 7)
        # confirmar de nuevo no descuenta doble
        ca.patch(f"/api/ventas/pedidos/{pid}/", {"estado": "confirmado"}, format="json")
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock_disponible, 7)

    # --- A2: endpoint "Mi perfil" ---
    def test_mi_perfil(self):
        ca = auth_client(self.cliente_a)
        resp = ca.get("/api/auth/me/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["correo"], "a@test.com")
