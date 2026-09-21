from rest_framework import serializers
from .models import (
    CategoriaMateria,
    MateriaPrima,
    StockMateriaPrima,
    MermaStock,
    MovimientoStock,
)


class CategoriaMateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaMateria
        fields = "__all__"


class MateriaPrimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MateriaPrima
        fields = "__all__"


class StockMateriaPrimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMateriaPrima
        fields = "__all__"


class MermaStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MermaStock
        fields = "__all__"


class MovimientoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoStock
        fields = "__all__"
