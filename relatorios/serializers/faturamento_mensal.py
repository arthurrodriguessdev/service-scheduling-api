from rest_framework import serializers
from pagamentos.models import Pagamento


class FaturamentoMensalSerializer(serializers.Serializer):
    mes_ano = serializers.CharField()
    total = serializers.DecimalField(max_digits=11, decimal_places=2)