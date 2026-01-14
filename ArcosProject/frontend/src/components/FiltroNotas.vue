<template>
  <div class="card mb-3">
    <div class="card-body">
      <div class="row g-3 align-items-end">
        <div class="col-md-4">
          <label class="form-label">Data Inicial</label>
          <input type="date" class="form-control" v-model="inicio" />
        </div>

        <div class="col-md-4">
          <label class="form-label">Data Final</label>
          <input type="date" class="form-control" v-model="fim" />
        </div>

        <div class="col-md-4">
          <button class="btn btn-primary w-100" @click="buscar">
            Buscar Notas
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const inicio = ref('')
const fim = ref('')

const emit = defineEmits(['buscar'])

function buscar() {
  emit('buscar', { inicio: inicio.value, fim: fim.value })
}
</script>