from django.db import models
from agendamentos.models import Agendamento
from django.contrib.auth import get_user_model

User = get_user_model()


class Pagamento(models.Model):
    METODOS_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao', 'Cartão'),
        ('pix', 'Pix')
    ]

    STATUS_PAGAMENTO_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago')
    ]

    agendamento = models.ForeignKey(Agendamento, on_delete=models.PROTECT, related_name='pagamentos')
    metodo_pagamento = models.CharField(choices=METODOS_PAGAMENTO_CHOICES, default='pix')
    pago_em = models.DateTimeField(blank=True, null=True)
    valor = models.DecimalField(
        max_digits=11,
        decimal_places=2
    )
    status  = models.CharField(choices=STATUS_PAGAMENTO_CHOICES, default='pendente')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pagamentos')

    def __str__(self):
        return f'Pagamento: {self.agendamento}'