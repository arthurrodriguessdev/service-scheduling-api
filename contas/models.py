from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    email = models.CharField(
        unique=True,
        validators=[
            EmailValidator(message='O e-mail informado não é valido.')
        ]
    )
    nome = models.CharField(max_length=150)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nome} ({self.email})'
