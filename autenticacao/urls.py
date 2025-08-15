from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name="cadastro"),
    path('login/', views.login, name="login"),
    path('alterar_senha/', views.alterar_senha, name="alterar_senha"),
    path('sair/', views.sair, name="sair"),
]