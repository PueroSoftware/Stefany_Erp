from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet

# Router REST para /api/usuarios/ — solo usuarios con rol fabril pueden acceder.
router = DefaultRouter()
router.register("", UsuarioViewSet, basename="usuarios")

urlpatterns = router.urls
