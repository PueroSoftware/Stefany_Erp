from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ProveedorViewSet,
    CompraMateriaPrimaViewSet,
    DetalleCompraViewSet,
    RegistrarCompraView,
)

router = DefaultRouter()
router.register("proveedores", ProveedorViewSet)
router.register("compras", CompraMateriaPrimaViewSet)
router.register("detalles-compra", DetalleCompraViewSet)

urlpatterns = router.urls + [
    path("sp/registrar-compra/", RegistrarCompraView.as_view(), name="sp_registrar_compra"),
]
