from rest_framework import serializers
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
        usuario = self.context['request'].user

        # Não deixa um usuário criar pagamentos para agendamentos de outros
        if not usuario.agendamentos.filter(pk=agendamento.pk).exists():
            raise serializers.ValidationError(
                {'agendamento': 'Não é possível gerar pagamentos para agendamentos que não foram feitos pelo usuário logado.'}
            )

        # Se o agendamento já tiver um pagamento criado sem finalizar, retorna erro
        queryset = Pagamento.objects.filter(agendamento=agendamento, status='pendente')
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                {'agendamento': 'Já existe um pagamento pendente criado para esse agendamento. Finalize ou cancele primeiro.'}
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
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)