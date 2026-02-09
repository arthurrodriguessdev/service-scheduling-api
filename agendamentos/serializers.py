from rest_framework import serializers
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from servicos.models import Servico
from agendamentos.models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    data_hoje = datetime.now().date()

    class Meta:
        model = Agendamento
        fields = '__all__'
    
    def calcular_hora_fim(self):
        servico = self.validated_data.get('servico')
        hora_inicio = self.validated_data.get('hora_inicio')
        data = self.validated_data.get('data')

        # Montando data e hora com a data e hora de início para calcular com timedelta
        data_hora = datetime.combine(data, hora_inicio)
        return (data_hora + timedelta(minutes=servico.duracao_minutos)).time()
    
    def validate_data(self, value):
        if value < self.data_hoje:
            raise serializers.ValidationError('A data informada já passou.')
        
        return value
    
    def validate_hora_inicio(self, value):
        data_agendamento = self.initial_data.get('data')
        data_hoje = datetime.strftime(self.data_hoje, "%Y-%m-%d")

        if data_agendamento == data_hoje:
            if value < datetime.now().time():
                raise serializers.ValidationError('O horário de início já passou.')
            
        return value

    def create(self, validated_data):
        validated_data['hora_fim'] = self.calcular_hora_fim()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.pk:
            instance.hora_fim = self.calcular_hora_fim()

        return super().update(instance, validated_data)
