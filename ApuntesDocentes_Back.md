# Apuntes Docentes – Backend con Django (ERP TiendaSoap)

> Documento de apoyo para el estudiante. Recopila toda la teoría explicada
> durante el desarrollo del backend del ERP. Lenguaje: castellano.
> Estilo: para cada tema se indica **qué es**, **por qué se usa**, **dónde vive**
> en el código y una **analogía** cuando el concepto es abstracto.

---

## 0. El flujo completo (la "película" de una petición)

Antes de entrar a cada pieza, memoriza este recorrido. Toda petición HTTP en
Django REST Framework (DRF) viaja así:

```
Usuario → Navegador/App → (HTTP) → URL → View/ViewSet → Serializer
        → Modelo (ORM) → Base de datos PostgreSQL → Respuesta JSON → Cliente
```

- **URL**: decide qué función atiende la ruta.
- **View/ViewSet**: contiene la lógica de negocio.
- **Serializer**: traduce entre JSON ↔ objetos Python/Django.
- **Modelo + ORM**: escribe/lee en la base de datos sin escribir SQL a mano.
- **Respuesta**: DRF la vuelve a convertir en JSON.

**Analogía:** imagina un restaurante. La **URL** es el maître que te asigna
mesa; la **View** es el chef; el **Serializer** es el traductor que pasa el
pedido del cliente al chef y el plato del chef al cliente; el **Modelo/ORM**
es la despensa y nevera; la **Base de datos** es la nevera física.

---

## 1. Estructura del proyecto

```
Erp_Stefanny_Django/
├── backend/                 # Proyecto Django
│   ├── config/              # settings.py, urls.py, wsgi.py (configuración global)
│   ├── core/                # Usuario, autenticación, permisos, "Mi perfil"
│   ├── inventario/          # Materias primas, stock, mermas (SOLO FABRIL)
│   ├── compras/             # Proveedores, compras (SOLO FABRIL)
│   ├── produccion/          # Productos terminados, órdenes (FABRIL + catálogo público)
│   ├── ventas/              # Pedidos, carrito, ventas, pagos (CLIENTE + FABRIL)
│   ├── tests_api.py         # Pruebas automáticas solo-backend
│   └── manage.py
└── frontend/                # React (FUERA del backend; aún no conectado)
```

Cada app Django tiene: `models.py`, `serializers.py`, `views.py`, `urls.py`,
`admin.py`, `migrations/`.

**Concepto clave – App:** una app es un módulo de funcionalidad cohesivo.
Separar por dominio (inventario, ventas…) sigue el principio de **Responsabilidad
Única (SRP)** de SOLID.

---

## 2. Modelos y ORM

### ¿Qué es un modelo?
Es la definición de una tabla de base de datos en código Python. Django crea
la tabla SQL automáticamente a partir de la clase.

```python
from django.db import models

class ProductoTerminado(models.Model):
    id_producto = models.AutoField(primary_key=True)  # PK entero autoincremental
    nombre = models.CharField(max_length=100)
    stock_disponible = models.IntegerField(default=0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = "producto_terminado"   # nombre real en la BD
```

### ORM (Object Relational Mapper)
El ORM traduce código Python a SQL. En vez de escribir
`SELECT * FROM producto_terminado WHERE stock_disponible > 0`, escribes:

```python
ProductoTerminado.objects.filter(stock_disponible__gt=0)
```

**¿Por qué usar ORM?** Evitas SQL inyectable a mano, ganas portabilidad entre
motores y el código queda legible. El ORM también te protege de **SQL Injection**
porque escapa los parámetros.

### La regla "sin vacíos" (criterio del proyecto)
Nunca usamos `null=True`/`blank=True` salvo justificación. Reglas:

- Texto opcional → `default=""`.
- Número opcional → `default=0`.
- Fecha opcional → `default=timezone.now` o `null=True` solo si es fecha real vacía.
- Clave foránea → `on_delete=models.RESTRICT` (no borres en cascada datos
  contables; `RESTRICT` impide borrar si hay hijos).

**¿Por qué?** Los campos `NULL` complican validaciones y reportes. Mejor un
valor explícito (`""`, `0`) que un hueco desconocido.

### Clave primaria: AutoField, no string
`id_usuario`, `id_producto`, etc. son **`AutoField` (entero)**. No les pasamos
texto al crear objetos; el número lo genera la BD. En los tests usamos el valor
autogenerado: `self.producto.id_producto`.

### Migraciones
Cada cambio en `models.py` se materializa en la BD con dos comandos:

```bash
python manage.py makemigrations   # genera el script de cambio
python manage.py migrate          # aplica el script a PostgreSQL
```

**Analogía:** `makemigrations` es escribir la receta; `migrate` es cocinarla.

---

## 3. Serializers (traductores JSON ↔ Python)

El Serializer convierte el JSON entrante en datos válidos del modelo y viceversa.

```python
from rest_framework import serializers
from .models import Pedido

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"            # todos los campos del modelo
        read_only_fields = ("id_usuario",)  # lo fija el servidor, no el cliente
```

- `fields = "__all__"`: exponer todo. Práctico al inicio; en producción se
  limita lo que el cliente puede leer/escribir.
- `read_only_fields`: campos que el servidor controla (ej. el dueño del pedido).
  Si no los marcas `read_only`, DRF exigirá que el cliente los envíe y romperá
  el POST con 400.

**¿Por qué el servidor fija `id_usuario`?** Por seguridad: un cliente no debe
poder falsificar "este pedido es de otro usuario". El `perform_create` del
ViewSet lo asigna desde el token.

---

## 4. Views y ViewSets

### APIView vs ViewSet
- `APIView`: una vista manual (ej. `RegisterView`, `MeView`) para casos a medida.
- `ModelViewSet`: CRUD completo (list, create, retrieve, update, partial_update,
  destroy) sobre un modelo, listo para un router.

### Router y el requisito `queryset`
Un `ModelViewSet` **necesita** `queryset = Model.objects.all()` (o pasar
`basename` al router) para que DRF derive el nombre de la ruta. Por eso, al
añadir `get_queryset` personalizado, dejamos también `queryset` definido.

```python
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsOwnerOrFabril]

    def get_queryset(self):
        qs = Pedido.objects.all()
        if self.request.user.tipo != "fabril":
            qs = qs.filter(id_usuario=self.request.user)  # cada cliente ve los suyos
        return qs

    def perform_create(self, serializer):
        serializer.save(id_usuario=self.request.user)  # dueño = usuario autenticado
```

- `get_queryset`: filtra la lista (multi-tenant: cada cliente solo ve sus datos).
- `perform_create` / `perform_update`: lugar ideal para lógica extra (fijar dueño,
  descontar stock) justo antes de guardar.

---

## 5. Permisos (autorización = qué puede hacer)

DRF separa **autenticación** (¿quién eres?) de **autorización** (¿qué puedes?).
Los permisos viven en `core/permissions.py` y se aplican con
`permission_classes = [...]`.

### BasePermission y SAFE_METHODS
```python
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsFabril(BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, "tipo", None) == "fabril")
```

- `has_permission`: se evalúa **antes** de entrar (¿puede usar la vista?).
- `has_object_permission`: se evalúa **por objeto** (¿puede tocar ESTE registro?).
- `SAFE_METHODS` = `GET, HEAD, OPTIONS` (lectura).

### Jerarquía de permisos usados en el proyecto
| Permiso | Regla |
|---|---|
| `IsFabril` | Solo usuarios con `tipo="fabril"`. |
| `IsFabrilOrReadOnly` | Fabril todo; los demás solo lectura (catálogo público). |
| `IsFabrilOrClienteWrite` | Lectura/escritura autenticados; edición solo fabril. |
| `IsOwnerOrFabril` | Fabril todo; cliente solo sus propios datos (por `id_usuario`/pedido). |

`IsOwnerOrFabril` resuelve el dueño así:
```python
def _owner_id(self, obj):
    if getattr(obj, "id_usuario_id", None):      return obj.id_usuario_id
    if getattr(obj, "id_pedido", None) is not None: return obj.id_pedido.id_usuario_id
    if getattr(obj, "id_venta", None) is not None:  return obj.id_venta.id_pedido.id_usuario_id
    return None
```
**Por qué importa:** sin esto, un cliente autenticado podría leer/modificar los
pedidos de otro (fuga de datos multi-tenant).

---

## 6. Autenticación y JWT

Usamos **djangorestframework-simplejwt**. El flujo:

1. `POST /api/auth/login/` con correo+password → devuelve `access` (corta vida)
   y `refresh` (larga vida).
2. El cliente manda `Authorization: Bearer <access>` en cada petición.
3. DRF valida el token con `JWTAuthentication`.

```python
# settings.py
SIMPLE_JWT = {
    "USER_ID_FIELD": "id_usuario",   # nuestro PK no es "id", es "id_usuario"
}
```

**¿Por qué `USER_ID_FIELD`?** SimpleJWT asume que la PK se llama `id`. Como
nuestro usuario usa `id_usuario`, hay que decírselo o falla con
`AttributeError: 'Usuario' object has no attribute 'id'`.

### "Mi perfil" (endpoint autenticado)
```python
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UsuarioSerializer(request.user).data)
```
`request.user` es el usuario del token. El cliente no envía su id; el servidor
lo saca del token (más seguro).

---

## 7. Configuración DRF y CORS

`config/settings.py` define el comportamiento global:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticatedOrReadOnly",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
}
```

- `IsAuthenticatedOrReadOnly`: cualquiera lee; para escribir hay que loguearse.
- `PAGE_SIZE`: las listas vienen paginadas (clave `results`, `count`).
- **CORS** (`django-cors-headers`): permite que el frontend (otro origen/puerto)
  consuma la API. En desarrollo `CORS_ALLOW_ALL_ORIGINS = True`; en producción
  se lista `CORS_ALLOWED_ORIGINS` explícita.

**Bug real del proyecto:** escribir `REST__FRAMEWORK` (doble guion) en vez de
`REST_FRAMEWORK` hace que DRF no aplique la autenticación JWT y todo falla en
silencio. Revisa siempre la ortografía de las claves de settings.

---

## 8. Filtros del catálogo (django-filter + SearchFilter)

El catálogo de productos es público para clientes, pero debe poder filtrarse:

```python
class ProductoTerminadoViewSet(viewsets.ModelViewSet):
    queryset = ProductoTerminado.objects.all()
    serializer_class = ProductoTerminadoSerializer
    permission_classes = [IsFabrilOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["aroma", "peso", "tipo"]      # ?aroma=arroz
    search_fields = ["nombre", "descripcion"]          # ?search=jabon
    ordering_fields = ["precio_venta", "stock_disponible"]
```

URL ejemplo: `/api/produccion/productos-terminados/?aroma=arroz&search=jabon`.

---

## 9. Separación de roles (cliente vs fabril) – arquitectura de negocio

No es solo una etiqueta: define qué tablas son **exclusivas fabril** y cuáles
el cliente puede tocar.

- **Exclusiva fabril:** inventario, compras, producción (interna), mermas.
- **Cliente:** lee catálogo (ProductoTerminado, público) y gestiona sus propios
  pedidos/ventas/carrito/pagos.
- **Ambos:** ventas (el cliente escribe lo suyo; el fabril ve todo).

El backend **impone** esto con permisos; el frontend solo **muestra/oculta**
botones. Nunca confíes solo en el frontend para seguridad.

---

## 10. Lógica de stock y transacciones

Cuando se confirma un pedido (o se crea una venta) descontamos el stock:

```python
from django.db import transaction

def perform_update(self, serializer):
    instance = self.get_object()
    nuevo = serializer.validated_data.get("estado", instance.estado)
    if nuevo == "confirmado" and not instance.stock_descontado:
        with transaction.atomic():
            pedido = serializer.save()
            for item in pedido.carrito.all():
                prod = item.id_producto
                prod.stock_disponible -= item.cantidad
                prod.save()
            pedido.stock_descontado = True
            pedido.save()
```

- `transaction.atomic()`: si algo falla a la mitad, se reversa todo (el stock no
  queda inconsistente).
- `stock_descontado`: bandera que evita descontar **dos veces** si el pedido se
  confirma y luego se crea la venta (ambos disparadores del mismo carrito).

**Analogía:** es como cobrar una tarjeta; si el banco descuenta al confirmar y
otra vez al entregar, cobras doble. La bandera garantiza un solo cobro.

---

## 11. Admin de Django

`/admin` es el panel nativo. Mejoramos cada `admin.py` con `ModelAdmin`:

```python
@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ("id_producto", "nombre", "aroma", "stock_disponible", "precio_venta")
    search_fields = ("nombre", "codigo_producto")
    list_filter = ("aroma", "peso", "tipo", "activo")
```

- `list_display`: columnas de la tabla.
- `search_fields`: caja de búsqueda.
- `list_filter`: filtros laterales.

---

## 12. Testing solo-backend

`tests_api.py` usa `APITestCase` + `APIClient` para probar la API sin navegador:

```python
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

def auth_client(user):
    c = APIClient()
    token = str(RefreshToken.for_user(user).access_token)
    c.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return c

class ApiTests(TestCase):
    def test_catalogo_publico(self):
        resp = self.client.get("/api/produccion/productos-terminados/")
        self.assertEqual(resp.status_code, 200)
```

Ejecutar:
```bash
cd backend && source venv/bin/activate
python manage.py test tests_api -v1
```

Cubre: catálogo público, auth requerida, bloqueo de rol, aislamiento por dueño,
descuento de stock sin doble, y "Mi perfil". **Resultado: 6/6 pasan.**

**Prueba manual rápida (curl):**
```bash
# login
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" \
  -d '{"correo":"ana@test.com","password":"123456"}'

# catálogo público
curl "http://localhost:8000/api/produccion/productos-terminados/?aroma=arroz"
```

---

## 13. Seguridad (Regla Bronce) – checklist

- ✔ Autenticación JWT con `USER_ID_FIELD` correcto.
- ✔ Autorización por permisos (`IsFabril`, `IsOwnerOrFabril`…).
- ✔ Validación en Serializers; el servidor fija campos sensibles (`id_usuario`).
- ✔ ORM evita SQL Injection; `on_delete=RESTRICT` protege integridad.
- ✔ CORS abierto solo en DEBUG; en producción orígenes explícitos.
- ✔ Secretos vía `os.getenv` (`.env`), no hardcodeados.
- ⚠ El catálogo público NO expone datos de clientes (solo productos).
- ❌ Nunca confíes en el frontend para ocultar datos sensibles.

---

## 14. Buenas prácticas (SOLID / DRY / KISS)

- **SRP:** cada app un dominio; cada permiso una regla.
- **DRY:** `IsOwnerOrFabril` reutilizado en los 7 ViewSets de ventas.
- **KISS:** `stock_descontado` (un booleano) resuelve el doble descuento sin
  arquitecturas complejas.
- **Open/Closed:** añadir un filtro al catálogo = una línea, sin tocar la lógica.

---

## 15. Glosario de conceptos aprendidos

- **Endpoint:** la combinación URL + método HTTP (ej. `POST /api/auth/login/`).
  "Punto final" = dónde termina la petición del cliente y empieza el backend.
- **Singleton (conexión BD):** Django ya gestiona una única conexión/pool a
  PostgreSQL de forma interna; **no** implementamos patrón Singleton a mano.
- **JWT:** token firmado que viaja en la cabecera; el backend lo valida sin
  consultar sesión (es stateless).
- **Multi-tenant:** varios clientes comparten la BD pero cada uno ve solo lo suyo
  (filtrado por `id_usuario` en `get_queryset`).
- **Transacción atómica:** conjunto de operaciones que se confirman juntas o se
  revierten juntas.
- **Migración:** script que transforma el esquema de la BD para igualarlo a los
  modelos.

---

## 16. Comandos útiles

```bash
python manage.py check            # valida la configuración (0 silenced = OK)
python manage.py makemigrations   # genera cambios de modelo
python manage.py migrate          # aplica migraciones
python manage.py test tests_api   # pruebas solo-backend
python manage.py runserver        # servidor de desarrollo en :8000
```

---

### Resumen para el estudiante
Lo que acabas de repasar es el **esqueleto completo de un backend API REST con
Django**: modelos + ORM, serializers, viewsets, permisos de rol, autenticación
JWT, filtros, transacciones de stock, admin y pruebas automáticas. Con esto
puedes leer cualquier API DRF y explicar cada capa de forma profesional.
