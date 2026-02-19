from django.urls import path
from rest_framework.routers import SimpleRouter
from contas import views

router = SimpleRouter()
router.register('', views.GerenciarContasAPI, basename='contas')