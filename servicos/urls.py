from django.urls import path
from servicos import views


urlpatterns = [
    path('servicos/', views.CriarListarServicos.as_view(), name='criar_listar_servicos'),
    path('servicos/<int:pk>/', views.DetalharAtualizarDeletarServicos.as_view(), name='detalhar_atualizar_deletar_servicos')
]