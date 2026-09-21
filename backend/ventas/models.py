from datetime import date
from django.utils import timezone
from django.db import models
from core.models import Usuario
from produccion.models import ProductoTerminado


class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    numero_pedido = models.CharField(max_length=20, default="", unique=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.RESTRICT,
        db_column="id_usuario",
        related_name="pedidos",
    )
    fecha_pedido = models.DateTimeField(default=timezone.now)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "pendiente"),
            ("confirmado", "confirmado"),
            ("en_proceso", "en_proceso"),
            ("listo", "listo"),
            ("enviado", "enviado"),
            ("entregado", "entregado"),
            ("cancelado", "cancelado"),
        ],
        default="pendiente",
    )
    metodo_pago = models.CharField(
        max_length=20,
        choices=[
            ("efectivo", "efectivo"),
            ("transferencia", "transferencia"),
            ("paypal", "paypal"),
            ("tarjeta", "tarjeta"),
            ("datafono", "datafono"),
        ],
        default="efectivo",
    )
    estado_pago = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "pendiente"),
            ("pagado", "pagado"),
            ("parcial", "parcial"),
            ("fallido", "fallido"),
            ("reembolsado", "reembolsado"),
        ],
        default="pendiente",
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    envio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observaciones = models.TextField(default="")
    direccion_envio = models.TextField(default="")
    contacto_envio = models.CharField(max_length=100, default="")
    activo = models.BooleanField(default=True)
    stock_descontado = models.BooleanField(default=False)

    class Meta:
        db_table = "pedido"

    def __str__(self):
        return self.numero_pedido


class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column="id_pedido",
        related_name="carrito",
    )
    id_producto = models.ForeignKey(
        ProductoTerminado,
        on_delete=models.RESTRICT,
        db_column="id_producto",
        related_name="carrito",
    )
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descuento_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )

    @property
    def subtotal(self):
        return (self.cantidad * self.precio_unitario) - (
            self.cantidad * self.descuento_unitario
        )

    class Meta:
        db_table = "carrito"
        constraints = [
            models.UniqueConstraint(
                fields=["id_pedido", "id_producto"], name="uq_carrito_pedido_producto"
            )
        ]

    def __str__(self):
        return f"{self.id_pedido} - {self.id_producto}"


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        db_column="id_pedido",
        related_name="venta",
    )
    fecha_venta = models.DateTimeField(default=timezone.now)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tipo_venta = models.CharField(
        max_length=20,
        choices=[
            ("online", "online"),
            ("presencial", "presencial"),
            ("whatsapp", "whatsapp"),
            ("instagram", "instagram"),
        ],
        default="online",
    )
    vendedor = models.CharField(max_length=100, default="")
    canal_venta = models.CharField(max_length=50, default="")
    observaciones = models.TextField(default="")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "venta"

    def __str__(self):
        return f"Venta {self.id_venta}"


class DetalleVenta(models.Model):
    id_detalle_venta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        db_column="id_venta",
        related_name="detalles",
    )
    id_producto = models.ForeignKey(
        ProductoTerminado,
        on_delete=models.RESTRICT,
        db_column="id_producto",
        related_name="detalles_venta",
    )
    cantidad = models.IntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descuento_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    @property
    def subtotal(self):
        return self.cantidad * (self.precio_unitario - self.descuento_unitario)

    @property
    def ganancia_bruta(self):
        return (self.precio_unitario - self.descuento_unitario) - self.costo_unitario

    @property
    def margen_porcentaje(self):
        if self.costo_unitario > 0:
            return (
                (self.precio_unitario - self.descuento_unitario - self.costo_unitario)
                / self.costo_unitario
                * 100
            )
        return 0

    class Meta:
        db_table = "detalle_venta"

    def __str__(self):
        return f"{self.id_venta} - {self.id_producto}"


class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column="id_pedido",
        related_name="pagos",
    )
    fecha_pago = models.DateTimeField(default=timezone.now)
    metodo_pago = models.CharField(
        max_length=20,
        choices=[
            ("efectivo", "efectivo"),
            ("transferencia", "transferencia"),
            ("paypal", "paypal"),
            ("tarjeta", "tarjeta"),
            ("datafono", "datafono"),
        ],
        default="efectivo",
    )
    referencia = models.CharField(max_length=100, default="")
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("confirmado", "confirmado"),
            ("pendiente", "pendiente"),
            ("fallido", "fallido"),
            ("reembolsado", "reembolsado"),
        ],
        default="pendiente",
    )
    comprobante_url = models.CharField(max_length=255, default="")
    observaciones = models.TextField(default="")

    class Meta:
        db_table = "pago"

    def __str__(self):
        return f"Pago {self.id_pago}"


class Envio(models.Model):
    id_envio = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column="id_pedido",
        related_name="envios",
    )
    direccion = models.TextField(default="")
    ciudad = models.CharField(max_length=50, default="")
    telefono_contacto = models.CharField(max_length=20, default="")
    tipo_envio = models.CharField(
        max_length=20,
        choices=[
            ("retiro", "retiro"),
            ("domicilio", "domicilio"),
            ("correo", "correo"),
            ("mensajeria", "mensajeria"),
        ],
        default="domicilio",
    )
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_envio = models.DateField(default=date.today)
    fecha_entrega_estimada = models.DateField(default=date.today)
    fecha_entrega_real = models.DateField(default=date.today)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "pendiente"),
            ("enviado", "enviado"),
            ("entregado", "entregado"),
            ("cancelado", "cancelado"),
            ("devuelto", "devuelto"),
        ],
        default="pendiente",
    )
    tracking_number = models.CharField(max_length=100, default="")
    observaciones = models.TextField(default="")

    class Meta:
        db_table = "envio"

    def __str__(self):
        return f"Envio {self.id_envio}"


class HistorialNavegacion(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column="id_usuario",
        related_name="historial_navegacion",
    )
    id_producto = models.ForeignKey(
        ProductoTerminado,
        on_delete=models.CASCADE,
        db_column="id_producto",
        related_name="historial_navegacion",
    )
    sesion_id = models.CharField(max_length=100, default="")
    fecha_visita = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "historial_navegacion"

    def __str__(self):
        return f"{self.id_usuario} - {self.id_producto}"
