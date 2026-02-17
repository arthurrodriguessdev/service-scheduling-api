from rest_framework import serializers
from django.contrib.auth.models import User
from pagamentos.models import Pagamento


class PagamentoSerializer(serializers.ModelSerializer):
    valor_formatado = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pagamento 
        fields = '__all__'
        read_only_fields = ['usuario', 'pago_em', 'status']
    
    def validate(self, attrs):
        valor_cobrado = attrs.get('valor')
        agendamento = attrs.get('agendamento')

        # Se o agendamento já tiver um pagamento criado sem finalizar, retorna erro
        if Pagamento.objects.filter(agendamento=agendamento, status='pendente').exists():
            raise serializers.ValidationError(
                {'agendamento': 'Já existe um pagamento pendente criado para esse agendamento. Finalize ou cancele.'}
            )
        
        valor_servico = agendamento.servico.preco

        if not valor_cobrado == valor_servico:
            raise serializers.ValidationError(
                {'valor': 'O valor cobrado está diferente do preço do serviço agendado.'}
            )
        
        status_agendamento = agendamento.status
        if not status_agendamento == 'agendado':
            raise serializers.ValidationError(
                {'agendamento': 'O agendamento não pode ser pago porque está cancelado ou finalizado.'}
            )
        
        return attrs
    
    def get_valor_formatado(self, obj):
        return f'R${obj.valor}'
    
    def create(self, validated_data):
        user_teste = User.objects.first()
        validated_data['usuario'] = user_teste

        return super().create(validated_data)