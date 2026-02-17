from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from agendamentos.serializers import AgendamentoSerializer
from agendamentos.models import Agendamento


class CriarListarAgendamentos(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = (IsAuthenticated,)


class DetalharAtualizarDeletarAgendamentos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = (IsAuthenticated,)
