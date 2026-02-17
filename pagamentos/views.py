from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime as dt
from pagamentos.serializers import PagamentoSerializer
from pagamentos.models import Pagamento
from agendamentos.models import Agendamento


class CriarListarPagamentos(generics.ListCreateAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer


class DetalharAtualizarDeletarPagamentos(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer


class GerenciarPagamentos(viewsets.ViewSet):
    @action(methods=['post'], detail=False, url_path='pagar/agendamento/(?P<agendamento_pk>\d+)', url_name='pagar-agendamento')
    def pagar_agendamento(self, request, agendamento_pk):
        agendamento = get_object_or_404(Agendamento, pk=agendamento_pk)

        # Atualiza o status e a hora do pagamento
        try:
            pagamento_pendente = Pagamento.objects.get(
                status='pendente',
                agendamento=agendamento.pk
            )

            pagamento_pendente.pago_em=dt.now()
            pagamento_pendente.status = 'pago'
            pagamento_pendente.save()

        except:
            return Response({'message': 'Não foi encontrado pagamento pendente para esse agendamento'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'O agendamento foi pago com sucesso.'}, status=status.HTTP_200_OK)