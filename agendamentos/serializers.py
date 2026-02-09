from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from servicos.models import Servico
from agendamentos.models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    '''duracao = serializers.SerializerMethodField(read_only=True)
    preco_total = serializers.SerializerMethodField(read_only=True)
    eh_futuro = serializers.SerializerMethodField(read_only=True)
    eh_hoje = serializers.SerializerMethodField(read_only=True)'''

    class Meta:
        model = Agendamento
        fields = '__all__'
        read_only_fields = ['hora_fim', 'usuario', 'status']
    
    def validate(self, attrs):
        servico = attrs.get('servico')
        cliente = attrs.get('cliente')
        data_agendamento = attrs.get('data')
        hora_inicio = attrs.get('hora_inicio')
        usuario = self.context['request'].user

        user_test = User.objects.first()

        if not all([servico, cliente, data_agendamento, hora_inicio]):
            return attrs

        if not servico.usuario.id == cliente.usuario.id:
            raise serializers.ValidationError('O serviço e o cliente devem pertencer ao mesmo usuário.')
        
        hora_fim = (datetime.combine(data_agendamento, hora_inicio) + timedelta(minutes=servico.duracao_minutos)).time()
        conflitos = user_test.agendamentos.filter(
            status='agendado', 
            data=data_agendamento,
            hora_inicio__lte=hora_fim,
            hora_fim__gte=hora_inicio
        )
        
        if self.instance:
            conflitos = conflitos.exclude(pk=self.instance.pk)
        
        if conflitos:
            raise serializers.ValidationError({'hora_inicio': 'A empresa já possui um agendamento nesse horário.'})
        
        return attrs
    
    def validate_data(self, value):
        if value < datetime.now().date():
            raise serializers.ValidationError('A data informada já passou.')
        
        return value

    def create(self, validated_data):
        servico = validated_data['servico']
        hora_inicio = validated_data['hora_inicio']
        data = validated_data['data']

        user_test = User.objects.first()
        
        # A hora final é a hora inicial + tempo de duração do serviço
        validated_data['hora_fim'] = (datetime.combine(data, hora_inicio) + timedelta(minutes=servico.duracao_minutos)).time()
        validated_data['usuario'] = user_test
        return super().create(validated_data)

    def update(self, instance, validated_data):
        servico = validated_data.get('servico', instance.servico)
        data = validated_data.get('data', instance.data)
        hora_inicio = validated_data.get('hora_inicio', instance.hora_inicio)

        instance.hora_fim = (datetime.combine(data, hora_inicio) + timedelta(minutes=servico.duracao_minutos)).time()
        return super().update(instance, validated_data)