from rest_framework import serializers
from django.shortcuts import get_object_or_404
from servicos.models import Servico
from contas.models import Usuario


class SevicoSerializer(serializers.ModelSerializer):
    preco_formatado = serializers.SerializerMethodField(read_only=True)
    duracao_em_horas = serializers.SerializerMethodField(read_only=True)
    total_agendamentos_desse_servico = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Servico
        fields = '__all__'
        read_only_fields = ['usuario']

    def validate_preco(self, value):
        if not value > 0:
            raise serializers.ValidationError('O preço deve ser maior que R$0,00')
        return value
    
    def validate_duracao_minutos(self, value):
        if not value > 0:
            raise serializers.ValidationError('O serviço deve ter uma duração maior que zero minutos.')
        return value
    
    def validate_nome(self, value):
        usuario = get_object_or_404(Usuario, pk=self.context['request'].user.pk)
        queryset = usuario.servicos.filter(nome=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError('Já existe um serviço com esse nome vinculado ao usuário informado.')

        return value
    
    def get_preco_formatado(self, obj):
        return f'R${obj.preco}'
    
    def get_duracao_em_horas(self, obj):
        minutos = obj.duracao_minutos
        parte_hora = minutos // 60
        parte_minutos = minutos % 60
        
        return f'{parte_hora}h {parte_minutos}m'
    
    def get_total_agendamentos_desse_servico(self, obj):
        return obj.agendamentos.count()
    
    def create(self, validated_data):
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)