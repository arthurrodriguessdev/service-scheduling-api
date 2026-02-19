from django.shortcuts import get_object_or_404
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from pagamentos.models import Pagamento
from clientes.models import Cliente
from servicos.models import Servico
from relatorios.serializers.clientes_ativos import ClientesAtivosSerializer
from relatorios.serializers.faturamento import FaturamentoMensalSerializer, FaturamentoServicoSerializer, FaturamentoMedioSerializer


class RelatoriosViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='clientes/ativos', url_name='list_total_clientes_ativos')
    def total_clientes_ativos(self, request):
        clientes_ativos = self.request.user.clientes.filter(ativo=True)

        if not clientes_ativos.exists():
            return Response({'message': 'Não foram encontrados clientes ativos.'}, status.HTTP_400_BAD_REQUEST)
        
        lista_clientes = list()
        for cliente in clientes_ativos:
            lista_clientes.append({'nome_cliente': cliente.nome, 'id_cliente': cliente.pk})
        
        serializer = ClientesAtivosSerializer(lista_clientes, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'], url_path='faturamento/mensal', url_name='list_faturamento_mensal')
    def faturamento_mensal(self, request):
        agendamentos = self.request.user.agendamentos.all()

        # faturamento_mensal > equivalente ao GRUPO relacionado por mes_ano
        faturamentos_mensais = Pagamento.objects.filter(
            agendamento__in = agendamentos,
            status = 'pago'
        
        ).annotate(mes_ano=TruncMonth('agendamento__data')
        ).values('mes_ano').annotate(faturamento_mensal=Sum('valor')
        ).order_by('mes_ano')

        if not faturamentos_mensais.exists():
            return Response({'message': 'Não houve pagamentos finalizados em nenhum mês.'})

        serializer = FaturamentoMensalSerializer(faturamentos_mensais, many=True)
        return Response(serializer.data)
    

    # Calcula e retorna o faturamento total por um serviço específico
    @action(detail=False, methods=['get'], url_path='faturamento/servico/(?P<servico_pk>\d+)', url_name='faturamento_servico')
    def faturamento_por_servico(self, request, servico_pk=None):
        servico = get_object_or_404(Servico, pk=servico_pk)

        agendamentos_servico = servico.agendamentos.all()
        if not agendamentos_servico.exists():
            return Response({'message': 'Não há registros de agendamentos para o serviço informado.'})
        
        faturamento_total = Pagamento.objects.filter(
            agendamento__in=agendamentos_servico,
            status='pago'
        ).aggregate(faturamento_total=Sum('agendamento__servico__preco'))


        serializer = FaturamentoServicoSerializer(faturamento_total, many=False)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'], url_path='faturamento/media', url_name='faturamento_medio')
    def faturamento_medio(self, request):
        pagamentos_feitos = Pagamento.objects.filter(
            usuario=self.request.user,
            status='pago'
        )

        if not pagamentos_feitos.exists():
            return Response({'message': 'Não há compras concluídas e pagas.'}, status.HTTP_400_BAD_REQUEST)
        
        quantidade_vendas = pagamentos_feitos.count()
        pagamentos_feitos = pagamentos_feitos.aggregate(valor_total=Sum('valor'))
        media = pagamentos_feitos['valor_total'] / quantidade_vendas

        serializer = FaturamentoMedioSerializer({'media_faturamento': media}, many=False)
        return Response(serializer.data)