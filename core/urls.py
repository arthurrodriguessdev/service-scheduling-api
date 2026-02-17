from django.contrib import admin
from django.urls import path, include
from relatorios.urls import router as router_relatorios
from pagamentos.urls import router as router_pagamentos


urlpatterns = [
    path('admin/', admin.site.urls),

    # Versão 01 da API
    path('api/v1/', include('clientes.urls')),
    path('api/v1/', include('servicos.urls')),
    path('api/v1/', include('agendamentos.urls')),
    path('api/v1/', include('pagamentos.urls')),
    path('api/v1/', include('autenticacao.urls')),
    path('api/v1/relatorios/', include(router_relatorios.urls)),
    path('api/v1/pagamentos/', include(router_pagamentos.urls))
]