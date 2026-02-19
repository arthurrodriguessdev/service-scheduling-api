from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from clientes.serializers import ClienteSerializer
from clientes.models import Cliente


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