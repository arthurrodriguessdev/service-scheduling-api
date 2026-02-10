from django.urls import path
from relatorios import views


urlpatterns = [
    path('relatorios/faturamento_mensal/', views.FaturamentoMensal.as_view(), name='listar_faturamento_mensal'),
]