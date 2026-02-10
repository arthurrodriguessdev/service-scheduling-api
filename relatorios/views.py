from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from pagamentos.models import Pagamento
from relatorios.serializers.faturamento_mensal import FaturamentoMensalSerializer


class FaturamentoMensal(generics.ListAPIView):
    serializer_class = FaturamentoMensalSerializer

    def get_queryset(self):
        ...
        return super().get_queryset()