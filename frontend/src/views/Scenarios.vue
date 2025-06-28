<template>
  <Layout>
    <div>
      <h2>Experiment Scenarios</h2>
      <div class="row">
        <div v-for="scenario in scenarios" :key="scenario.id" class="col-md-6 mb-4">
          <div class="result-card">
            <h5>{{ scenario.name }}</h5>
            <p class="text-muted">{{ scenario.description }}</p>
            <div class="row">
              <div class="col-6">
                <small><strong>Demand:</strong> {{ scenario.demand }} MW</small>
              </div>
              <div class="col-6">
                <small><strong>Status:</strong> 
                  <span :class="getStatusClass(scenario.status)">
                    {{ scenario.status }}
                  </span>
                </small>
              </div>
            </div>
            <div class="row mt-2">
              <div class="col-6">
                <small><strong>Participants:</strong> {{ scenario.participants || 0 }}</small>
              </div>
              <div class="col-6">
                <small><strong>Created:</strong> {{ formatDate(scenario.created_at) }}</small>
              </div>
            </div>
            <div class="mt-3">
              <button 
                v-if="scenario.status === 'active'" 
                class="btn btn-primary btn-sm me-2"
                @click="joinScenario(scenario.id)"
              >
                Join Scenario
              </button>
              <button 
                class="btn btn-outline-secondary btn-sm"
                @click="viewDetails(scenario.id)"
              >
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script>
import Layout from '../components/Layout.vue'
import api from '../services/api.js'

export default {
  name: 'Scenarios',
  components: {
    Layout
  },
  data() {
    return {
      scenarios: []
    }
  },
  async mounted() {
    await this.loadScenarios()
  },
  methods: {
    async loadScenarios() {
      try {
        const response = await api.get('/scenarios/')
        console.log('Scenarios response:', response.data)
        this.scenarios = response.data
      } catch (error) {
        console.error('Error loading scenarios:', error)
      }
    },
    
    async joinScenario(scenarioId) {
      try {
        await api.post(`/scenarios/${scenarioId}/join`)
        this.$router.push(`/bidding?scenario=${scenarioId}`)
      } catch (error) {
        console.error('Error joining scenario:', error)
      }
    },
    
    viewDetails(scenarioId) {
      this.$router.push(`/scenarios/${scenarioId}`)
    },
    
    getStatusClass(status) {
      const classes = {
        'active': 'badge bg-success',
        'completed': 'badge bg-secondary',
        'pending': 'badge bg-warning'
      }
      return classes[status] || 'badge bg-secondary'
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script> 