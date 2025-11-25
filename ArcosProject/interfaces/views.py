from django.shortcuts import render

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