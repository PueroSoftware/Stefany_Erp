from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaMateriaViewSet,
    MateriaPrimaViewSet,
    StockMateriaPrimaViewSet,
    MermaStockViewSet,
    MovimientoStockViewSet,
)

router = DefaultRouter()
router.register("categorias", CategoriaMateriaViewSet)
router.register("materias-primas", MateriaPrimaViewSet)
router.register("stock-materias-primas", StockMateriaPrimaViewSet)
router.register("mermas-stock", MermaStockViewSet)
router.register("movimientos-stock", MovimientoStockViewSet)

urlpatterns = router.urls
