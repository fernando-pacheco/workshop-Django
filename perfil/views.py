from django.shortcuts import render, redirect
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financeiro
from extrato.models import Valores
from datetime import datetime
from contas.views import context_ver_contas



def home(request):
    contas = Conta.objects.all()
    valores = Valores.objects.filter(data__month=datetime.now().month)
    entradas = valores.filter(tipo="E")
    saidas = valores.filter(tipo="S")

    total_entradas = calcula_total(entradas, 'valor')
    total_saidas = calcula_total(saidas, 'valor')
    total_gastos = total_saidas + total_entradas
    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro()  
    total_conta = calcula_total(contas,'valor')
    livre = total_conta - total_gastos

    retorno_ver_contas = context_ver_contas()
    contagem_proximas = retorno_ver_contas['contagem_proximas']
    contagem_contas_vencidas = retorno_ver_contas['contagem_contas_vencidas']

    return render(request,'home.html', {
        'contas':contas, 
        'total_conta':total_conta, 
        'total_entradas':total_entradas, 
        'total_saidas':total_saidas,
        'percentual_gastos_essenciais': round(percentual_gastos_essenciais), 
        'percentual_gastos_nao_essenciais': round(percentual_gastos_nao_essenciais),
        'total_gastos':total_gastos,
        'livre':livre,
        'contagem_proximas':contagem_proximas,
        'contagem_contas_vencidas':contagem_contas_vencidas,
        })

def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_conta = calcula_total(contas,'valor')
    return render(request,'gerenciar.html', {'contas':contas, 'total_conta':total_conta, 'categorias':categorias})


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')
    
    if not apelido.isascii():
        messages.add_message(request, constants.ERROR, 'Digite informações válidas nos campos abaixo')
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

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    if not nome.isalpha():
        messages.add_message(request, constants.ERROR, 'Digite informações válidas no campo da Categoria')
        return redirect('/perfil/gerenciar/')
        
    categoria = Categoria(
        categoria=nome.title(),
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')

def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar/')

def dashboard(request):
    dados = {}
    categorias = Categoria.objects.all()

    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)
        for v in valores:
            total += v.valor

        dados[categoria.categoria] = total

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})
