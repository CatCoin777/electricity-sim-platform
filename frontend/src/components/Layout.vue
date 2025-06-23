<template>
  <div class="main-container">
    <div class="container-fluid">
      <div class="row">
        <!-- Sidebar -->
        <div class="col-md-2 sidebar">
          <div class="p-3">
            <h5>Electricity Market Simulation</h5>
            <p class="small">Welcome, {{ currentUser.full_name }}</p>
          </div>
          <nav class="nav flex-column">
            <router-link class="nav-link" to="/dashboard" active-class="active">
              📊 Dashboard
            </router-link>
            <router-link class="nav-link" to="/scenarios" active-class="active">
              📋 Experiment Scenarios
            </router-link>
            <router-link class="nav-link" to="/bidding" active-class="active">
              💰 Submit Bids
            </router-link>
            <router-link class="nav-link" to="/results" active-class="active">
              📈 Results Analysis
            </router-link>
            <router-link class="nav-link" to="/profile" active-class="active">
              👤 Profile Management
            </router-link>
            <router-link v-if="currentUser.role === 'teacher'" class="nav-link" to="/admin" active-class="active">
              ⚙️ Admin Panel
            </router-link>
            <router-link v-if="currentUser.role === 'teacher'" class="nav-link" to="/class-management" active-class="active">
              👥 Class Management
            </router-link>
            <a class="nav-link" @click="logout" style="cursor: pointer;">
              🚪 Logout
            </a>
          </nav>
        </div>

        <!-- Main Content Area -->
        <div class="col-md-10 p-4">
          <slot></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Layout',
  computed: {
    currentUser() {
      const user = localStorage.getItem('currentUser')
      return user ? JSON.parse(user) : {}
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('userRole')
      localStorage.removeItem('currentUser')
      this.$router.push('/login')
    }
  }
}
</script> 