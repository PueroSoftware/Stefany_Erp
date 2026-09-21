from rest_framework.routers import DefaultRouter
from .views import (
    PedidoViewSet,
    CarritoViewSet,
    VentaViewSet,
    DetalleVentaViewSet,
    PagoViewSet,
    EnvioViewSet,
    HistorialNavegacionViewSet,
)

router = DefaultRouter()
router.register("pedidos", PedidoViewSet)
router.register("carritos", CarritoViewSet)
router.register("ventas", VentaViewSet)
router.register("detalles-venta", DetalleVentaViewSet)
router.register("pagos", PagoViewSet)
router.register("envios", EnvioViewSet)
router.register("historial-navegacion", HistorialNavegacionViewSet)

urlpatterns = router.urls
