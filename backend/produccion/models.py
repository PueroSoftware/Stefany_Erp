from datetime import date
from django.utils import timezone
from django.db import models
from inventario.models import MateriaPrima


class Aroma(models.Model):
    id_aroma = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(default="")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "aroma"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Presentacion(models.Model):
    id_presentacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(default="")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "presentacion"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Color(models.Model):
    id_color = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "color"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class ProductoTerminado(models.Model):
    id_producto = models.AutoField(primary_key=True)
    codigo_producto = models.CharField(max_length=20, default="", unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default="")
    aroma = models.ForeignKey(
        Aroma,
        on_delete=models.RESTRICT,
        db_column="id_aroma",
        related_name="productos",
        null=True,
        blank=True,
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.RESTRICT,
        db_column="id_color",
        related_name="productos",
        null=True,
        blank=True,
    )
    peso = models.ForeignKey(
        Presentacion,
        on_delete=models.RESTRICT,
        db_column="id_presentacion",
        related_name="productos",
        null=True,
        blank=True,
    )
    tipo = models.CharField(
        max_length=20,
        choices=[
            ("jabon", "jabon"),
            ("kit", "kit"),
            ("promocion", "promocion"),
            ("muestra", "muestra"),
        ],
        default="jabon",
    )
    stock_disponible = models.IntegerField(default=0)
    stock_reservado = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=10)
    stock_maximo = models.IntegerField(default=100)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    calificacion_promedio = models.DecimalField(
        max_digits=3, decimal_places=2, default=0
    )
    total_resenas = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateField(default=date.today)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    @property
    def stock_total(self):
        return self.stock_disponible + self.stock_reservado

    @property
    def margen_ganancia(self):
        if self.precio_costo > 0:
            return (self.precio_venta - self.precio_costo) / self.precio_costo * 100
        return 0

    class Meta:
        db_table = "producto_terminado"

    def __str__(self):
        return self.nombre


class FormulaProducto(models.Model):
    id_formula = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        ProductoTerminado,
        on_delete=models.CASCADE,
        db_column="id_producto",
        related_name="formulas",
    )
    id_insumo = models.ForeignKey(
        MateriaPrima,
        on_delete=models.RESTRICT,
        db_column="id_insumo",
        related_name="formulas",
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=4)
    unidad = models.CharField(max_length=20, default="")
    orden = models.IntegerField(default=1)
    observaciones = models.TextField(default="")
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formula_producto"
        constraints = [
            models.UniqueConstraint(
                fields=["id_producto", "id_insumo"], name="uq_formula_producto_insumo"
            )
        ]

    def __str__(self):
        return f"{self.id_producto} - {self.id_insumo}"


class OrdenProduccion(models.Model):
    id_orden = models.AutoField(primary_key=True)
    numero_orden = models.CharField(max_length=20, default="", unique=True)
    id_producto = models.ForeignKey(
        ProductoTerminado,
        on_delete=models.CASCADE,
        db_column="id_producto",
        related_name="ordenes",
    )
    cantidad_producir = models.IntegerField()
    cantidad_producida = models.IntegerField(default=0)
    fecha_programada = models.DateField(default=date.today)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(default=timezone.now)
    estado = models.CharField(
        max_length=20,
        choices=[
            ("planificada", "planificada"),
            ("en_proceso", "en_proceso"),
            ("completada", "completada"),
            ("cancelada", "cancelada"),
            ("pausada", "pausada"),
        ],
        default="planificada",
    )
    prioridad = models.CharField(
        max_length=20,
        choices=[
            ("baja", "baja"),
            ("normal", "normal"),
            ("alta", "alta"),
            ("urgente", "urgente"),
        ],
        default="normal",
    )
    responsable = models.CharField(max_length=100, default="")
    observaciones = models.TextField(default="")
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "orden_produccion"

    def __str__(self):
        return self.numero_orden


class DetalleProduccion(models.Model):
    id_detalle_produccion = models.AutoField(primary_key=True)
    id_orden = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        db_column="id_orden",
        related_name="detalles",
    )
    id_insumo = models.ForeignKey(
        MateriaPrima,
        on_delete=models.RESTRICT,
        db_column="id_insumo",
        related_name="detalles_produccion",
    )
    cantidad_requerida = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    cantidad_usada = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    lote_usado = models.CharField(max_length=50, default="")
    costo_insumo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observaciones = models.TextField(default="")

    class Meta:
        db_table = "detalle_produccion"

    def __str__(self):
        return f"{self.id_orden} - {self.id_insumo}"


class FaseProduccion(models.Model):
    id_fase = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(default="")
    orden_secuencia = models.IntegerField(unique=True)
    tiempo_estimado_minutos = models.IntegerField(default=30)
    requiere_control_calidad = models.BooleanField(default=False)
    requiere_insumos_especificos = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "fase_produccion"

    def __str__(self):
        return self.nombre


class DetalleFaseProduccion(models.Model):
    id_detalle_fase = models.AutoField(primary_key=True)
    id_orden_produccion = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        db_column="id_orden_produccion",
        related_name="detalles_fase",
    )
    id_fase = models.ForeignKey(
        "FaseProduccion",
        on_delete=models.RESTRICT,
        db_column="id_fase",
        related_name="detalles_fase",
    )
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(default=timezone.now)
    responsable = models.CharField(max_length=100, default="")
    estado = models.CharField(
        max_length=20,
        choices=[
            ("pendiente", "pendiente"),
            ("en_proceso", "en_proceso"),
            ("completada", "completada"),
            ("pausada", "pausada"),
            ("cancelada", "cancelada"),
        ],
        default="pendiente",
    )
    observaciones = models.TextField(default="")
    tiempo_real_minutos = models.IntegerField(default=0)
    incidencias = models.TextField(default="")

    class Meta:
        db_table = "detalle_fase_produccion"

    def __str__(self):
        return f"{self.id_orden_produccion} - {self.id_fase}"


class MermaProduccion(models.Model):
    id_merma = models.AutoField(primary_key=True)
    id_orden_produccion = models.ForeignKey(
        OrdenProduccion,
        on_delete=models.CASCADE,
        db_column="id_orden_produccion",
        related_name="mermas",
    )
    id_insumo = models.ForeignKey(
        MateriaPrima,
        on_delete=models.RESTRICT,
        db_column="id_insumo",
        related_name="mermas_produccion",
        null=True,
        blank=True,
    )
    id_producto = models.ForeignKey(
        ProductoTerminado,
        on_delete=models.RESTRICT,
        db_column="id_producto",
        related_name="mermas_produccion",
        null=True,
        blank=True,
    )
    tipo_merma = models.CharField(
        max_length=30,
        choices=[
            ("insumo", "insumo"),
            ("producto", "producto"),
            ("material_empaque", "material_empaque"),
        ],
    )
    cantidad_perdida = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=20, default="")
    motivo = models.CharField(
        max_length=50,
        choices=[
            ("calidad", "calidad"),
            ("exceso", "exceso"),
            ("derrame", "derrame"),
            ("caducidad", "caducidad"),
            ("defecto", "defecto"),
            ("mal_manejo", "mal_manejo"),
        ],
    )
    valor_perdido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    porcentaje_perdida = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fecha_registro = models.DateTimeField(default=timezone.now)
    registrado_por = models.CharField(max_length=100, default="")
    observaciones = models.TextField(default="")

    class Meta:
        db_table = "merma_produccion"

    def __str__(self):
        return f"Merma {self.id_merma}"


class SeguimientoProduccion(models.Model):
    id_seguimiento = models.AutoField(primary_key=True)
    id_orden_produccion = models.OneToOneField(
        OrdenProduccion,
        on_delete=models.CASCADE,
        db_column="id_orden_produccion",
        related_name="seguimiento",
    )
    id_producto = models.ForeignKey(
        ProductoTerminado,
        on_delete=models.CASCADE,
        db_column="id_producto",
        related_name="seguimientos",
    )
    lote_produccion = models.CharField(max_length=50, default="")
    numero_orden = models.CharField(max_length=20, default="")
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin_estimada = models.DateTimeField(default=timezone.now)
    fecha_fin_real = models.DateTimeField(default=timezone.now)
    estado_actual = models.CharField(
        max_length=20,
        choices=[
            ("planificada", "planificada"),
            ("en_proceso", "en_proceso"),
            ("completada", "completada"),
            ("cancelada", "cancelada"),
            ("pausada", "pausada"),
        ],
        default="planificada",
    )
    fase_actual = models.CharField(max_length=50, default="")
    porcentaje_avance = models.IntegerField(default=0)
    responsable_actual = models.CharField(max_length=100, default="")
    observaciones_continuas = models.TextField(default="")
    tiempo_total_estimado_minutos = models.IntegerField(default=0)
    tiempo_total_real_minutos = models.IntegerField(default=0)
    eficiencia_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, default=0
    )
    cumplimiento_plazo = models.BooleanField(default=False)
    calidad_aprobada = models.BooleanField(default=False)
    fecha_control_calidad = models.DateTimeField(default=timezone.now)
    inspector_calidad = models.CharField(max_length=100, default="")
    observaciones_calidad = models.TextField(default="")

    class Meta:
        db_table = "seguimiento_produccion"

    def __str__(self):
        return f"Seguimiento {self.id_seguimiento}"
