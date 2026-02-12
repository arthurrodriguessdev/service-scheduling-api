from django.urls import path
from rest_framework.routers import SimpleRouter
from relatorios import views

router = SimpleRouter()
router.register('', views.RelatoriosViewSet, basename='relatorios')