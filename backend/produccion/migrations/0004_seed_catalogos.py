from django.db import migrations

AROMAS = [
    "lavanda", "limon", "canela", "coco", "vainilla", "pino_silvestre",
    "manzanilla", "romero", "rosa", "maracuya", "naranja", "floral",
    "manzana", "invictus", "dolce_gabanna", "jockey_club", "arroz",
    "avena", "carbon_activo", "matico", "lumbre",
]
PRESENTACIONES = [
    "100g", "75g", "50g",
    "kit_animalito_75g", "kit_piecito_60gr", "kit_huellita_75g",
]
COLORES = [
    "rosado_princesa", "oro_viejo", "rojo_navidad", "rojo_bandera",
    "rojo_num40", "verde_navidad", "verde_manzana", "verde_menta_vegetal",
    "green_num12", "azul_uva_vegetal", "violeta", "celeste", "negro",
    "amarillo5_vegetal", "anaranjado_vegetal",
]


def sembrar(apps, schema_editor):
    """Puebla los catalogos con los valores que antes eran listas fijas."""
    Aroma = apps.get_model("produccion", "Aroma")
    Presentacion = apps.get_model("produccion", "Presentacion")
    Color = apps.get_model("produccion", "Color")
    Aroma.objects.bulk_create([Aroma(nombre=n) for n in AROMAS], ignore_conflicts=True)
    Presentacion.objects.bulk_create(
        [Presentacion(nombre=n) for n in PRESENTACIONES], ignore_conflicts=True
    )
    Color.objects.bulk_create([Color(nombre=n) for n in COLORES], ignore_conflicts=True)


def revertir(apps, schema_editor):
    """Elimina solo los valores sembrados (reversible)."""
    Aroma = apps.get_model("produccion", "Aroma")
    Presentacion = apps.get_model("produccion", "Presentacion")
    Color = apps.get_model("produccion", "Color")
    Aroma.objects.filter(nombre__in=AROMAS).delete()
    Presentacion.objects.filter(nombre__in=PRESENTACIONES).delete()
    Color.objects.filter(nombre__in=COLORES).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("produccion", "0003_aroma_color_presentacion_and_more"),
    ]

    operations = [
        migrations.RunPython(sembrar, revertir),
    ]
