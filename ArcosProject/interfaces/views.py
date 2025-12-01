from django.shortcuts import render, redirect
from .util import *
import re

# 1. Página de Login
def login_view(request):
    return render(request, 'login.html', {'title': 'Login'})

# 2. Dashboard: Minhas Operações de Consumo
def dashboard_view(request):
    return render(request, 'dashboard.html', {'title': 'Minhas Operações de Consumo'})

# 3. Cockpit de Apuração
def apuracao_view(request):
    return render(request, 'apuracao.html', {'title': 'Apuração Assistida'})

# 4. Modal/Página de Pagamento
def pagamento_view(request):
    return render(request, 'pagamento.html', {'title': 'Débitos para Pagamento'})


def cadastra_cnpj(request):
    # Verificamos se o método é POST (alguém clicou no botão)
    if request.method == 'POST':
        cnpj_raw = request.POST.get('cnpj')  # Pega o valor do input pelo 'name="cnpj"'

        # 1. Limpeza: Remove pontos, traços e barras, deixando só números
        cnpj_limpo = re.sub(r'\D', '', cnpj_raw)

        # Verificamos se tem tamanho mínimo (CNPJ tem 14 dígitos)
        if not cnpj_limpo:
            return render(request, 'login.html', {'title': 'Login', 'erro': 'CNPJ vazio'})

        try:
            # 2. Conversão: Sua função util espera um Inteiro
            cnpj_int = int(cnpj_limpo)

            # 3. Validação
            if valida_cnpj(cnpj_int):
                # Se válido, redireciona para o dashboard
                return redirect('dashboard')
            else:
                # Se inválido, volta pro login com aviso (você pode adicionar msg de erro no html depois)
                print("CNPJ Inválido")  # Apenas para debug no terminal
                return render(request, 'login.html', {'title': 'Login', 'error': 'CNPJ Inválido'})

        except ValueError:
            return render(request, 'login.html', {'title': 'Login'})

    # Se tentarem acessar /cadastro/ direto sem enviar formulário, manda pro login
    return redirect('login')

def enviar_receita(request):
    if request.method == 'POST':
        # VERIFICAÇÃO: O usuário já confirmou no modal?
        # Se o formulário enviado tiver o campo hidden 'confirmacao_final' == 'sim'
        if request.POST.get('confirmacao_final') == 'sim':
            # Lógica de negócio (salvar no banco, etc) iria aqui
            return redirect('pagamento') # Vai para pagamento.html

        # FASE 1: O usuário apenas clicou em "Enviar" na tela principal.
        # Renderizamos a página de apuração novamente, mas ativando o modal.
        return render(request, 'apuracao.html', {
            'title': 'Apuração Assistida',
            'exibir_modal_confirmacao': True # <--- Essa variável ativa a janela no HTML
        })

    # Se tentar acessar via GET, volta para o dashboard ou apuração limpa
    return redirect('apuracao')

# Informe a receita financeira dos ativos garantidores(provisões técnicas).