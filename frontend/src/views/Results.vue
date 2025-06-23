<template>
  <Layout>
    <div>
      <h2>Results Analysis</h2>
      
      <!-- Scenario Selection -->
      <div class="mb-4">
        <label class="form-label">Select Scenario</label>
        <select class="form-select" v-model="selectedScenarioId" @change="onScenarioChange">
          <option value="">Choose a scenario...</option>
          <option v-for="scenario in scenarios" :key="scenario.id" :value="scenario.id">
            {{ scenario.name }} ({{ scenario.status }})
          </option>
        </select>
        <small class="form-text text-muted">
          Select any scenario to view results. Completed scenarios will have full results, while active scenarios may have partial data.
        </small>
      </div>

      <!-- Mechanism Selection -->
      <div v-if="selectedScenarioId && availableMechanisms.length > 0" class="mb-4">
        <label class="form-label">Select Market Mechanism</label>
        <select class="form-select" v-model="selectedMechanism" @change="loadResults">
          <option value="">Choose a mechanism...</option>
          <option v-for="mechanism in availableMechanisms" :key="mechanism" :value="mechanism">
            {{ formatMechanismName(mechanism) }}
          </option>
        </select>
        <small class="form-text text-muted">
          Different market mechanisms may produce different clearing prices and results.
        </small>
      </div>

      <!-- Results Display -->
      <div v-if="selectedScenarioId && selectedMechanism && results" class="row">
        <!-- Market Clearing Results -->
        <div class="col-md-6">
          <div class="result-card">
            <h5>Market Clearing Results</h5>
            <div class="row">
              <div class="col-6">
                <p><strong>Clearing Price:</strong> ${{ results.clearing_price }}/MWh</p>
                <p><strong>Total Volume:</strong> {{ results.total_volume }} MW</p>
              </div>
              <div class="col-6">
                <p><strong>Total Revenue:</strong> ${{ results.total_revenue }}</p>
                <p><strong>Participants:</strong> {{ results.participants }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- My Performance -->
        <div class="col-md-6">
          <div class="result-card">
            <h5>My Performance</h5>
            <div class="row">
              <div class="col-6">
                <p><strong>My Bids:</strong> {{ myBids.length }}</p>
                <p><strong>Accepted Volume:</strong> {{ myAcceptedVolume }} MW</p>
              </div>
              <div class="col-6">
                <p><strong>My Revenue:</strong> ${{ myRevenue }}</p>
                <p><strong>My Profit:</strong> ${{ myProfit }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts -->
        <div class="col-md-12 mt-4">
          <div class="chart-container">
            <div id="priceChart" style="height: 400px;"></div>
          </div>
        </div>

        <!-- Bid Details -->
        <div class="col-md-12 mt-4">
          <div class="result-card">
            <h5>All Bids</h5>
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>Participant</th>
                    <th>Price ($/MWh)</th>
                    <th>Quantity (MW)</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Revenue</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="bid in allBids" :key="bid.id">
                    <td>{{ bid.participant_name }}</td>
                    <td>${{ bid.price }}</td>
                    <td>{{ bid.quantity }}</td>
                    <td>{{ bid.bid_type }}</td>
                    <td>
                      <span :class="getBidStatusClass(bid.status)">
                        {{ bid.status }}
                      </span>
                    </td>
                    <td>${{ bid.revenue || 0 }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- No Results Message -->
      <div v-else-if="selectedScenarioId && selectedMechanism" class="text-center mt-4">
        <p>No results available for this scenario and mechanism combination.</p>
        <p class="text-muted">This scenario may not have been completed or may not have any bids for the selected mechanism.</p>
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
import * as echarts from 'echarts'

export default {
  name: 'Results',
  components: {
    Layout
  },
  data() {
    return {
      scenarios: [],
      selectedScenarioId: '',
      results: null,
      allBids: [],
      myBids: [],
      priceChart: null,
      alert: {
        show: false,
        type: '',
        message: ''
      },
      availableMechanisms: [],
      selectedMechanism: ''
    }
  },
  computed: {
    myAcceptedVolume() {
      return this.myBids
        .filter(bid => bid.status === 'accepted')
        .reduce((sum, bid) => sum + bid.quantity, 0)
    },
    myRevenue() {
      return this.myBids
        .filter(bid => bid.status === 'accepted')
        .reduce((sum, bid) => sum + (bid.revenue || 0), 0)
    },
    myProfit() {
      // Simplified profit calculation
      return this.myRevenue * 0.1 // Assuming 10% profit margin
    }
  },
  async mounted() {
    // Check login status first
    const token = localStorage.getItem('token')
    const user = localStorage.getItem('currentUser')
    
    console.log('Login status check:', {
      hasToken: !!token,
      hasUser: !!user,
      user: user ? JSON.parse(user) : null
    })
    
    if (!token || !user) {
      this.showAlert('warning', 'Please log in to view results')
      return
    }
    
    await this.loadScenarios()
  },
  methods: {
    async loadScenarios() {
      try {
        // Check if user is logged in
        const token = localStorage.getItem('token')
        if (!token) {
          this.showAlert('danger', 'Please log in first')
          return
        }
        
        console.log('Loading scenarios...')
        const response = await api.get('/scenarios/')
        // Show all scenarios, not just completed ones
        this.scenarios = response.data
        console.log('Loaded scenarios:', this.scenarios)
      } catch (error) {
        console.error('Error loading scenarios:', error)
        if (error.response) {
          this.showAlert('danger', `Failed to load scenarios: ${error.response.status} - ${error.response.data?.detail || error.response.statusText}`)
        } else if (error.request) {
          this.showAlert('danger', 'Network error: Unable to connect to server. Please check if the backend is running.')
        } else {
          this.showAlert('danger', 'Error loading scenarios: ' + error.message)
        }
      }
    },
    
    async loadResults() {
      if (!this.selectedScenarioId || !this.selectedMechanism) return
      
      try {
        console.log('Loading results for scenario:', this.selectedScenarioId, 'with mechanism:', this.selectedMechanism)
        
        // Check if user is logged in
        const token = localStorage.getItem('token')
        if (!token) {
          this.showAlert('danger', 'Please log in first')
          return
        }
        
        console.log('Token exists:', !!token)
        console.log('Making API calls...')
        
        const [resultsRes, bidsRes] = await Promise.all([
          api.get(`/simulation/result/${this.selectedScenarioId}?type=${this.selectedMechanism}`), // Add mechanism parameter
          api.get(`/bids/scenario/${this.selectedScenarioId}`)
        ])
        
        console.log('Results response:', resultsRes.data)
        console.log('Bids response:', bidsRes.data)
        
        this.results = resultsRes.data
        this.allBids = bidsRes.data
        this.myBids = bidsRes.data.filter(bid => bid.participant_id === this.getCurrentUserId())
        
        this.$nextTick(() => {
          this.initPriceChart()
        })
      } catch (error) {
        console.error('Error loading results:', error)
        console.error('Error details:', {
          message: error.message,
          response: error.response,
          request: error.request,
          config: error.config
        })
        
        if (error.response) {
          // Server responded with error status
          this.showAlert('danger', `Server error: ${error.response.status} - ${error.response.data?.detail || error.response.statusText}`)
        } else if (error.request) {
          // Network error
          this.showAlert('danger', 'Network error: Unable to connect to server. Please check if the backend is running.')
        } else {
          // Other error
          this.showAlert('danger', 'Error: ' + error.message)
        }
      }
    },
    
    getCurrentUserId() {
      const user = localStorage.getItem('currentUser')
      return user ? JSON.parse(user).id : null
    },
    
    initPriceChart() {
      if (this.priceChart) {
        this.priceChart.dispose()
      }
      
      const chartDom = document.getElementById('priceChart')
      this.priceChart = echarts.init(chartDom)
      
      // Sort bids by price
      const sortedBids = [...this.allBids].sort((a, b) => a.price - b.price)
      
      const option = {
        title: {
          text: 'Supply and Demand Curve'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['Supply', 'Demand', 'Clearing Price']
        },
        xAxis: {
          type: 'value',
          name: 'Price ($/MWh)'
        },
        yAxis: {
          type: 'value',
          name: 'Quantity (MW)'
        },
        series: [
          {
            name: 'Supply',
            type: 'line',
            data: sortedBids
              .filter(bid => bid.bid_type === 'supply')
              .map((bid, index) => [bid.price, sortedBids
                .filter(b => b.bid_type === 'supply' && b.price <= bid.price)
                .reduce((sum, b) => sum + b.quantity, 0)
              ])
          },
          {
            name: 'Demand',
            type: 'line',
            data: sortedBids
              .filter(bid => bid.bid_type === 'demand')
              .map((bid, index) => [bid.price, sortedBids
                .filter(b => b.bid_type === 'demand' && b.price >= bid.price)
                .reduce((sum, b) => sum + b.quantity, 0)
              ])
          },
          {
            name: 'Clearing Price',
            type: 'line',
            data: [[this.results.clearing_price, 0], [this.results.clearing_price, this.results.total_volume]],
            lineStyle: {
              type: 'dashed'
            }
          }
        ]
      }
      
      this.priceChart.setOption(option)
    },
    
    getBidStatusClass(status) {
      const classes = {
        'accepted': 'badge bg-success',
        'rejected': 'badge bg-danger',
        'pending': 'badge bg-warning'
      }
      return classes[status] || 'badge bg-secondary'
    },
    
    showAlert(type, message) {
      this.alert.show = true
      this.alert.type = type
      this.alert.message = message
      setTimeout(() => {
        this.alert.show = false
      }, 3000)
    },

    onScenarioChange() {
      // Reset mechanism selection when scenario changes
      this.selectedMechanism = ''
      this.results = null
      this.allBids = []
      this.myBids = []
      
      if (this.selectedScenarioId) {
        // Get available mechanisms for the selected scenario
        const selectedScenario = this.scenarios.find(s => s.id === this.selectedScenarioId)
        if (selectedScenario && selectedScenario.enabled_mechanisms) {
          this.availableMechanisms = selectedScenario.enabled_mechanisms
          // Auto-select first mechanism if available
          if (this.availableMechanisms.length > 0) {
            this.selectedMechanism = this.availableMechanisms[0]
            this.loadResults()
          }
        } else {
          this.availableMechanisms = []
        }
      } else {
        this.availableMechanisms = []
      }
    },

    formatMechanismName(mechanism) {
      const mechanismNames = {
        'uniform_price': 'Uniform Price',
        'pay_as_bid': 'Pay-as-Bid',
        'fixed_cost_uniform': 'Fixed Cost Uniform',
        'fixed_cost_pay_as_bid': 'Fixed Cost Pay-as-Bid',
        'zone_limit_uniform': 'Zone Limit Uniform',
        'constrained_on': 'Constrained On',
        'risk_adjusted_uniform': 'Risk Adjusted Uniform',
        'two_stage': 'Two Stage Market'
      }
      return mechanismNames[mechanism] || mechanism
    }
  }
}
</script> 