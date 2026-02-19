from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from servicos.serializers import SevicoSerializer
from servicos.models import Servico


class CriarListarServicos(generics.ListCreateAPIView):
    queryset = Servico.objects.all()
    serializer_class = SevicoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)


class DetalharAtualizarDeletarServicos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Servico.objects.all()
    serializer_class = SevicoSerializer
    permission_classes = (IsAuthenticated,)
