from datetime import date

from django.db import models

from inventario.models import MateriaPrima


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    ruc_ci = models.CharField(max_length=20, default="", unique=True)
    contacto = models.CharField(max_length=100, default="")
    telefono = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=100, default="")
    direccion = models.TextField(default="")
    fecha_registro = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("activo", "activo"),
            ("inactivo", "inactivo"),
        ],
        default="activo",
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "proveedor"

    def __str__(self):
        return self.nombre


class CompraMateriaPrima(models.Model):
    id_compra = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(
        "Proveedor",
        on_delete=models.RESTRICT,
        db_column="id_proveedor",
        related_name="compras",
    )
    numero_factura = models.CharField(max_length=50)
    tipo_factura = models.CharField(
        max_length=20,
        choices=[
            ("factura", "factura"),
            ("recibo", "recibo"),
            ("nota_venta", "nota_venta"),
            ("boleta", "boleta"),
        ],
        default="factura",
    )
    fecha_compra = models.DateField(default=date.today)
    fecha_recepcion = models.DateField(default=date.today)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "pendiente"),
            ("recibida", "recibida"),
            ("cancelada", "cancelada"),
            ("parcial", "parcial"),
        ],
        default="pendiente",
    )
    observaciones = models.TextField(default="")
    documento_url = models.CharField(max_length=255, default="")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "compra_materia_prima"
        constraints = [
            models.UniqueConstraint(
                fields=["numero_factura"], name="uq_compra_materia_prima_numero_factura"
            )
        ]

    def __str__(self):
        return self.numero_factura


class DetalleCompra(models.Model):
    id_detalle_compra = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(
        CompraMateriaPrima,
        on_delete=models.CASCADE,
        db_column="id_compra",
        related_name="detalles",
    )
    id_insumo = models.ForeignKey(
        MateriaPrima,
        on_delete=models.RESTRICT,
        db_column="id_insumo",
        related_name="detalles_compra",
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    lote = models.CharField(max_length=50, default="")
    fecha_vencimiento = models.DateField(default=date.today)
    observaciones = models.TextField(default="")

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    class Meta:
        db_table = "detalle_compra"

    def __str__(self):
        return f"{self.id_compra} - {self.id_insumo}"
