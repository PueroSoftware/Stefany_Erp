from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True")
        return self.create_user(correo, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    objects = UsuarioManager()

    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(
        max_length=20,
        choices=[("cliente", "Cliente"), ("fabril", "fabril")],
        default="cliente",
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ("activo", "Activo"),
            ("inactivo", "Inactivo"),
            ("bloqueado", "bloqueado"),
        ],
        default="activo",
    )
    is_staff = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre"]

    class Meta:
        db_table = "usuario"

    def __str__(self):
        return self.nombre or self.correo


class ObjectStorage(models.Model):
    # Registro de archivos alojados en Cloudflare R2.
    # Guarda la RUTA/URL de cada objeto, nunca el binario (anti-patron blob).

    id_archivo = models.AutoField(primary_key=True)
    clave_r2 = models.CharField(max_length=255, unique=True)  # ej: sliders/aromas/lavanda.webp
    url_publica = models.CharField(max_length=500)
    grupo = models.CharField(max_length=100, blank=True, default="")  # carpeta/slider logico
    orden = models.PositiveIntegerField(default=0)
    tipo_contenido = models.CharField(max_length=100, blank=True, default="")  # mime: image/webp
    tamano_bytes = models.BigIntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "objectstorage"
        ordering = ["grupo", "orden"]

    def __str__(self):
        return self.clave_r2
