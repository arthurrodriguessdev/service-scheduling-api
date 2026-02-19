from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from agendamentos.serializers import AgendamentoSerializer
from agendamentos.models import Agendamento
from utils.utils import pode_executar_acoes


class CriarListarAgendamentos(generics.ListCreateAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)


class DetalharAtualizarDeletarAgendamentos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        queryset = request.user.agendamentos
        if not pode_executar_acoes(queryset, kwargs['pk']):
            return Response(
                {'message': 'O agendamento que deseja obter detalhes não pertence ao usuário logado ou não existe.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        queryset = request.user.agendamentos
        if not pode_executar_acoes(queryset, kwargs['pk']):
            return Response(
                {'message': 'O agendamento que deseja editar não pertence ao usuário logado ou não existe.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        queryset = request.user.agendamentos
        if not pode_executar_acoes(queryset, kwargs['pk']):
            return Response(
                {'message': 'O agendamento que deseja excluir não pertence ao usuário logado ou não existe.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
