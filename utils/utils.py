# Funções genéricas e úteis que podem ser utilizadas por qualquer entidade da aplicação

def filtrar_registros_usuario(queryset, usuario):
    return queryset.filter(usuario=usuario)