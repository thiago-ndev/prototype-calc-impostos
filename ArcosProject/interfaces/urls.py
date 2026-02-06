from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login_cnpj', views.login_cnpj_view, name='login-cnpj'),
    path('apuracao/', views.apuracao_view, name='apuracao'),
    path('pagamento/', views.pagamento_view, name='pagamento'),
    path('cadastro/', views.cadastra_cnpj, name='cadastro'),
    path('enviar_receita/', views.enviar_receita, name='receita'),
    path('operacoes/', views.operacoes_view, name='operacoes'),
    path('portal/', views.portal_view, name='portal'),
    path('home/', views.home_view, name='home'),
    path('captura/', views.captura_view, name='captura'),
    path('notas/', views.notas_fiscais, name='notas'),

    path('dere/', views.dere_view, name='dere'),
    path('captura_balancete/', views.captura_balancete_view, name='captura-balancete'),
    path('captura_apolices/', views.captura_apolices_view, name='captura-apolices'),
]