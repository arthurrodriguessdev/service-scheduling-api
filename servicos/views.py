from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from servicos.serializers import SevicoSerializer
from servicos.models import Servico
from utils.utils import filtrar_registros_usuario


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

    def get_queryset(self):
        return filtrar_registros_usuario(self.queryset, self.request.user)