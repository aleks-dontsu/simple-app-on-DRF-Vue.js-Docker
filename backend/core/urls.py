from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import CarViewSet

router = DefaultRouter()
router.register('cars', CarViewSet)

urlpatterns = router.urls
