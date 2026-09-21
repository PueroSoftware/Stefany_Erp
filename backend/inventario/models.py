from django.db import models
from datetime import date


class CategoriaMateria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    tipo = models.CharField(
        max_length=20,
        choices=[
            ("base", "base"),
            ("aroma", "aroma"),
            ("color", "color"),
            ("aditivo", "aditivo"),
            ("molde", "molde"),
            ("empaque", "empaque"),
        ],
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "categoria_materia"
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "tipo"], name="uq_categoria_nombre_tipo"
            )
        ]

    def __str__(self):
        return self.nombre


class MateriaPrima(models.Model):
    id_insumo = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(
        CategoriaMateria,
        on_delete=models.RESTRICT,
        db_column="id_categoria",
        related_name="materias_primas",
    )
    nombre = models.CharField(max_length=100)
    unidad_medida = models.CharField(
        max_length=10,
        choices=[
            ("kg", "kg"),
            ("gr", "gr"),
            ("lt", "lt"),
            ("ml", "ml"),
            ("unidad", "unidad"),
        ],
    )
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_maximo = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    precio_promedio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observaciones = models.TextField()
    fecha_creacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "materia_prima"

    def __str__(self):
        return self.nombre


class StockMateriaPrima(models.Model):
    id_stock = models.AutoField(primary_key=True)
    id_insumo = models.ForeignKey(
        MateriaPrima,
        on_delete=models.RESTRICT,
        db_column="id_insumo",
        related_name="stocks",
    )
    lote = models.CharField(max_length=50)
    cantidad_disponible = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    cantidad_reservada = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def cantidad_total(self):
        return self.cantidad_disponible + self.cantidad_reservada

    fecha_entrada = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ubicacion = models.CharField(max_length=50, default="")
    estado = models.CharField(
        max_length=20,
        choices=[
            ("disponible", "disponible"),
            ("agotado", "agotado"),
            ("vencido", "vencido"),
            ("reservado", "reservado"),
        ],
        default="disponible",
    )
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "stock_materia_prima"  # apunta a la tabla de mi .SQL
        constraints = [
            models.UniqueConstraint(
                fields=["id_insumo", "lote"], name="uq_stock_insumo_lote"
            )
        ]

    def __str__(self):
        return f"{self.id_insumo}-{self.lote}"


class MermaStock(models.Model):
    id_merma_stock = models.AutoField(primary_key=True)
    id_insumo = models.ForeignKey(
        MateriaPrima,
        on_delete=models.RESTRICT,
        db_column="id_insumo",
        related_name="mermas_stock",
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    fecha_deteccion = models.DateField(auto_now_add=True)
    motivo = models.CharField(max_length=50, null=False)
    responsable = models.CharField(max_length=100)
    observaciones = models.TextField(default="")
    procesado = models.BooleanField(default=False)
    fecha_procesamiento = models.DateField(default=date.today)

    class Meta:
        db_table = "merma_stock"

    def __str__(self):
        return f"{self.id_insumo}-{self.fecha_deteccion}"


class MovimientoStock(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    id_insumo = models.ForeignKey(
        MateriaPrima,
        on_delete=models.RESTRICT,
        db_column="id_insumo",
        related_name="movimientos",
    )
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=[
            ("entrada", "entrada"),
            ("salida", "salida"),
            ("ajuste", "ajuste"),
            ("transferencia", "transferencia"),
        ],
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    stock_anterior = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_nuevo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(
        max_length=20,
        choices=[
            ("compra", "compra"),
            ("produccion", "produccion"),
            ("venta", "venta"),
            ("ajuste", "ajuste"),
            ("perdida", "perdida"),
            ("devolucion", "devolucion"),
            ("inicial", "inicial"),
            ("alerta", "alerta"),
        ],
    )
    referencia_id = models.IntegerField(default=0)
    referencia_tabla = models.CharField(max_length=50, default="")
    observaciones = models.TextField(default="")
    usuario_registro = models.CharField(max_length=100, default="")

    class Meta:
        db_table = "movimiento_stock"

    def __str__(self):
        return f"{self.tipo_movimiento} {self.cantidad}"
