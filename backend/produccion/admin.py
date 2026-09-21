from django.contrib import admin
from .models import (
    Aroma,
    Color,
    Presentacion,
    ProductoTerminado,
    FormulaProducto,
    FaseProduccion,
    OrdenProduccion,
    DetalleProduccion,
    DetalleFaseProduccion,
    MermaProduccion,
    SeguimientoProduccion,
)


@admin.register(Aroma)
class AromaAdmin(admin.ModelAdmin):
    list_display = ("id_aroma", "nombre", "activo")
    search_fields = ("nombre",)
    list_filter = ("activo",)


@admin.register(Presentacion)
class PresentacionAdmin(admin.ModelAdmin):
    list_display = ("id_presentacion", "nombre", "activo")
    search_fields = ("nombre",)
    list_filter = ("activo",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("id_color", "nombre", "activo")
    search_fields = ("nombre",)
    list_filter = ("activo",)


@admin.register(ProductoTerminado)
class ProductoTerminadoAdmin(admin.ModelAdmin):
    list_display = ("id_producto", "codigo_producto", "nombre", "aroma", "peso", "tipo", "stock_disponible", "precio_venta", "activo")
    search_fields = ("nombre", "codigo_producto", "id_producto")
    list_filter = ("aroma", "peso", "tipo", "activo")


@admin.register(FormulaProducto)
class FormulaProductoAdmin(admin.ModelAdmin):
    list_display = ("id_formula", "id_producto", "id_insumo", "cantidad", "orden")
    search_fields = ("id_producto", "id_insumo", "id_formula")


@admin.register(FaseProduccion)
class FaseProduccionAdmin(admin.ModelAdmin):
    list_display = ("id_fase", "nombre", "orden_secuencia", "requiere_control_calidad", "activo")
    search_fields = ("nombre", "id_fase")


@admin.register(OrdenProduccion)
class OrdenProduccionAdmin(admin.ModelAdmin):
    list_display = ("id_orden", "numero_orden", "id_producto", "cantidad_producir", "cantidad_producida", "estado", "prioridad")
    search_fields = ("numero_orden", "id_orden", "id_producto")
    list_filter = ("estado", "prioridad")


@admin.register(DetalleProduccion)
class DetalleProduccionAdmin(admin.ModelAdmin):
    list_display = ("id_detalle_produccion", "id_orden", "id_insumo", "cantidad_requerida", "cantidad_usada")
    search_fields = ("id_orden", "id_insumo", "id_detalle_produccion")


@admin.register(DetalleFaseProduccion)
class DetalleFaseProduccionAdmin(admin.ModelAdmin):
    list_display = ("id_detalle_fase", "id_orden_produccion", "id_fase", "estado")
    search_fields = ("id_orden_produccion", "id_detalle_fase")
    list_filter = ("estado",)


@admin.register(MermaProduccion)
class MermaProduccionAdmin(admin.ModelAdmin):
    list_display = ("id_merma", "id_orden_produccion", "tipo_merma", "cantidad_perdida", "fecha_registro")
    search_fields = ("id_orden_produccion", "id_merma")
    list_filter = ("tipo_merma",)


@admin.register(SeguimientoProduccion)
class SeguimientoProduccionAdmin(admin.ModelAdmin):
    list_display = ("id_seguimiento", "id_orden_produccion", "numero_orden", "estado_actual", "porcentaje_avance")
    search_fields = ("numero_orden", "id_orden_produccion", "id_seguimiento")
    list_filter = ("estado_actual",)
