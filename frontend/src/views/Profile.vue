<template>
  <Layout>
    <div>
      <h2>Profile Management</h2>
      
      <div class="row">
        <!-- Profile Information -->
        <div class="col-md-6">
          <div class="result-card">
            <h5>Profile Information</h5>
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label class="form-label">Username</label>
                <input type="text" class="form-control" v-model="profileForm.username" readonly>
              </div>
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" class="form-control" v-model="profileForm.full_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" v-model="profileForm.email">
              </div>
              <div class="mb-3">
                <label class="form-label">Role</label>
                <input type="text" class="form-control" v-model="profileForm.role" readonly>
              </div>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                {{ loading ? 'Updating...' : 'Update Profile' }}
              </button>
            </form>
          </div>
        </div>

        <!-- Change Password -->
        <div class="col-md-6">
          <div class="result-card">
            <h5>Change Password</h5>
            <form @submit.prevent="changePassword">
              <div class="mb-3">
                <label class="form-label">Current Password</label>
                <input type="password" class="form-control" v-model="passwordForm.current_password" required>
              </div>
              <div class="mb-3">
                <label class="form-label">New Password</label>
                <input type="password" class="form-control" v-model="passwordForm.new_password" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Confirm New Password</label>
                <input type="password" class="form-control" v-model="passwordForm.confirm_password" required>
              </div>
              <button type="submit" class="btn btn-warning" :disabled="loading">
                {{ loading ? 'Changing...' : 'Change Password' }}
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Statistics -->
      <div class="row mt-4">
        <div class="col-md-12">
          <div class="result-card">
            <h5>My Statistics</h5>
            <div class="row">
              <div class="col-md-3">
                <div class="text-center">
                  <h4>{{ statistics.totalBids }}</h4>
                  <p>Total Bids</p>
                </div>
              </div>
              <div class="col-md-3">
                <div class="text-center">
                  <h4>{{ statistics.acceptedBids }}</h4>
                  <p>Accepted Bids</p>
                </div>
              </div>
              <div class="col-md-3">
                <div class="text-center">
                  <h4>${{ statistics.totalRevenue.toFixed(2) }}</h4>
                  <p>Total Revenue</p>
                </div>
              </div>
              <div class="col-md-3">
                <div class="text-center">
                  <h4>{{ statistics.participatedScenarios }}</h4>
                  <p>Scenarios Participated</p>
                </div>
              </div>
            </div>
          </div>
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
  name: 'Profile',
  components: {
    Layout
  },
  data() {
    return {
      loading: false,
      profileForm: {
        username: '',
        full_name: '',
        email: '',
        role: ''
      },
      passwordForm: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      },
      statistics: {
        totalBids: 0,
        acceptedBids: 0,
        totalRevenue: 0,
        participatedScenarios: 0
      },
      alert: {
        show: false,
        type: 'success',
        message: ''
      }
    }
  },
  async mounted() {
    await this.loadProfile()
    await this.loadStatistics()
  },
  methods: {
    async loadProfile() {
      try {
        const response = await api.get('/users/profile')
        const user = response.data
        
        this.profileForm = {
          username: user.username,
          full_name: user.full_name,
          email: user.email || '',
          role: user.role
        }
      } catch (error) {
        console.error('Error loading profile:', error)
      }
    },
    
    async loadStatistics() {
      try {
        const response = await api.get('/users/statistics')
        this.statistics = response.data
      } catch (error) {
        console.error('Error loading statistics:', error)
      }
    },
    
    async updateProfile() {
      this.loading = true
      try {
        await api.put('/users/profile', {
          full_name: this.profileForm.full_name,
          email: this.profileForm.email
        })
        
        // Update local storage
        const currentUser = JSON.parse(localStorage.getItem('currentUser'))
        currentUser.full_name = this.profileForm.full_name
        currentUser.email = this.profileForm.email
        localStorage.setItem('currentUser', JSON.stringify(currentUser))
        
        this.showAlert('success', 'Profile updated successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to update profile')
      } finally {
        this.loading = false
      }
    },
    
    async changePassword() {
      if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        this.showAlert('danger', 'New passwords do not match')
        return
      }
      
      this.loading = true
      try {
        await api.put('/users/change-password', {
          current_password: this.passwordForm.current_password,
          new_password: this.passwordForm.new_password
        })
        
        this.passwordForm = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        }
        
        this.showAlert('success', 'Password changed successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to change password')
      } finally {
        this.loading = false
      }
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