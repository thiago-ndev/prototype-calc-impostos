pesos = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 6]
def valida_cnpj(cnpj: int) -> bool:
    validacao = False
    dig_verif = [(cnpj % 10), (cnpj % 100) // 10] # dig2 vem primeiro, seguido do dig1
    print(dig_verif[1])
    print(dig_verif[0])

    # primeiro digito
    digitos = cnpj
    for a in range(2): # a=0 -> a=1
        soma = 0
        digitos = digitos // 10
        for i in range(13-a):
            soma += pesos[i] * (digitos % 10)
            digitos = digitos // 10

        resto = soma % 11
        if (resto == 0 or resto == 1) and dig_verif[a] == 0:
            validacao = True
        elif (11 - resto) == dig_verif[a]:
            validacao = True

    return validacao

# Função auxiliar para formatar moeda no padrão BRL (R$ 1.000,00)
def formatar_brl(valor):
    try:
        val = float(valor)
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"