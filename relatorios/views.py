from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from pagamentos.models import Pagamento
from clientes.models import Cliente
from relatorios.serializers.clientes_ativos import ClientesAtivosSerializer


class RelatoriosViewSet(viewsets.ViewSet):
    queryset = Cliente.objects.all()

    @action(detail=False, methods=['get'])
    def total_clientes_ativos(self, request):
        # usuario = request.user 

        user_teste = User.objects.first() # Setado APENAS para testes
        clientes_ativos = user_teste.clientes.filter(ativo=True)

        if not clientes_ativos:
            return Response({'message': 'Não foram encontrados clientes ativos.'}, status.HTTP_400_BAD_REQUEST)
        
        lista_clientes = list()
        for cliente in clientes_ativos:
            lista_clientes.append({'nome_cliente': cliente.nome, 'id_cliente': cliente.pk})
        
        serializer = ClientesAtivosSerializer(lista_clientes, many=True)
        return Response(serializer.data)