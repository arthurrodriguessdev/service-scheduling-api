from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Cliente(models.Model):
    nome = models.CharField(max_length=120, null=False, blank=False)
    email = models.EmailField()
    telefone = models.CharField(
        validators=[
            MinLengthValidator(10, message='O telefone deve ter 10 ou 11 dígitos.'),
            MaxLengthValidator(11, message='O telefone deve ter 10 ou 11 dígitos.')
        ],
        null=False, 
        blank=False
    )
    
    data_nascimento = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='clientes', verbose_name='Usuário')
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome