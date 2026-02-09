from django.contrib import admin
from servicos.models import Servico


class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'preco')
    search_fields = ('nome', 'descricao')

admin.site.register(Servico, ServicoAdmin)
