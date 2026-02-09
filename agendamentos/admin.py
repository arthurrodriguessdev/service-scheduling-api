from django.contrib import admin
from agendamentos.models import Agendamento


class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('hora_inicio', 'hora_fim')

admin.site.register(Agendamento, AgendamentoAdmin)
