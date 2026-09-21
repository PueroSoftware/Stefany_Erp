from rest_framework import serializers
from .models import (
    Pedido,
    Carrito,
    Venta,
    DetalleVenta,
    Pago,
    Envio,
    HistorialNavegacion,
)


class PedidoSerializer(serializers.ModelSerializer):
    # id_usuario lo fija el servidor en perform_create (no lo manda el cliente)
    class Meta:
        model = Pedido
        fields = "__all__"
        read_only_fields = ("id_usuario",)


class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = "__all__"


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = "__all__"


class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = "__all__"


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = "__all__"


class EnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envio
        fields = "__all__"


class HistorialNavegacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialNavegacion
        fields = "__all__"
        read_only_fields = ("id_usuario",)
