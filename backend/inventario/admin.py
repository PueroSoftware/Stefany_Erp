from django.contrib import admin
from .models import (
    CategoriaMateria,
    MateriaPrima,
    StockMateriaPrima,
    MermaStock,
    MovimientoStock,
)


@admin.register(CategoriaMateria)
class CategoriaMateriaAdmin(admin.ModelAdmin):
    list_display = ("id_categoria", "nombre", "tipo", "activo")
    search_fields = ("nombre", "id_categoria")
    list_filter = ("tipo", "activo")


@admin.register(MateriaPrima)
class MateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ("id_insumo", "nombre", "unidad_medida", "stock_minimo", "stock_maximo", "precio_promedio", "activo")
    search_fields = ("nombre", "id_insumo")
    list_filter = ("activo",)


@admin.register(StockMateriaPrima)
class StockMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ("id_stock", "id_insumo", "lote", "cantidad_disponible", "estado", "activo")
    search_fields = ("id_insumo", "lote", "id_stock")
    list_filter = ("estado", "activo")


@admin.register(MermaStock)
class MermaStockAdmin(admin.ModelAdmin):
    list_display = ("id_merma_stock", "id_insumo", "cantidad", "fecha_deteccion", "procesado")
    search_fields = ("id_insumo", "id_merma_stock")
    list_filter = ("procesado",)


@admin.register(MovimientoStock)
class MovimientoStockAdmin(admin.ModelAdmin):
    list_display = ("id_movimiento", "id_insumo", "tipo_movimiento", "cantidad", "fecha_movimiento", "usuario_registro")
    search_fields = ("id_insumo", "id_movimiento", "referencia_id")
    list_filter = ("tipo_movimiento",)
