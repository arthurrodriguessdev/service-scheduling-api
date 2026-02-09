from django.urls import path
from agendamentos import views


urlpatterns = [
    path('agendamentos/', views.CriarListarAgendamentos.as_view(), name='criar_listar_agendamentos'),
    path('agendamentos/<int:pk>/', views.DetalharAtualizarDeletarAgendamentos.as_view(), name='detalhar_atualizar_deletar_agendamentos')
]