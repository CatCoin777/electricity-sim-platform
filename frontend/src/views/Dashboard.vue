<template>
  <Layout>
    <div>
      <h2>Dashboard</h2>
      <div class="row">
        <div class="col-md-3">
          <div class="result-card text-center">
            <h4>{{ scenarios.length }}</h4>
            <p>Available Scenarios</p>
          </div>
        </div>
        <div class="col-md-3">
          <div class="result-card text-center">
            <h4>{{ myBids.length }}</h4>
            <p>My Bids</p>
          </div>
        </div>
        <div class="col-md-3">
          <div class="result-card text-center">
            <h4>{{ completedScenarios.length }}</h4>
            <p>Completed</p>
          </div>
        </div>
        <div class="col-md-3">
          <div class="result-card text-center">
            <h4>{{ totalProfit.toFixed(2) }}</h4>
            <p>Total Profit</p>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="row mt-4">
        <div class="col-md-6">
          <div class="result-card">
            <h5>Recent Scenarios</h5>
            <div v-for="scenario in recentScenarios" :key="scenario.id" class="mb-2 p-2 border-bottom">
              <strong>{{ scenario.name }}</strong>
              <br>
              <small class="text-muted">{{ scenario.description }}</small>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="result-card">
            <h5>Recent Bids</h5>
            <div v-for="bid in recentBids" :key="bid.id" class="mb-2 p-2 border-bottom">
              <strong>Bid: ${{ bid.price }}</strong>
              <br>
              <small class="text-muted">{{ bid.scenario_name }}</small>
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
  name: 'Dashboard',
  components: {
    Layout
  },
  data() {
    return {
      scenarios: [],
      myBids: [],
      completedScenarios: [],
      totalProfit: 0
    }
  },
  computed: {
    recentScenarios() {
      return this.scenarios.slice(0, 5)
    },
    recentBids() {
      return this.myBids.slice(0, 5)
    }
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      try {
        const [scenariosRes, bidsRes] = await Promise.all([
          api.get('/scenarios/'),
          api.get('/bids/my-bids')
        ])
        
        this.scenarios = scenariosRes.data
        this.myBids = bidsRes.data
        
        // Calculate completed scenarios and total profit
        this.completedScenarios = this.scenarios.filter(s => s.status === 'completed')
        this.totalProfit = this.myBids.reduce((sum, bid) => sum + (bid.profit || 0), 0)
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      }
    }
  }
}
</script> 