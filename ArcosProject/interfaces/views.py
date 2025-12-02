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

# 5. Página Marota
def operacoes_view(request):
    return render(request, 'operacoes.html', {'title': 'Minhas Operações de Consumo Atualizadas'})

# 4. Modal/Página de Pagamento
def pagamento_view(request):
    # 1. Recupera o valor da sessão. Se não tiver (acesso direto), assume 0.
    iva_total = float(request.session.get('iva_a_pagar', 0))

    # 2. Faz os cálculos das porcentagens
    # Documentos Fiscais: 1001 (20%), 1002 (13%), 1003 (35%), 1004 (17%), 1005 (15%)
    # Soma das porcentagens = 100%

    contexto = {
        'title': 'Débitos para Pagamento',
        'valor_total_pagar': formatar_brl(iva_total),
        # Calculando e formatando cada item
        'doc_1001': formatar_brl(iva_total * 0.20),
        'doc_1002': formatar_brl(iva_total * 0.13),
        'doc_1003': formatar_brl(iva_total * 0.35),
        'doc_1004': formatar_brl(iva_total * 0.17),
        'doc_1005': formatar_brl(iva_total * 0.15),
    }

    return render(request, 'pagamento.html', contexto)


def cadastra_cnpj(request):
    # Verificamos se alguém clicou no botão (se é POST)
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
        # CASO 2: O usuário clicou em "Sim, confirmar" no Modal
        if request.POST.get('confirmacao_final') == 'sim':
            # Recuperamos o valor calculado que passamos via hidden input
            iva_final = request.POST.get('iva_pagar_final')

            # SALVAMOS NA SESSÃO (Memória temporária do navegador/servidor)
            request.session['iva_a_pagar'] = iva_final

            return redirect('pagamento')

        # CASO 1: O usuário clicou em "Enviar" na tela principal (Vem com a alíquota)
        aliquota = request.POST.get('aliquota_envio')

        # Recalculamos aqui no Python para ter segurança dos dados
        try:
            base_calculo = 560000.00
            total_creditos = 15000.00
            aliq_float = float(aliquota) if aliquota else 0

            total_debitos = base_calculo * (aliq_float / 100)
            iva_pagar = total_debitos - total_creditos
        except ValueError:
            iva_pagar = 0.0

        # Renderiza a mesma página, mas agora com o Modal ativado e os valores pré-carregados
        return render(request, 'apuracao.html', {
            'title': 'Apuração Assistida',
            'exibir_modal_confirmacao': True,
            'iva_calculado': iva_pagar,  # Envia o valor bruto (float) para o formulário oculto
            'iva_formatado': formatar_brl(iva_pagar),  # Envia formatado para exibir no texto
            'aliquota_informada': aliquota  # Devolve a alíquota para o input não ficar vazio
        })

    return redirect('apuracao')

# Informe a receita financeira dos ativos garantidores(provisões técnicas).