"""
config/settings_test.py — Configuración SOLO para la suite de tests.

Motivo:
  El cluster PostgreSQL local tiene el template1 con "collation version
  mismatch" (libc 2.39 vs 2.43), lo que impide clonar la BD de test.
  Para que la suite corra se sobreescribe DATABASES a SQLite (todos los
  modelos son portables: sin ArrayField/JSONField/HStoreField).
  No se usa en producción ni en dev: solo con `--settings=config.settings_test`.

  `python manage.py test core --settings=config.settings_test`
"""

from .settings import *  # noqa: F401,F403  — hereda TODO (JWT, DRF, permisos…)

# Reemplaza Postgres por SQLite en memoria para test (rápido y sin cluster).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST": {"NAME": ":memory:"},
    }
}

# La colación de SQLite no necesita REFRESH COLLATION VERSION.
