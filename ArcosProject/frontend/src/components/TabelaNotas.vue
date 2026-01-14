<template>
  <div class="card shadow-sm">
    <div class="card-header bg-dark text-white">
      <h5 class="mb-0"><i class="bi bi-table"></i> Detalhamento Fiscal</h5>
    </div>
    <div class="table-responsive">
      <table class="table table-hover table-striped align-middle mb-0">
        <thead class="table-light">
          <tr>
            <th>Prestador</th>
            <th>Emissão</th>
            <th class="text-end">Valor Bruto</th>
            <th class="text-end text-danger">IRRF</th>
            <th class="text-end text-danger">INSS</th>
            <th class="text-end text-primary">IBS (Novo)</th>
            <th class="text-end text-primary">CBS (Novo)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(nota, index) in notas" :key="index">
            <td>
              <div class="fw-bold">{{ nota.razao_social }}</div>
              <div class="small text-muted">{{ nota.cnpj }}</div>
            </td>
            <td>{{ formatarData(nota.data_emissao) }}</td>
            <td class="text-end fw-bold">{{ formatarMoeda(nota.valor_bruto) }}</td>
            <td class="text-end text-danger">{{ formatarMoeda(nota.irrf) }}</td>
            <td class="text-end text-danger">{{ formatarMoeda(nota.inss) }}</td>
            <td class="text-end text-primary bg-light">{{ formatarMoeda(nota.ibs) }}</td>
            <td class="text-end text-primary bg-light">{{ formatarMoeda(nota.cbs) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  notas: { type: Array, required: true }
})

function formatarMoeda(valor) {
  return Number(valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatarData(data) {
  if (!data) return '-'
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}
</script>