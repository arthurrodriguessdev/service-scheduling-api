# Funções genéricas e úteis que podem ser utilizadas por qualquer entidade da aplicação

def pode_executar_acoes(queryset, pk):
    try:
        obj = queryset.get(pk=pk)
        return obj
    except:
        return False