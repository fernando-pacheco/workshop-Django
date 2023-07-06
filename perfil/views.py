from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta
from django.contrib import messages
from django.contrib.messages import constants


def home(request):
    return render(request,'home.html')

def gerenciar(request):
    contas = Conta.objects.all()
    total_conta = 0
    for conta in contas:
        total_conta += conta.valor
    return render(request,'gerenciar.html', {'contas':contas, 'total_conta':total_conta})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido = apelido,
        banco = banco,
        tipo = tipo,
        valor = valor,
        icone = icone,
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')
    return redirect('/perfil/gerenciar/')


def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()
    
    messages.add_message(request, constants.INFO, 'Conta removida com sucesso')
    return redirect('/perfil/gerenciar/')

