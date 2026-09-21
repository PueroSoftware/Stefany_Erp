from rest_framework.routers import DefaultRouter
from .views import (
    AromaViewSet,
    ColorViewSet,
    PresentacionViewSet,
    ProductoTerminadoViewSet,
    FormulaProductoViewSet,
    FaseProduccionViewSet,
    OrdenProduccionViewSet,
    DetalleProduccionViewSet,
    DetalleFaseProduccionViewSet,
    MermaProduccionViewSet,
    SeguimientoProduccionViewSet,
)

router = DefaultRouter()
router.register("productos-terminados", ProductoTerminadoViewSet)
router.register("aromas", AromaViewSet)
router.register("presentaciones", PresentacionViewSet)
router.register("colores", ColorViewSet)
router.register("formula-producto", FormulaProductoViewSet)
router.register("fases-produccion", FaseProduccionViewSet)
router.register("ordenes-produccion", OrdenProduccionViewSet)
router.register("detalles-produccion", DetalleProduccionViewSet)
router.register("detalles-fase-produccion", DetalleFaseProduccionViewSet)
router.register("mermas-produccion", MermaProduccionViewSet)
router.register("seguimientos-produccion", SeguimientoProduccionViewSet)

urlpatterns = router.urls
