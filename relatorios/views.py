from django.contrib.auth.models import User
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from pagamentos.models import Pagamento
from clientes.models import Cliente
from relatorios.serializers.clientes_ativos import ClientesAtivosSerializer
from relatorios.serializers.faturamento_mensal import FaturamentoMensalSerializer


class RelatoriosViewSet(viewsets.ViewSet):
    queryset = Cliente.objects.all()
    user_teste = User.objects.first()

    @action(detail=False, methods=['get'], url_path='clientes/ativos', url_name='list_total_clientes_ativos')
    def total_clientes_ativos(self, request):
        # usuario = request.user 

        # Setado APENAS para testes
        clientes_ativos = self.user_teste.clientes.filter(ativo=True)

        if not clientes_ativos.exists():
            return Response({'message': 'Não foram encontrados clientes ativos.'}, status.HTTP_400_BAD_REQUEST)
        
        lista_clientes = list()
        for cliente in clientes_ativos:
            lista_clientes.append({'nome_cliente': cliente.nome, 'id_cliente': cliente.pk})
        
        serializer = ClientesAtivosSerializer(lista_clientes, many=True)
        return Response(serializer.data)
    

    @action(detail=False, methods=['get'], url_path='faturamento/mensal', url_name='list_faturamento_mensal')
    def faturamento_mensal(self, request):
        agendamentos = self.user_teste.agendamentos.all()

        # faturamento_mensal > equivalente ao GRUPO relacionado por mes_ano
        faturamentos_mensais = Pagamento.objects.filter(
            agendamento__in = agendamentos,
            status = 'pendente'
        
        ).annotate(mes_ano=TruncMonth('agendamento__data')
        ).values('mes_ano').annotate(faturamento_mensal=Sum('valor')
        ).order_by('mes_ano')

        if not faturamentos_mensais.exists():
            return Response({'message': 'Não houve pagamentos finalizados em nenhum mês.'})

        serializer = FaturamentoMensalSerializer(faturamentos_mensais, many=True)
        return Response(serializer.data)