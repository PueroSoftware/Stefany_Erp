from django.db import migrations


def actualizar_a_aroma(apps, schema_editor):
    """Renombra la categoria unica existente (Aceites/base) a aroma/aroma."""
    CategoriaMateria = apps.get_model("inventario", "CategoriaMateria")
    CategoriaMateria.objects.filter(id_categoria=1).update(nombre="aroma", tipo="aroma")


def revertir_a_aceites(apps, schema_editor):
    """Revierte al estado original (Aceites/base)."""
    CategoriaMateria = apps.get_model("inventario", "CategoriaMateria")
    CategoriaMateria.objects.filter(id_categoria=1).update(nombre="Aceites", tipo="base")


class Migration(migrations.Migration):

    dependencies = [
        ("inventario", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(actualizar_a_aroma, revertir_a_aceites),
    ]
