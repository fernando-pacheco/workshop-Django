from django.urls import path
from . import views
from perfil.models import Conta, Categoria


urlpatterns = [
    path('definir_planejamento/', views.definir_planejamento, name="definir_planejamento"),
]