from django.shortcuts import render
from rest_framework import generics
from clientes.serializers import ClienteSerializer
from clientes.models import Cliente


class CriarListarClientes(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class DetalharAtualizarDeletarClientes(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer