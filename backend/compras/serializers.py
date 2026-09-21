from rest_framework import serializers
from .models import Proveedor, CompraMateriaPrima, DetalleCompra


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = "__all__"


class CompraMateriaPrimaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompraMateriaPrima
        fields = "__all__"


class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = "__all__"
