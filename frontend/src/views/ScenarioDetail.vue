<template>
  <Layout>
    <div>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Scenario Details</h2>
        <button class="btn btn-secondary" @click="$router.go(-1)">
          ← Back
        </button>
      </div>

      <div v-if="loading" class="text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="scenario" class="row">
        <!-- Scenario Information -->
        <div class="col-md-8">
          <div class="result-card mb-4">
            <h4>{{ scenario.name }}</h4>
            <p class="text-muted">{{ scenario.description || 'No description provided' }}</p>
            
            <div class="row">
              <div class="col-md-6">
                <div class="mb-3">
                  <strong>Demand:</strong> {{ scenario.demand }} MW
                </div>
                <div class="mb-3">
                  <strong>Status:</strong> 
                  <span :class="getStatusClass(scenario.status)">
                    {{ scenario.status }}
                  </span>
                </div>
                <div class="mb-3">
                  <strong>Market Type:</strong> 
                  <span class="badge bg-info">{{ formatMarketType(scenario.enabled_mechanisms?.[0]) }}</span>
                </div>
              </div>
              <div class="col-md-6">
                <div class="mb-3">
                  <strong>Created:</strong> {{ formatDate(scenario.created_at) }}
                </div>
                <div class="mb-3">
                  <strong>Participants:</strong> {{ scenario.participants?.length || 0 }}
                </div>
                <div class="mb-3">
                  <strong>Experiment Type:</strong> 
                  <span class="badge" :class="scenario.is_open ? 'bg-success' : 'bg-warning'">
                    {{ scenario.is_open ? 'Open' : 'Class Limited' }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-4">
              <button 
                v-if="scenario.status === 'active' && !isParticipant"
                class="btn btn-primary me-2"
                @click="joinScenario"
              >
                Join Scenario
              </button>
              <button 
                v-if="scenario.status === 'active' && isParticipant"
                class="btn btn-success me-2"
                @click="goToBidding"
              >
                Submit Bids
              </button>
              <button 
                v-if="scenario.status === 'completed'"
                class="btn btn-info me-2"
                @click="viewResults"
              >
                View Results
              </button>
            </div>
          </div>

          <!-- Participants List -->
          <div class="result-card mb-4">
            <h5>Participants</h5>
            <div v-if="participants.length > 0" class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Username</th>
                    <th>Full Name</th>
                    <th>Role</th>
                    <th>Join Time</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="participant in participants" :key="participant.username">
                    <td>{{ participant.username }}</td>
                    <td>{{ participant.full_name }}</td>
                    <td>
                      <span class="badge" :class="participant.role === 'teacher' ? 'bg-primary' : 'bg-secondary'">
                        {{ participant.role }}
                      </span>
                    </td>
                    <td>{{ formatDate(participant.join_time) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-muted">
              No participants yet.
            </div>
          </div>
        </div>

        <!-- Bids Summary -->
        <div class="col-md-4">
          <div class="result-card">
            <h5>Bids Summary</h5>
            <div v-if="bids.length > 0">
              <div class="mb-3">
                <strong>Total Bids:</strong> {{ bids.length }}
              </div>
              <div class="mb-3">
                <strong>Supply Bids:</strong> {{ supplyBids.length }}
              </div>
              <div class="mb-3">
                <strong>Demand Bids:</strong> {{ demandBids.length }}
              </div>
              <div class="mb-3">
                <strong>Average Price:</strong> ${{ averagePrice.toFixed(2) }}
              </div>
              <div class="mb-3">
                <strong>Total Quantity:</strong> {{ totalQuantity }} MW
              </div>
            </div>
            <div v-else class="text-muted">
              No bids submitted yet.
            </div>
          </div>

          <!-- Recent Bids -->
          <div class="result-card mt-3">
            <h6>Recent Bids</h6>
            <div v-if="recentBids.length > 0">
              <div v-for="bid in recentBids.slice(0, 5)" :key="bid.id" class="mb-2 p-2 border rounded">
                <div class="d-flex justify-content-between">
                  <span>{{ bid.participant_name }}</span>
                  <span class="badge" :class="bid.bid_type === 'supply' ? 'bg-success' : 'bg-warning'">
                    {{ bid.bid_type }}
                  </span>
                </div>
                <div class="small text-muted">
                  ${{ bid.price }} | {{ bid.quantity }} MW
                </div>
              </div>
            </div>
            <div v-else class="text-muted">
              No bids yet.
            </div>
          </div>
        </div>
      </div>

      <div v-else class="alert alert-danger">
        Scenario not found.
      </div>

      <!-- Alert Messages -->
      <div v-if="alert.show" :class="`alert alert-${alert.type} mt-3`" role="alert">
        {{ alert.message }}
      </div>
    </div>
  </Layout>
</template>

<script>
import Layout from '../components/Layout.vue'
import api from '../services/api.js'

export default {
  name: 'ScenarioDetail',
  components: {
    Layout
  },
  data() {
    return {
      loading: true,
      scenario: null,
      participants: [],
      bids: [],
      alert: {
        show: false,
        type: 'success',
        message: ''
      }
    }
  },
  computed: {
    isParticipant() {
      if (!this.scenario || !this.scenario.participants) return false
      const currentUser = JSON.parse(localStorage.getItem('currentUser') || '{}')
      return this.scenario.participants.includes(currentUser.username)
    },
    supplyBids() {
      return this.bids.filter(bid => bid.bid_type === 'supply')
    },
    demandBids() {
      return this.bids.filter(bid => bid.bid_type === 'demand')
    },
    averagePrice() {
      if (this.bids.length === 0) return 0
      const total = this.bids.reduce((sum, bid) => sum + bid.price, 0)
      return total / this.bids.length
    },
    totalQuantity() {
      return this.bids.reduce((sum, bid) => sum + bid.quantity, 0)
    },
    recentBids() {
      return [...this.bids].sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    }
  },
  async mounted() {
    await this.loadScenario()
  },
  methods: {
    async loadScenario() {
      try {
        const scenarioId = this.$route.params.id
        console.log('Loading scenario with ID:', scenarioId)
        
        const response = await api.get(`/scenarios/${scenarioId}`)
        console.log('Scenario response:', response.data)
        this.scenario = response.data
        
        // Load participants
        await this.loadParticipants()
        
        // Load bids
        await this.loadBids()
        
      } catch (error) {
        console.error('Error loading scenario:', error)
        console.error('Error response:', error.response)
        this.showAlert('danger', `Failed to load scenario details: ${error.response?.data?.detail || error.message}`)
      } finally {
        this.loading = false
      }
    },
    
    async loadParticipants() {
      if (!this.scenario || !this.scenario.participants) return
      
      try {
        // Get user details for each participant
        const participants = []
        for (const username of this.scenario.participants) {
          try {
            const response = await api.get(`/users/profile`)
            const user = response.data
            if (user.username === username) {
              participants.push({
                username: user.username,
                full_name: user.full_name,
                role: user.role,
                join_time: this.scenario.created_at // Approximate join time
              })
            }
          } catch (error) {
            // If we can't get user details, use basic info
            participants.push({
              username: username,
              full_name: username,
              role: 'unknown',
              join_time: this.scenario.created_at
            })
          }
        }
        this.participants = participants
      } catch (error) {
        console.error('Error loading participants:', error)
      }
    },
    
    async loadBids() {
      try {
        const scenarioId = this.$route.params.id
        const response = await api.get(`/bids/scenario/${scenarioId}`)
        this.bids = response.data
      } catch (error) {
        console.error('Error loading bids:', error)
        this.bids = []
      }
    },
    
    async joinScenario() {
      try {
        const scenarioId = this.$route.params.id
        await api.post(`/scenarios/${scenarioId}/join`)
        this.showAlert('success', 'Successfully joined scenario!')
        await this.loadScenario() // Reload to update participant status
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to join scenario')
      }
    },
    
    goToBidding() {
      this.$router.push(`/bidding?scenario=${this.scenario.id}`)
    },
    
    viewResults() {
      this.$router.push(`/results?scenario=${this.scenario.id}`)
    },
    
    getStatusClass(status) {
      const classes = {
        'active': 'badge bg-success',
        'completed': 'badge bg-secondary',
        'pending': 'badge bg-warning'
      }
      return classes[status] || 'badge bg-secondary'
    },
    
    formatMarketType(marketType) {
      const types = {
        'uniform_price': 'Uniform Price',
        'pay_as_bid': 'Pay-as-Bid',
        'fixed_cost_uniform': 'Fixed Cost Uniform',
        'fixed_cost_pay_as_bid': 'Fixed Cost Pay-as-Bid',
        'zone_limit_uniform': 'Zone Limit Uniform',
        'constrained_on': 'Constrained On',
        'risk_adjusted_uniform': 'Risk Adjusted Uniform',
        'two_stage': 'Two Stage Market'
      }
      return types[marketType] || marketType
    },
    
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString()
    },
    
    showAlert(type, message) {
      this.alert = {
        show: true,
        type,
        message
      }
      setTimeout(() => {
        this.alert.show = false
      }, 5000)
    }
  }
}
</script> 