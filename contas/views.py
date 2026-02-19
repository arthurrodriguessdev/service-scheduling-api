from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
import json
from contas.models import Usuario


class GerenciarContasAPI(viewsets.ViewSet):
    def create(self, request):
        try:
            dados = json.loads(request.body.decode('utf-8'))
        except:
            return Response({'message': 'Essa requisição exige alguns parâmetros. (username, nome, email, password)'}, status=status.HTTP_400_BAD_REQUEST)
        
        parametros_obrigatorios = ['username', 'nome', 'email', 'password']
        parametros_enviados = [chave for chave in dados.keys()]

        # Laço verifica se todos as chaves foram enviadas pelo usuário
        for parametro_obrigatorio in parametros_obrigatorios:
            if parametro_obrigatorio not in parametros_enviados:
                return Response({'message': f'Parâmetro obrigatório "{parametro_obrigatorio}" está faltando.'}, status=status.HTTP_400_BAD_REQUEST)
        
        usuario = Usuario(
            nome=dados['nome'],
            username=dados['username'], 
            email=dados['email']
        )
        usuario.set_password(dados['password'])

        # Executa as validações do modelo
        try:
            usuario.full_clean()
        except ValidationError as error:
            return Response({'message': f'Ocorreu um erro: {error}'}, status=status.HTTP_400_BAD_REQUEST)
        
        usuario.save()
        return Response({'message': 'Conta registrada com sucesso.'}, status=status.HTTP_201_CREATED)