from django.shortcuts import render
from rest_framework import generics
from servicos.serializers import SevicoSerializer
from servicos.models import Servico


class CriarListarServicos(generics.ListCreateAPIView):
    queryset = Servico.objects.all()
    serializer_class = SevicoSerializer


class DetalharAtualizarDeletarServicos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servico.objects.all()
    serializer_class = SevicoSerializer
