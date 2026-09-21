from django.contrib import admin
from .models import (
    Pedido,
    Carrito,
    Venta,
    DetalleVenta,
    Pago,
    Envio,
    HistorialNavegacion,
)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id_pedido", "numero_pedido", "id_usuario", "fecha_pedido", "estado", "estado_pago", "total", "stock_descontado")
    search_fields = ("numero_pedido", "id_pedido", "id_usuario")
    list_filter = ("estado", "estado_pago")


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ("id_carrito", "id_pedido", "id_producto", "cantidad", "precio_unitario")
    search_fields = ("id_pedido", "id_producto", "id_carrito")


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id_venta", "id_pedido", "fecha_venta", "total_venta", "tipo_venta")
    search_fields = ("id_pedido", "id_venta")
    list_filter = ("tipo_venta",)


@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("id_detalle_venta", "id_venta", "id_producto", "cantidad", "precio_unitario")
    search_fields = ("id_venta", "id_producto", "id_detalle_venta")


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id_pago", "id_pedido", "fecha_pago", "metodo_pago", "monto", "estado")
    search_fields = ("id_pedido", "id_pago", "referencia")
    list_filter = ("estado", "metodo_pago")


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ("id_envio", "id_pedido", "ciudad", "tipo_envio", "estado", "tracking_number")
    search_fields = ("tracking_number", "id_pedido", "id_envio")
    list_filter = ("estado",)


@admin.register(HistorialNavegacion)
class HistorialNavegacionAdmin(admin.ModelAdmin):
    list_display = ("id_historial", "id_usuario", "id_producto", "fecha_visita")
    search_fields = ("id_usuario", "id_producto", "id_historial")
