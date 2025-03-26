<template>
  <div class="app-container">
    <header class="app-header">
      <h1>Busca de Operadoras de Saúde</h1>
    </header>

    <main class="app-main">
      <div class="search-container">
        <div class="search-box">
          <input
            v-model.trim="searchQuery"
            @input="handleInput"
            @keyup.enter="searchOperadoras"
            placeholder="Digite o nome da operadora..."
            type="text"
            class="search-input"
            :disabled="loading"
          />
          <button
            @click="searchOperadoras"
            :disabled="searchQuery.length < 3 || loading"
            class="search-button"
          >
            {{ loading ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>
      </div>

      <div v-if="error" class="error-message">
        <p>⚠️ {{ error }}</p>
        <button @click="resetError" class="retry-button">Tentar novamente</button>
      </div>

      <div v-else-if="loading" class="loading-indicator">
        <div class="spinner"></div>
        <p>Carregando resultados...</p>
      </div>

      <div v-else-if="operadoras.length === 0 && searchPerformed" class="empty-results">
        <p>Nenhuma operadora encontrada para "{{ searchQuery }}"</p>
      </div>

      <div v-else-if="operadoras.length > 0" class="results-container">
        <div class="results-summary">
          <p>{{ operadoras.length }} resultados encontrados</p>
        </div>
        
        <div class="operadoras-list">
          <div v-for="operadora in operadoras" :key="operadora.registro_ans" class="operadora-card">
            <h3>{{ operadora.razao_social }}</h3>
            <p v-if="operadora.nome_fantasia">
              <span class="label">Nome Fantasia:</span> {{ operadora.nome_fantasia }}
            </p>
            <p><span class="label">CNPJ:</span> {{ formatCNPJ(operadora.cnpj) }}</p>
            <p><span class="label">Registro ANS:</span> {{ operadora.registro_ans }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      searchQuery: '',
      operadoras: [],
      loading: false,
      error: null,
      searchPerformed: false,
      debounceTimer: null
    }
  },
  methods: {
    async searchOperadoras() {
      if (this.searchQuery.length < 3) return;

      this.loading = true;
      this.error = null;
      this.searchPerformed = true;

      try {
        const response = await fetch(
          `http://localhost:5000/api/operadoras?q=${encodeURIComponent(this.searchQuery)}`
        );

        if (!response.ok) {
          throw new Error(`Erro na requisição: ${response.status}`);
        }

        this.operadoras = await response.json();
      } catch (err) {
        console.error('Erro na busca:', err);
        this.error = err.message;
        this.operadoras = [];
      } finally {
        this.loading = false;
      }
    },
    handleInput() {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = setTimeout(() => {
        if (this.searchQuery.length >= 3) {
          this.searchOperadoras();
        }
      }, 500);
    },
    resetError() {
      this.error = null;
      this.searchOperadoras();
    },
    formatCNPJ(cnpj) {
      if (!cnpj) return 'Não informado';
      const cleaned = cnpj.toString().replace(/\D/g, '');
      return cleaned.replace(
        /(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/,
        '$1.$2.$3/$4-$5'
      );
    }
  }
}
</script>

<style src="./assets/styles/main.css"></style>