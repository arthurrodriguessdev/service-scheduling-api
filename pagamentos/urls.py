from django.urls import path
from rest_framework import routers
from rest_framework.routers import SimpleRouter
from pagamentos import views

router = SimpleRouter()
router.register('', views.GerenciarPagamentos, basename='pagamentos')


urlpatterns = [
    path('pagamentos/', views.CriarListarPagamentos.as_view(), name='criar_listar_pagamentos'),
    path('pagamentos/<int:pk>', views.DetalharAtualizarDeletarPagamentos.as_view(), name='detalhar_atualizar_deletar_pagamentos')
]