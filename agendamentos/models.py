from django.db import models
from django.contrib.auth.models import User
from servicos.models import Servico
from clientes.models import Cliente


class Agendamento(models.Model):
    AGENDAMENTO_CHOICES = [
        ('agendado', 'Agendado'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado')
    ]

    servico = models.ForeignKey(
        Servico, 
        on_delete=models.PROTECT, 
        related_name='agendamentos'
    )
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT, 
        related_name='agendamentos'
    )
    usuario = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='agendamentos'
    )

    status = models.CharField(choices=AGENDAMENTO_CHOICES, default='agendado')
    data = models.DateField(blank=False, null=False)
    hora_inicio = models.TimeField(blank=False, null=False)
    hora_fim = models.TimeField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.cliente.nome} - {self.servico.nome} ({self.data})'


