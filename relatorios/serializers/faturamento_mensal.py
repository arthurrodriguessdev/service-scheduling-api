from rest_framework import serializers
from pagamentos.models import Pagamento


class FaturamentoMensalSerializer(serializers.Serializer):
    mes_ano = serializers.DateField()
    faturamento_mensal = serializers.DecimalField(
        max_digits=11,
        decimal_places=2
    )


class FaturamentoServicoSerializer(serializers.Serializer):
    faturamento_total = serializers.DecimalField(
        max_digits=11,
        decimal_places=2
    )