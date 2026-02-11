from rest_framework import serializers
from pagamentos.models import Pagamento


class ClientesAtivosSerializer(serializers.Serializer):
    nome_cliente = serializers.CharField()
    id_cliente = serializers.IntegerField()