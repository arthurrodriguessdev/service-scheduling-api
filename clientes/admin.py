from django.contrib import admin
from clientes.models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'telefone')
    search_fields = ('nome', 'email')

admin.site.register(Cliente, ClienteAdmin)