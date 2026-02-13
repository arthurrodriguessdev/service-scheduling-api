from django.urls import path
from clientes import views


urlpatterns = [
    path('clientes/', views.CriarListarClientes.as_view(), name='criar_listar_clientes'),
    path('clientes/<int:pk>/', views.DetalharAtualizarDeletarClientes.as_view(), name='detalhar_atualizar_deletar_clientes')
]