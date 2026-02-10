from django.shortcuts import render
from rest_framework import generics
from pagamentos.serializers import PagamentoSerializer
from pagamentos.models import Pagamento


class CriarListarPagamentos(generics.ListCreateAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer


class DetalharAtualizarDeletarPagamentos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer