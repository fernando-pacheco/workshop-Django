from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request,'home.html')

def gerenciar(request):
    return render(request,'gerenciar.html')

def cadastrar_banco(request):
    return render(request,'cadastrar_banco.html')

