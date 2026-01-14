import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/app/api',
})

export async function buscarNotas(dataInicial, dataFinal) {
  try {
      const response = await api.get('/notas/', {
        params: { inicio: dataInicial, fim: dataFinal }
      })

      // CORREÇÃO AQUI:
      // response.data = O JSON que veio do Django ({ data: [...] })
      // response.data.data = A lista real de notas ([...])
      console.log("O que chegou do Django:", response.data);
      return response.data.data;

  } catch (error) {
      console.error("Erro ao conectar com o Arcos Tributos:", error);
      throw error;
  }
}