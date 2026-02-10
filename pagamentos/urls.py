from django.urls import path
from pagamentos import views


urlpatterns = [
    path('pagamentos/', views.CriarListarPagamentos.as_view(), name='criar_listar_pagamentos'),
    path('pagamentos/<int:pk>', views.DetalharAtualizarDeletarPagamentos.as_view(), name='detalhar_atualizar_deletar_pagamentos')
]