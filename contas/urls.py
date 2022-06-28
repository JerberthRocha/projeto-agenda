from django.urls import path
from . import views

urlpatterns = [
    path('', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
]