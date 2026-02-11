from django.contrib import admin
from django.urls import path, include
from relatorios.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),

    # Versão 01 da API
    path('api/v1/', include('clientes.urls')),
    path('api/v1/', include('servicos.urls')),
    path('api/v1/', include('agendamentos.urls')),
    path('api/v1/', include('pagamentos.urls')),
    path('api/v1/relatorios/', include(router.urls))
]