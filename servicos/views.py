from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from servicos.serializers import SevicoSerializer
from servicos.models import Servico
from utils.utils import pode_executar_acoes


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

    def update(self, request, *args, **kwargs):
        queryset = request.user.servicos
        if not pode_executar_acoes(queryset, kwargs['pk']):
            return Response(
                {'message': 'O serviço que deseja editar não pertence ao usuário logado ou não existe.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        queryset = request.user.servicos
        if not pode_executar_acoes(queryset, kwargs['pk']):
            return Response(
                {'message': 'O serviço que deseja detalhar não pertence ao usuário logado ou não existe.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().retrieve(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        queryset = request.user.servicos
        if not pode_executar_acoes(queryset, kwargs['pk']):
            return Response(
                {'message': 'O serviço que deseja deletar não pertence ao usuário logado ou não existe.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().destroy(request, *args, **kwargs)
