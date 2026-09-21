from rest_framework import serializers
from .models import ObjectStorage, Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        # ⚠️ Enumeramos campos explícitamente para NO exponer el hash de la contraseña
        fields = [
            "id_usuario",
            "nombre",
            "apellido",
            "correo",
            "telefono",
            "direccion",
            "ciudad",
            "tipo",
            "estado",
            "activo",
            "fecha_registro",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    # write_only = se recibe para crear, pero nunca se devuelve en la respuesta
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ["nombre", "apellido", "correo", "password", "telefono", "tipo"]

    def create(self, validated_data):
        # create_user hashea la contraseña (set_password internamente)
        usuario = Usuario.objects.create_user(
            correo=validated_data["correo"],
            password=validated_data["password"],
            nombre=validated_data["nombre"],
            apellido=validated_data.get("apellido", ""),
            telefono=validated_data.get("telefono", ""),
            tipo=validated_data.get("tipo", "cliente"),
        )
        return usuario


class ObjectStorageSerializer(serializers.ModelSerializer):
    """Serializador de imágenes R2 — SOLO lectura para el catálogo público.
    read_only_fields garantiza que nadie pueda crear/editar registros vía API."""

    class Meta:
        model = ObjectStorage
        fields = [
            "id_archivo",
            "clave_r2",
            "url_publica",
            "grupo",
            "orden",
            "tipo_contenido",
            "tamano_bytes",
        ]
        # Nadie debe escribir aquí vía API: las imágenes las siembra sync_r2.
        read_only_fields = fields
