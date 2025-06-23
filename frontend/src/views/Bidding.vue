<template>
  <Layout>
    <div>
      <h2>Submit Bids</h2>
      
      <!-- Scenario Selection -->
      <div v-if="!selectedScenario" class="bid-form">
        <h5>Select a Scenario</h5>
        <div class="row">
          <div v-for="scenario in availableScenarios" :key="scenario.id" class="col-md-6 mb-3">
            <div class="card">
              <div class="card-body">
                <h6 class="card-title">{{ scenario.name }}</h6>
                <p class="card-text">{{ scenario.description }}</p>
                <button 
                  class="btn btn-primary"
                  @click="selectScenario(scenario)"
                >
                  Select This Scenario
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bidding Form -->
      <div v-else class="bid-form">
        <h5>Bidding for: {{ selectedScenario.name }}</h5>
        <p class="text-muted">{{ selectedScenario.description }}</p>
        
        <div class="row">
          <div class="col-md-6">
            <div class="mb-3">
              <label class="form-label">Bid Price ($/MWh)</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="bidForm.price" 
                min="0" 
                step="0.01"
                required
              >
            </div>
            <div class="mb-3">
              <label class="form-label">Bid Quantity (MW)</label>
              <input 
                type="number" 
                class="form-control" 
                v-model="bidForm.quantity" 
                min="0" 
                max="selectedScenario.demand"
                required
              >
            </div>
            <div class="mb-3">
              <label class="form-label">Bid Type</label>
              <select class="form-select" v-model="bidForm.bid_type">
                <option value="supply">Supply Bid</option>
                <option value="demand">Demand Bid</option>
              </select>
            </div>
            <button 
              class="btn btn-primary"
              @click="submitBid"
              :disabled="loading"
            >
              {{ loading ? 'Submitting...' : 'Submit Bid' }}
            </button>
            <button 
              class="btn btn-secondary ms-2"
              @click="selectedScenario = null"
            >
              Back to Scenarios
            </button>
          </div>
          
          <div class="col-md-6">
            <div class="result-card">
              <h6>Scenario Details</h6>
              <p><strong>Demand:</strong> {{ selectedScenario.demand }} MW</p>
              <p><strong>Status:</strong> {{ selectedScenario.status }}</p>
              <p><strong>Participants:</strong> {{ selectedScenario.participants || 0 }}</p>
              <p><strong>Created:</strong> {{ formatDate(selectedScenario.created_at) }}</p>
            </div>
            
            <div class="result-card mt-3">
              <h6>My Previous Bids</h6>
              <div v-for="bid in myBids" :key="bid.id" class="mb-2 p-2 border-bottom">
                <strong>${{ bid.price }}/MWh</strong> - {{ bid.quantity }} MW
                <br>
                <small class="text-muted">{{ formatDate(bid.created_at) }}</small>
              </div>
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
  name: 'Bidding',
  components: {
    Layout
  },
  data() {
    return {
      availableScenarios: [],
      selectedScenario: null,
      myBids: [],
      bidForm: {
        price: '',
        quantity: '',
        bid_type: 'supply'
      },
      loading: false
    }
  },
  async mounted() {
    await this.loadScenarios()
    // Check if scenario is passed in URL
    const scenarioId = this.$route.query.scenario
    if (scenarioId) {
      await this.selectScenarioById(scenarioId)
    }
  },
  methods: {
    async loadScenarios() {
      try {
        const response = await api.get('/scenarios/')
        this.availableScenarios = response.data.filter(s => s.status === 'active')
      } catch (error) {
        console.error('Error loading scenarios:', error)
      }
    },
    
    async selectScenario(scenario) {
      this.selectedScenario = scenario
      await this.loadMyBids(scenario.id)
    },
    
    async selectScenarioById(scenarioId) {
      try {
        const response = await api.get(`/scenarios/${scenarioId}`)
        this.selectedScenario = response.data
        await this.loadMyBids(scenarioId)
      } catch (error) {
        console.error('Error loading scenario:', error)
      }
    },
    
    async loadMyBids(scenarioId) {
      try {
        const response = await api.get(`/bids/my-bids?scenario_id=${scenarioId}`)
        this.myBids = response.data
      } catch (error) {
        console.error('Error loading bids:', error)
      }
    },
    
    async submitBid() {
      if (!this.bidForm.price || !this.bidForm.quantity) {
        alert('Please fill in all fields')
        return
      }
      
      this.loading = true
      try {
        await api.post(`/bids/submit`, {
          scenario_id: this.selectedScenario.id,
          price: parseFloat(this.bidForm.price),
          quantity: parseFloat(this.bidForm.quantity),
          bid_type: this.bidForm.bid_type
        })
        
        // Reset form and reload bids
        this.bidForm = {
          price: '',
          quantity: '',
          bid_type: 'supply'
        }
        await this.loadMyBids(this.selectedScenario.id)
        
        alert('Bid submitted successfully!')
      } catch (error) {
        console.error('Error submitting bid:', error)
        alert('Error submitting bid: ' + (error.response?.data?.detail || 'Unknown error'))
      } finally {
        this.loading = false
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script> 