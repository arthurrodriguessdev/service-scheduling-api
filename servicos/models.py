from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Servico(models.Model):
    nome = models.CharField(max_length=80, blank=False, null=False, verbose_name='Nome do serviço')
    descricao = models.TextField(verbose_name='Descrição do serviço')
    preco = models.DecimalField(
        verbose_name='Preço do serviço',
        decimal_places=2,
        max_digits=11,
        null=False,
        blank=False
    )

    duracao_minutos = models.IntegerField(verbose_name='Duração em minutos')
    esta_ativo = models.BooleanField(verbose_name='Esse serviço está ativo?')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='servicos')

    def __str__(self):
        return f'{self.nome} ({self.duracao_minutos})'
