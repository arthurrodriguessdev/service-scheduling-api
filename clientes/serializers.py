from rest_framework import serializers
from datetime import datetime
import re
from clientes.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    '''total_agendamentos = serializers.SerializerMethodField(read_only=True)
    total_gasto = serializers.SerializerMethodField(read_only=True)
    data_ultimo_agendamento = serializers.SerializerMethodField(read_only=True)'''

    class Meta:
        model = Cliente
        fields = '__all__'
    
    def validate_email(self, value):
        email_informado = value
        queryset =  Cliente.objects.filter(email=email_informado)

        if self.instance:
            queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError('Já existe um cliente cadastrado com esse e-mail.')
        return value
    
    def validate_data_nascimento(self, value):
        data_hoje = datetime.now().date()
        data_minima_nascimento =data_hoje.replace(year=data_hoje.year - 18)

        if value.year < 1900 or value.year > datetime.now().year:
            raise serializers.ValidationError('Data de nascimento inválida.')
        
        if value > data_minima_nascimento:
            raise serializers.ValidationError('Data de nascimento inválida. É preciso ter, no mínimo, 18 anos.')
        
        return value
    
    def validate_telefone(self, value):
        padrao_aceito_telefone = re.compile(r'^\d+$')

        if not padrao_aceito_telefone.fullmatch(value):
            raise serializers.ValidationError('O número de telefone não está no padrão correto. Padrão aceito: DDDNXXXXXXXX')
        
        return value
    
