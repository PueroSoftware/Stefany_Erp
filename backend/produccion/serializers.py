from rest_framework import serializers

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


class ProductoTerminadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoTerminado
        fields = "__all__"


class FormulaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormulaProducto
        fields = "__all__"


class FaseProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaseProduccion
        fields = "__all__"


class OrdenProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenProduccion
        fields = "__all__"


class DetalleProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleProduccion
        fields = "__all__"


class DetalleFaseProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleFaseProduccion
        fields = "__all__"


class MermaProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MermaProduccion
        fields = "__all__"


class SeguimientoProduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguimientoProduccion
        fields = "__all__"


class AromaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aroma
        fields = "__all__"


class PresentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentacion
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = "__all__"
