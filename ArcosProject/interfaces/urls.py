from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('apuracao/', views.apuracao_view, name='apuracao'),
    path('pagamento/', views.pagamento_view, name='pagamento'),
    path('cadastro/', views.cadastra_cnpj, name='cadastro'),
    path('enviar_receita/', views.enviar_receita, name='receita'),
    path('operacoes/', views.operacoes_view, name='operacoes')
]