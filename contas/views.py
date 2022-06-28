import re
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormularioContato

# Create your views here.
def entrar(request):
    if request.method != 'POST':
        return render(request, 'contas/entrar.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'contas/entrar.html')
    else:
        auth.login(request, user)
        return redirect('dashboard')

def sair(request):
    auth.logout(request)
    return redirect('index')

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'contas/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    confirmacao_senha = request.POST.get('confirmacao_senha')

    if not nome or not sobrenome or not email or not usuario or not senha \
       or not confirmacao_senha:
       messages.error(request, 'Todos os campos são obrigatórios.')
       return render(request, 'contas/cadastro.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido.')
        return render(request, 'contas/cadastro.html')

    if len(senha) < 6:
       messages.error(request, 'Senha precisa ter no mínimo 6 caracteres.')
       return render(request, 'contas/cadastro.html')
    
    if senha != confirmacao_senha:
        messages.error(request, 'Senhas não conferem.')
        return render(request, 'contas/cadastro.html')
    
    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'contas/cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já existe.')
        return render(request, 'contas/cadastro.html')

    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()

    messages.success(request, 'Cadastrado com sucesso!')

    return redirect('entrar')

@login_required(login_url='entrar')
def dashboard(request):
    if request.method != 'POST':
        formulario = FormularioContato()
        return render(request, 'contas/dashboard.html', {'formulario': formulario})
    
    formulario = FormularioContato(request.POST, request.FILES) 

    if not formulario.is_valid():
        messages.error(request, 'Erro ao enviar formulário.')
        formulario = FormularioContato(request.POST)
        return render(request, 'contas/dashboard.html', {'formulario': formulario})
    
    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'O campo descrição precisa ter mais que 5 caracteres')
        formulario = FormularioContato(request.POST)
        return render(request, 'contas/dashboard.html', {'formulario': formulario})

    formulario.save()
    messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso!')
    return redirect('dashboard')