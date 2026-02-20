from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from datetime import datetime as dt
from pagamentos.serializers import PagamentoSerializer
from pagamentos.models import Pagamento
from agendamentos.models import Agendamento
from utils.utils import filtrar_registros_usuario


class CriarListarPagamentos(generics.ListCreateAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(usuario=self.request.user)


class DetalharAtualizarDeletarPagamentos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return filtrar_registros_usuario(self.queryset, self.request.user)
        

class GerenciarPagamentos(viewsets.ViewSet):
    @action(methods=['post'], detail=False, url_path='pagar/agendamento/(?P<agendamento_pk>\d+)', url_name='pagar-agendamento')
    def pagar_agendamento(self, request, agendamento_pk):
        agendamento = get_object_or_404(Agendamento, pk=agendamento_pk)

        # Atualiza o status, hora do pagamento e atualiza o status do agendamento (vai para finalizado)
        try:
            pagamento_pendente = Pagamento.objects.get(
                status='pendente',
                agendamento=agendamento.pk
            )

            pagamento_pendente.pago_em=dt.now()
            pagamento_pendente.status = 'pago'
            agendamento.status = 'finalizado'
            pagamento_pendente.save()

        except:
            return Response({'message': 'Não foi encontrado pagamento pendente para esse agendamento'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'O agendamento foi pago com sucesso.'}, status=status.HTTP_200_OK)