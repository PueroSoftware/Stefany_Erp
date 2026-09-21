from django.contrib import admin
from .models import Proveedor, CompraMateriaPrima, DetalleCompra


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("id_proveedor", "nombre", "ruc_ci", "estado", "activo")
    search_fields = ("nombre", "ruc_ci", "id_proveedor")
    list_filter = ("estado", "activo")


@admin.register(CompraMateriaPrima)
class CompraMateriaPrimaAdmin(admin.ModelAdmin):
    list_display = ("id_compra", "id_proveedor", "numero_factura", "fecha_compra", "total", "estado")
    search_fields = ("numero_factura", "id_compra")
    list_filter = ("estado",)


@admin.register(DetalleCompra)
class DetalleCompraAdmin(admin.ModelAdmin):
    list_display = ("id_detalle_compra", "id_compra", "id_insumo", "cantidad", "precio_unitario")
    search_fields = ("id_compra", "id_insumo", "id_detalle_compra")
