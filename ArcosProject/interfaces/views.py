from django.shortcuts import render, redirect
from django.http import JsonResponse
from datetime import datetime
from .util import *
from random import randint
import re


def login_view(request):
    return render(request, 'login.html', {'title': 'Login'})

def portal_view(request):
    return render(request, 'portal.html', {'title': 'Portal'})

def hub_view(request):
    return render(request, 'hub.html', {'title': 'Hub'})

def captura_view(request):
    return render(request, 'captura.html', {'title': 'Captura'})

def captura_balancete_view(request):
    return render(request, 'captura-balancete.html', {'title': 'Balancete'})

def captura_apolices_view(request):
    return render(request, 'captura-apolices.html', {'title': 'Apolices'})

def dere_view(request):
    return render(request, 'dere.html', {'title': 'DERE'})

def dashboard_view(request):
    return render(request, 'dashboard.html', {'title': 'Minhas Operações de Consumo'})


def apuracao_view(request):
    # Tenta recuperar o valor de utilizados se já tiver sido salvo, para o input não voltar ao padrão
    utilizados = request.session.get('utilizados', 15000)
    return render(request, 'apuracao.html', {
        'title': 'Apuração Assistida',
        'utilizados_informado': utilizados
    })



# ATUALIZADO: Cálculo dinâmico para o Dashboard
def operacoes_view(request):
    # Valores Padrão (Simulação)
    nao_apropriados = 15000.00
    apropriados = 20000.00

    # Tenta pegar 'utilizados' da sessão, senão usa padrão 15000
    try:
        utilizados = float(request.session.get('utilizados', 15000))
    except (ValueError, TypeError):
        utilizados = 15000.00

    # Lógica do Usuário: Valor do Resultado = Não Apropriados + Não Utilizados
    nao_utilizados = apropriados - utilizados
    resultado_janeiro = nao_apropriados + nao_utilizados

    # Se o valor for positivo, formata com 'C' (Credor). Se negativo, 'D' (Devedor)
    letra = "C" if resultado_janeiro >= 0 else "D"
    resultado_formatado = f"{formatar_brl(abs(resultado_janeiro))} {letra}"

    return render(request, 'operacoes.html', {
        'title': 'Minhas Operações de Consumo',
        'resultado_jan': resultado_formatado  # Passamos para o template
    })


def pagamento_view(request):
    iva_total = float(request.session.get('iva_a_pagar', 0))
    aliquota = float(request.session.get('aliquota', 0))
    receita = float(request.session.get('receita', 0))

    debito_puro = 560000 * (aliquota / 100)
    imposto_receita_financeira = receita * (aliquota / 100)

    contexto = {
        'title': 'Débitos para Pagamento',
        'valor_total_pagar': formatar_brl(iva_total),
        'doc_1001': formatar_brl(debito_puro * 0.20),
        'doc_1002': formatar_brl(debito_puro * 0.13),
        'doc_1003': formatar_brl(debito_puro * 0.35),
        'doc_1004': formatar_brl(debito_puro * 0.17),
        'doc_1005': formatar_brl(debito_puro * 0.15),
        'receita_financeira': formatar_brl(imposto_receita_financeira)
    }

    return render(request, 'pagamento.html', contexto)


def cadastra_cnpj(request):
    if request.method == 'POST':
        cnpj_raw = request.POST.get('cnpj')
        cnpj_limpo = re.sub(r'\D', '', cnpj_raw)
        if not cnpj_limpo:
            return render(request, 'login.html', {'title': 'Login', 'erro': 'CNPJ vazio'})
        try:
            cnpj_int = int(cnpj_limpo)
            if valida_cnpj(cnpj_int):
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'title': 'Login', 'error': 'CNPJ Inválido'})
        except ValueError:
            return render(request, 'login.html', {'title': 'Login'})
    return redirect('login')


def enviar_receita(request):
    if request.method == 'POST':
        if request.POST.get('confirmacao_final') == 'sim':
            iva_final = request.POST.get('iva_pagar_final')
            request.session['iva_a_pagar'] = iva_final
            return redirect('pagamento')

        # CASO 1: Preparação do Modal
        aliquota = request.POST.get('aliquota_envio')
        receita = request.POST.get('receita')
        utilizados = request.POST.get('utilizados')  # Novo campo recuperado

        # SALVA NA SESSÃO
        request.session['aliquota'] = aliquota
        request.session['receita'] = receita
        request.session['utilizados'] = utilizados  # Salva para o Dashboard usar

        try:
            base_calculo = 560000.00
            # ATUALIZADO: Total Créditos vem do input Utilizados
            total_creditos = float(utilizados) if utilizados else 0

            aliq_float = float(aliquota) if aliquota else 0
            rec_float = float(receita) if receita else 0

            total_debitos = (base_calculo + rec_float) * (aliq_float / 100)

            # ATUALIZADO: IVA = Débitos - Utilizados
            iva_pagar = total_debitos - total_creditos
        except ValueError:
            iva_pagar = 0.0

        return render(request, 'apuracao.html', {
            'title': 'Apuração Assistida',
            'exibir_modal_confirmacao': True,
            'iva_calculado': iva_pagar,
            'iva_formatado': formatar_brl(iva_pagar),
            'aliquota_informada': aliquota,
            'receita_informada': receita,
            'utilizados_informado': utilizados
        })

    return redirect('apuracao')

def notas_fiscais(request):
    """
    Retorna uma lista de notas fiscais em formato JSON para o Frontend.
    Simula uma consulta ao banco de dados.
    """
    # Recupera parâmetros da URL (ex: ?inicio=2025-01-01&fim=2025-01-31)
    data_inicial = request.GET.get('inicio')
    data_final = request.GET.get('fim')

    # Simulação de dados (Backend Python gerando a lista)
    lista_notas = []
    for i in range(12):
        dia = f'0{randint(4, 7)}'
        mes = f'0{i + 1}'
        if i >= 9:
            mes = str(i+1)

        valor_base = 976
        numero_nf = "0000033"+ f"{36 + i}"
        nota = {
            'data_emissao': f'{dia}-{mes}-2025',
            'data_captura': datetime.now().strftime('%d-%m-%Y'),
            'cnpj_tomador': '50.466.717/0001-00',
            'razao_tomador': 'ARCOS DA LAPA DESENVOLVIMENTO DE SISTEMAS E CONSULTORIA LTDA',
            'municipio_tomador': 'Rio de Janeiro',
            'uf_tomador': 'RJ',

            'cnpj_prestador': '23.301.943/0015-55',
            'razao_prestador': 'WEWORK SERVICOS DE ESCRITORIO LTDA',
            'municipio_prestador': 'São Paulo',
            'uf_prestador': 'SP',

            'cnpj_intermediario': 'N/A',
            'razao_intermediario': 'N/A',
            'municipio_intermediario': 'N/A',
            'uf_intermediario': 'N/A',

            'numero_nf': numero_nf,
            'valor_bruto': valor_base,
            'codigo_servico': 7773,
            'nbs': 'N/A',
            'nbs_descricao': 'N/A',
            'irrf': valor_base * 0.015,
            'irrf_aliq': '1,5%',
            'iss': valor_base * 0.05,
            'iss_aliq': '5%',

            'inss': valor_base * 0.02,
            'csrf': 0,

            'personalidade_jur': 'N/A',

            'cbs': valor_base * 0.12,
            'cbs_aliq': '12%',
            'ibs': valor_base * 0.1,
            'ibs_aliq': '10%',

            'valor_liquido': 0,
            'chave_nf': 'N/A',
        }
        lista_notas.append(nota) # lista de dicionários

    # Retorna como JSON. 'safe=False' permite retornar listas, não só dicionários.
    return JsonResponse({'data': lista_notas}, safe=False)