from core.permissions import IsFabril, IsFabrilOrReadOnly
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Aroma,
    Color,
    DetalleFaseProduccion,
    DetalleProduccion,
    FaseProduccion,
    FormulaProducto,
    MermaProduccion,
    OrdenProduccion,
    Presentacion,
    ProductoTerminado,
    SeguimientoProduccion,
)
from .serializers import (
    AromaSerializer,
    ColorSerializer,
    DetalleFaseProduccionSerializer,
    DetalleProduccionSerializer,
    FaseProduccionSerializer,
    FormulaProductoSerializer,
    MermaProduccionSerializer,
    OrdenProduccionSerializer,
    PresentacionSerializer,
    ProductoTerminadoSerializer,
    SeguimientoProduccionSerializer,
)


class ProductoTerminadoViewSet(viewsets.ModelViewSet):
    queryset = ProductoTerminado.objects.all()
    serializer_class = ProductoTerminadoSerializer
    permission_classes = [IsFabrilOrReadOnly]
    # B1: filtros para el catálogo público de clientes
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["aroma", "peso", "tipo"]
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["precio_venta", "stock_disponible", "nombre"]


class FormulaProductoViewSet(viewsets.ModelViewSet):
    queryset = FormulaProducto.objects.all()
    serializer_class = FormulaProductoSerializer


class AromaViewSet(viewsets.ModelViewSet):
    queryset = Aroma.objects.all()
    serializer_class = AromaSerializer
    permission_classes = [IsFabrilOrReadOnly]


class PresentacionViewSet(viewsets.ModelViewSet):
    queryset = Presentacion.objects.all()
    serializer_class = PresentacionSerializer
    permission_classes = [IsFabrilOrReadOnly]


class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsFabrilOrReadOnly]


class FaseProduccionViewSet(viewsets.ModelViewSet):
    queryset = FaseProduccion.objects.all()
    serializer_class = FaseProduccionSerializer
    permission_classes = [IsFabril]


class OrdenProduccionViewSet(viewsets.ModelViewSet):
    queryset = OrdenProduccion.objects.all()
    serializer_class = OrdenProduccionSerializer
    permission_classes = [IsFabril]


class DetalleProduccionViewSet(viewsets.ModelViewSet):
    queryset = DetalleProduccion.objects.all()
    serializer_class = DetalleProduccionSerializer
    permission_classes = [IsFabril]


class DetalleFaseProduccionViewSet(viewsets.ModelViewSet):
    queryset = DetalleFaseProduccion.objects.all()
    serializer_class = DetalleFaseProduccionSerializer
    permission_classes = [IsFabril]


class MermaProduccionViewSet(viewsets.ModelViewSet):
    queryset = MermaProduccion.objects.all()
    serializer_class = MermaProduccionSerializer
    permission_classes = [IsFabril]


class SeguimientoProduccionViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoProduccion.objects.all()
    serializer_class = SeguimientoProduccionSerializer
    permission_classes = [IsFabril]
