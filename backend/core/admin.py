from django.contrib import admin

from core.models import ObjectStorage, Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id_usuario",
        "nombre",
        "apellido",
        "correo",
        "tipo",
        "estado",
        "activo",
    )
    search_fields = ("nombre", "apellido", "correo", "id_usuario")
    list_filter = ("tipo", "estado", "activo")


@admin.register(ObjectStorage)
class ObjectStorageAdmin(admin.ModelAdmin):
    # Columnas visibles en el listado
    list_display = (
        "clave_r2",
        "grupo",
        "orden",
        "tipo_contenido",
        "tamano_bytes",
        "activo",
    )
    # Filtros laterales
    list_filter = ("grupo", "tipo_contenido", "activo")
    # Buscador superior (búsqueda insensible a mayúsculas con icontains)
    search_fields = ("clave_r2", "url_publica", "grupo")
    # Orden por defecto del listado
    ordering = ("grupo", "orden")
