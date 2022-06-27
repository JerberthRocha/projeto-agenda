import re
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
def entrar(request):
    return render(request, 'contas/entrar.html')

def sair(request):
    return render(request, 'contas/sair.html')

def cadastro(request):
    print(request.POST)
    # messages.add_message(
    #         request, 
    #         messages.SUCCESS,
    #         'Usuário cadastrado com sucesso.'
    #     )
    return render(request, 'contas/cadastro.html')

def dashboard(request):
    return render(request, 'contas/dashboard.html')

