from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ObjectStorageViewSet

# Router: genera /imagenes/ y /imagenes/{pk}/ automáticamente.
router = DefaultRouter()
router.register("imagenes", ObjectStorageViewSet, basename="storage-imagenes")

urlpatterns = router.urls