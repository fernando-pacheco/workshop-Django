from django.shortcuts import render, redirect
from perfil.models import Conta, Categoria

def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})