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
    aliquota = float(request.session.get('aliquota', 0))
    receita = float(request.session.get('receita', 0))
    # 2. Faz os cálculos das porcentagens
    # Documentos Fiscais: 1001 (20%), 1002 (13%), 1003 (35%), 1004 (17%), 1005 (15%)
    # Soma das porcentagens = 100%
    debito_puro = 560000 * (aliquota/100)
    imposto_receita_financeira = receita * (aliquota / 100)
    contexto = {
        'title': 'Débitos para Pagamento',
        'valor_total_pagar': formatar_brl(iva_total + imposto_receita_financeira),
        # Calculando e formatando cada item
        'doc_1001': formatar_brl(debito_puro * 0.20),
        'doc_1002': formatar_brl(debito_puro * 0.13),
        'doc_1003': formatar_brl(debito_puro * 0.35),
        'doc_1004': formatar_brl(debito_puro * 0.17),
        'doc_1005': formatar_brl(debito_puro * 0.15),
        'receita_financeira': formatar_brl(imposto_receita_financeira)
    }

    return render(request, 'pagamento.html', contexto)


def cadastra_cnpj(request):
    # Verificamos se alguém clicou no botão (se é POST)
    if request.method == 'POST':
        cnpj_raw = request.POST.get('cnpj')  # Pega o valor do input pelo 'name="cnpj"'
        cnpj_limpo = re.sub(r'\D', '', cnpj_raw)
        if not cnpj_limpo:
            return render(request, 'login.html', {'title': 'Login', 'erro': 'CNPJ vazio'})
        try:
            cnpj_int = int(cnpj_limpo)
            if valida_cnpj(cnpj_int):
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
    # 1. Inicializa variáveis no topo para evitar o erro "UnboundLocalError"
    # Isso garante que elas existam mesmo se o código pular algum bloco if
    aliquota = None
    receita = None
    iva_pagar = 0.0

    if request.method == 'POST':
        # CASO 2: O usuário clicou em "Sim, confirmar" no Modal
        if request.POST.get('confirmacao_final') == 'sim':
            # Recuperamos o valor calculado que passamos via hidden input
            iva_final = request.POST.get('iva_pagar_final')

            # SALVAMOS NA SESSÃO
            request.session['iva_a_pagar'] = iva_final

            return redirect('pagamento')

        # CASO 1: O usuário clicou em "Enviar" na tela principal
        # Agora estamos atribuindo valor às variáveis que criamos lá em cima
        aliquota = request.POST.get('aliquota_envio')
        receita = request.POST.get('receita')

        # Salva na sessão
        request.session['aliquota'] = aliquota
        request.session['receita'] = receita

        # Recálculo de segurança
        try:
            base_calculo = 560000.00
            total_creditos = 15000.00

            # Converte string para float com segurança
            if aliquota and aliquota.strip():
                aliq_float = float(aliquota)
            else:
                aliq_float = 0.0

            total_debitos = base_calculo * (aliq_float / 100)
            iva_pagar = total_debitos - total_creditos
        except ValueError:
            iva_pagar = 0.0

        # Renderiza a página com o modal de confirmação
        return render(request, 'apuracao.html', {
            'title': 'Apuração Assistida',
            'exibir_modal_confirmacao': True,
            'iva_calculado': iva_pagar,
            'iva_formatado': formatar_brl(iva_pagar),
            'aliquota_informada': aliquota,
            'receita_informada': receita
        })

    # Se não for POST (ex: GET), volta para apuração limpa
    return redirect('apuracao')

# Informe a receita financeira dos ativos garantidores(provisões técnicas).