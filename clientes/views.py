from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from clientes.serializers import ClienteSerializer
from clientes.models import Cliente
from utils.utils import filtrar_registros_usuario


class CriarListarClientes(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)

class DetalharAtualizarDeletarClientes(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return filtrar_registros_usuario(self.queryset, self.request.user)
    