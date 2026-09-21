from core.permissions import IsFabril
from rest_framework import viewsets

from .models import (
    CategoriaMateria,
    MateriaPrima,
    MermaStock,
    MovimientoStock,
    StockMateriaPrima,
)
from .serializers import (
    CategoriaMateriaSerializer,
    MateriaPrimaSerializer,
    MermaStockSerializer,
    MovimientoStockSerializer,
    StockMateriaPrimaSerializer,
)


class CategoriaMateriaViewSet(viewsets.ModelViewSet):
    queryset = CategoriaMateria.objects.all()
    serializer_class = CategoriaMateriaSerializer
    permission_classes = [IsFabril]


class MateriaPrimaViewSet(viewsets.ModelViewSet):
    queryset = MateriaPrima.objects.all()
    serializer_class = MateriaPrimaSerializer
    permission_classes = [IsFabril]


class StockMateriaPrimaViewSet(viewsets.ModelViewSet):
    queryset = StockMateriaPrima.objects.all()
    serializer_class = StockMateriaPrimaSerializer
    permission_classes = [IsFabril]


class MermaStockViewSet(viewsets.ModelViewSet):
    queryset = MermaStock.objects.all()
    serializer_class = MermaStockSerializer
    permission_classes = [IsFabril]


class MovimientoStockViewSet(viewsets.ModelViewSet):
    queryset = MovimientoStock.objects.all()
    serializer_class = MovimientoStockSerializer
    permission_classes = [IsFabril]
