from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from servicos.models import Servico
from agendamentos.models import Agendamento

User = get_user_model()

class AgendamentoSerializer(serializers.ModelSerializer):
    duracao = serializers.SerializerMethodField(read_only=True)
    preco_total = serializers.SerializerMethodField(read_only=True)
    eh_futuro = serializers.SerializerMethodField(read_only=True)
    eh_hoje = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Agendamento
        fields = '__all__'
        read_only_fields = ['hora_fim', 'usuario', 'status']
    
    data_hoje = datetime.now().today()
    
    def validate(self, attrs):
        servico = attrs.get('servico')
        cliente = attrs.get('cliente')
        data_agendamento = attrs.get('data')
        hora_inicio = attrs.get('hora_inicio')

        user_test = self.context['request'].user

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
        
        # A hora final é a hora inicial + tempo de duração do serviço
        validated_data['hora_fim'] = (datetime.combine(data, hora_inicio) + timedelta(minutes=servico.duracao_minutos)).time()
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        servico = validated_data.get('servico', instance.servico)
        data = validated_data.get('data', instance.data)
        hora_inicio = validated_data.get('hora_inicio', instance.hora_inicio)

        instance.hora_fim = (datetime.combine(data, hora_inicio) + timedelta(minutes=servico.duracao_minutos)).time()
        return super().update(instance, validated_data)
    
    def get_duracao(self, obj):
        data_hoje_hora_inicio = datetime.combine(self.data_hoje.date(), obj.hora_inicio)
        data_hoje_hora_fim = datetime.combine(self.data_hoje.date(), obj.hora_fim)

        # data_hoje_hora_fim recebe o combine today + 1 dia para regulatizar o cálculo
        if obj.hora_inicio > obj.hora_fim:
            data_hoje_hora_fim = datetime.combine(self.data_hoje.date() + timedelta(days=1), obj.hora_fim)

        duracao = str(data_hoje_hora_fim - data_hoje_hora_inicio)
        horas_pm = list()
        
        contador = 10
        while contador <= 23:
            horas_pm.append(str(contador))
            contador += 1
        
        hora = duracao[0]
        minutos = duracao[2:4]

        # Se a hora tiver mais de 2 dígitos, pega uma parte mais adiantada da string
        if duracao[0] in horas_pm or duracao[0:2] in horas_pm:
            hora = duracao[0:2]
            minutos = duracao[3:5]
        
        return f'{hora}h {minutos}m'
    
    def get_preco_total(self, obj):
        return f'R${obj.servico.preco}'
    
    def get_eh_futuro(self, obj):
        if obj.data > self.data_hoje.date():
            return True
    
        return False
    
    def get_eh_hoje(self, obj):
        if obj.data == self.data_hoje.date():
            return True
        
        return False