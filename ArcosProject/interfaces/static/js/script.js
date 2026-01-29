function simularImportacao(tipo) {
    const fileInput = document.getElementById('fileInput');
    const resultArea = document.getElementById('resultArea');
    const tbody = document.getElementById('tabelaCorpo');

    if (fileInput.files.length === 0) {
        alert("Por favor, selecione um arquivo CSV primeiro.");
        return;
    }

    // Limpa tabela anterior
    tbody.innerHTML = "";

    // Simula tempo de processamento
    fileInput.disabled = true;
    document.body.style.cursor = 'wait';

    setTimeout(() => {
        let html = "";

        if (tipo === 'balancete') {
            // Dados Mockados de Balancete
            html += `
                <tr><td>1.1.1.01</td><td>Caixa Geral</td><td>R$ 50.000</td><td>R$ 10.000</td><td>R$ 5.000</td><td>R$ 55.000</td></tr>
                <tr><td>3.1.1.01</td><td>Prêmios Ganhos</td><td>R$ 0</td><td>R$ 0</td><td>R$ 1.000.000</td><td>R$ 1.000.000</td></tr>
                <tr><td>4.1.1.01</td><td>Sinistros Ocorridos</td><td>R$ 0</td><td>R$ 350.000</td><td>R$ 0</td><td>(R$ 350.000)</td></tr>
            `;
        } else if (tipo === 'apolice') {
            // Dados Mockados de Apólices
            html += `
                <tr><td>102938</td><td>Empresa Logística LTDA</td><td>01/01/2026</td><td>01/01/2027</td><td>R$ 150.000,00</td></tr>
                <tr><td>102939</td><td>Construtora Norte</td><td>15/01/2026</td><td>15/01/2027</td><td>R$ 80.500,00</td></tr>
                <tr><td>102940</td><td>Transportes Rápidos</td><td>20/02/2026</td><td>20/02/2027</td><td>R$ 45.000,00</td></tr>
            `;
        }

        tbody.innerHTML = html;
        resultArea.style.display = 'block';

        fileInput.disabled = false;
        document.body.style.cursor = 'default';
        alert("Arquivo importado com sucesso!");

    }, 800); // 800ms de delay dramático
}