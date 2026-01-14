<template>
  <div class="card mb-4 border-0 shadow-sm">
    <div class="card-body">
      <h4 class="card-title text-success mb-3">Consulta de Notas Fiscais (Integração Django)</h4>
      <p class="text-muted">Teste de conexão entre Vue.js e Backend Arcos Project.</p>

      <div class="row g-3 align-items-end">
        <div class="col-md-3">
          <label class="form-label">Data Inicial</label>
          <input type="date" class="form-control" v-model="inicio">
        </div>
        <div class="col-md-3">
          <label class="form-label">Data Final</label>
          <input type="date" class="form-control" v-model="fim">
        </div>
        <div class="col-md-3">
          <button class="btn btn-success w-100" @click="carregarDados" :disabled="loading">
            <span v-if="loading" class="spinner-border spinner-border-sm"></span>
            <span v-else>Buscar Notas</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="erro" class="alert alert-danger">{{ erro }}</div>

  <TabelaNotas v-if="notas.length > 0" :notas="notas" />

  <div v-if="!loading && notas.length === 0 && iniciouBusca" class="alert alert-warning mt-3">
    Nenhuma nota encontrada. Tente clicar em buscar.
  </div>
</template>

<script setup>
import { ref } from 'vue'
import TabelaNotas from '../components/TabelaNotas.vue'
import { buscarNotas } from '../services/notasService'

const notas = ref([])
const loading = ref(false)
const erro = ref(null)
const iniciouBusca = ref(false)
const inicio = ref('2025-01-01')
const fim = ref('2025-01-31')

async function carregarDados() {
  loading.value = true
  erro.value = null
  iniciouBusca.value = true

  try {
    // Busca os dados do Django
    notas.value = await buscarNotas(inicio.value, fim.value)
  } catch (e) {
    erro.value = 'Falha ao comunicar com o servidor Django. Verifique se ele está rodando.'
  } finally {
    loading.value = false
  }
}
</script>