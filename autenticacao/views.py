from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages, auth
from django.contrib.messages import constants
import re

# Create your views here.
def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirma_senha = request.POST.get('confirmar-senha')
        termos = request.POST.get('termos') == 'on'

        if Users.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, "Usuário já existe com esse nome!")
            redirect ('/accounts/cadastro')
        
        if senha != confirma_senha:
            messages.add_message(request, constants.ERROR, "As senhas não coincidem!")
            redirect ('/accounts/cadastro')

        if len(senha) < 8:
            messages.add_message(request, constants.ERROR, "A senha deve ter pelo menos 8 caracteres!")
            return redirect('/accounts/cadastro')

        if not re.search(r'[A-Z]', senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos uma letra maiúscula!")
            return redirect('/accounts/cadastro')

        if not re.search(r'[a-z]', senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos uma letra minúscula!")
            return redirect('/accounts/cadastro')

        if not re.search(r'[0-9]', senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos um número!")
            return redirect('/accounts/cadastro')
        
        if not termos:
            messages.add_message(request, constants.WARNING, "Você deve aceitar os Termos de Condições para se registrar")
            return redirect('/accounts/cadastro')

        if not any(char in '!@#$%&*.' for char in senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos um caractere especial (!@#$%&*)!")
            return redirect('/accounts/cadastro')

        if Users.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, "Já existe um usuário cadastrado nesse e-mail!")
            redirect ('/accounts/cadastro')

        try:
            user = Users.objects.create_user(username = username, email = email, password=senha)

            messages.add_message(request, constants.SUCCESS, "Cadastro realizado com sucesso!")
            return redirect('/accounts/login')

        except Exception as e:
            messages.add_message(request, constants.ERROR, f"Erro ao criar o usuário: {str(e)}")
            return redirect('/accounts/cadastro')
        
def login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')

    if request.method == 'GET':
        return render(request, 'login.html')
    
    else:
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = Users.objects.get(email=email)
        authenticated_user = auth.authenticate(request, username=user.username, password=senha)
        if authenticated_user:
            auth.login(request, authenticated_user)
            return redirect('/dashboard/')
            
        else:
            messages.add_message(request, constants.ERROR, 'E-mail ou senha inválidos!')
            print ()
            return redirect('/accounts/login')
        
def alterar_senha(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    
    if request.method == 'GET':
        return render(request, 'alterar-senha.html')
    
    else:
        email = request.POST.get('email')
        nova_senha = request.POST.get('nova-senha')
        confirma_senha = request.POST.get('confirmar-senha')
        termos = request.POST.get('termos') == 'on'
        
        if not Users.objects.filter(email=email).exists():
            messages.add_message(request, constants.ERROR, "Não existe esse e-mail cadastrado")
            redirect ('auth/alterar_senha')

        if nova_senha != confirma_senha:
            messages.add_message(request, constants.ERROR, "As senhas não coincidem!")
            redirect ('/accounts/alterar_senha')

        if len(nova_senha) < 8:
            messages.add_message(request, constants.ERROR, "A senha deve ter pelo menos 8 caracteres!")
            return redirect('/accounts/alterar_senha')

        if not re.search(r'[A-Z]', nova_senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos uma letra maiúscula!")
            return redirect('/accounts/alterar_senha')

        if not re.search(r'[a-z]', nova_senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos uma letra minúscula!")
            return redirect('/accounts/alterar_senha')

        if not re.search(r'[0-9]', nova_senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos um número!")
            return redirect('/accounts/alterar_senha')
        
        if not termos:
            messages.add_message(request, constants.WARNING, "Você deve aceitar os Termos de Condições para se registrar")
            return redirect('/accounts/alterar_senha')

        if not any(char in '!@#$%&*.' for char in nova_senha):
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos um caractere especial (!@#$%&*)!")
            return redirect('/accounts/alterar_senha')
            
        try:
            user = Users.objects.get(email=email)
            user.set_password(nova_senha)
            user.save()

            messages.add_message(request, constants.SUCCESS, "Senha alterada com sucesso!")
            return redirect('/accounts/login')

        except Exception as e:
            messages.add_message(request, constants.ERROR, f"Erro ao alterar a senha: {str(e)}")
            return redirect('/accounts/alterar_senha')

def sair(request):
    auth.logout(request)
    return redirect('/accounts/login')