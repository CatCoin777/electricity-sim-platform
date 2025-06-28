<template>
  <Layout>
    <div>
      <h2>Admin Panel</h2>
      
      <!-- Create New Scenario -->
      <div class="result-card mb-4">
        <h5>Create New Scenario</h5>
        <form @submit.prevent="createScenario">
          <div class="row">
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label">Scenario Name</label>
                <input type="text" class="form-control" v-model="scenarioForm.name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="scenarioForm.description" rows="3" placeholder="(optional)"></textarea>
              </div>
            </div>
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label">Demand (MW)</label>
                <input type="number" class="form-control" v-model="scenarioForm.demand" min="1" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Market Type</label>
                <select class="form-select" v-model="scenarioForm.market_type" required>
                  <option value="uniform_price">Uniform Price</option>
                  <option value="pay_as_bid">Pay-as-Bid</option>
                  <option value="fixed_cost_uniform">Fixed Cost Uniform</option>
                  <option value="fixed_cost_pay_as_bid">Fixed Cost Pay-as-Bid</option>
                  <option value="zone_limit_uniform">Zone Limit Uniform</option>
                  <option value="constrained_on">Constrained On</option>
                  <option value="risk_adjusted_uniform">Risk Adjusted Uniform</option>
                  <option value="two_stage">Two Stage Market</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Experiment Type</label>
                <select class="form-select" v-model="scenarioForm.experiment_type">
                  <option value="open">Open Experiment</option>
                  <option value="class_limited">Class Limited</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Duration (minutes)</label>
                <input type="number" class="form-control" v-model="scenarioForm.duration" min="1" required>
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary" :disabled="loading">
            {{ loading ? 'Creating...' : 'Create Scenario' }}
          </button>
        </form>
      </div>

      <!-- Manage Scenarios -->
      <div class="result-card">
        <h5>Manage Scenarios</h5>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Name</th>
                <th>Demand</th>
                <th>Status</th>
                <th>Participants</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="scenario in scenarios" :key="scenario.id">
                <td>{{ scenario.name }}</td>
                <td>{{ scenario.demand }} MW</td>
                <td>
                  <span :class="getStatusClass(scenario.status)">
                    {{ scenario.status }}
                  </span>
                </td>
                <td>{{ scenario.participants || 0 }}</td>
                <td>{{ formatDate(scenario.created_at) }}</td>
                <td>
                  <button 
                    v-if="scenario.status === 'pending'"
                    class="btn btn-success btn-sm me-2"
                    @click="startScenario(scenario.id)"
                  >
                    Start
                  </button>
                  <button 
                    v-if="scenario.status === 'active'"
                    class="btn btn-warning btn-sm me-2"
                    @click="endScenario(scenario.id)"
                  >
                    End
                  </button>
                  <button 
                    class="btn btn-info btn-sm me-2"
                    @click="viewResults(scenario.id)"
                  >
                    Results
                  </button>
                  <button 
                    class="btn btn-danger btn-sm"
                    @click="deleteScenario(scenario.id)"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
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
  name: 'AdminPanel',
  components: {
    Layout
  },
  data() {
    return {
      loading: false,
      scenarios: [],
      scenarioForm: {
        name: '',
        description: '',
        demand: 10,
        market_type: 'uniform_price',
        experiment_type: 'open',
        duration: 60
      },
      alert: {
        show: false,
        type: 'success',
        message: ''
      }
    }
  },
  async mounted() {
    await this.loadScenarios()
  },
  methods: {
    async loadScenarios() {
      try {
        const response = await api.get('/scenarios/')
        this.scenarios = response.data
      } catch (error) {
        console.error('Error loading scenarios:', error)
      }
    },
    
    async createScenario() {
      this.loading = true
      try {
        await api.post('/scenarios/', this.scenarioForm)
        
        // Reset form
        this.scenarioForm = {
          name: '',
          description: '',
          demand: 10,
          market_type: 'uniform_price',
          experiment_type: 'open',
          duration: 60
        }
        
        await this.loadScenarios()
        this.showAlert('success', 'Scenario created successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to create scenario')
      } finally {
        this.loading = false
      }
    },
    
    async startScenario(scenarioId) {
      try {
        await api.post(`/scenarios/${scenarioId}/start`)
        await this.loadScenarios()
        this.showAlert('success', 'Scenario started successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to start scenario')
      }
    },
    
    async endScenario(scenarioId) {
      try {
        await api.post(`/scenarios/${scenarioId}/end`)
        await this.loadScenarios()
        this.showAlert('success', 'Scenario ended successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to end scenario')
      }
    },
    
    async deleteScenario(scenarioId) {
      if (!confirm('Are you sure you want to delete this scenario?')) return
      
      try {
        await api.delete(`/scenarios/${scenarioId}`)
        await this.loadScenarios()
        this.showAlert('success', 'Scenario deleted successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to delete scenario')
      }
    },
    
    viewResults(scenarioId) {
      this.$router.push(`/results?scenario=${scenarioId}`)
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