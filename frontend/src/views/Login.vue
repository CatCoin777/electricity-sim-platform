<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="text-center mb-4">Electricity Market Simulation Platform</h2>
      
      <!-- Login Form -->
      <form v-if="!showRegister" @submit.prevent="login">
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" class="form-control" v-model="loginForm.username" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" v-model="loginForm.password" required>
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
        <div class="text-center mt-3">
          <a href="#" @click="showRegister = true">Register New User</a>
        </div>
      </form>
      
      <!-- Registration Form -->
      <form v-else @submit.prevent="register">
        <h5 class="mb-3">Register New User</h5>
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input type="text" class="form-control" v-model="registerForm.username" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" v-model="registerForm.password" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" class="form-control" v-model="registerForm.full_name" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Role</label>
          <select class="form-select" v-model="registerForm.role">
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </select>
        </div>
        <button type="submit" class="btn btn-success w-100" :disabled="loading">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
        <button type="button" class="btn btn-link w-100" @click="showRegister = false">
          Back to Login
        </button>
      </form>
      
      <!-- Alert Messages -->
      <div v-if="alert.show" :class="`alert alert-${alert.type} mt-3`" role="alert">
        {{ alert.message }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api.js'

export default {
  name: 'Login',
  data() {
    return {
      showRegister: false,
      loading: false,
      loginForm: {
        username: '',
        password: ''
      },
      registerForm: {
        username: '',
        password: '',
        full_name: '',
        role: 'student'
      },
      alert: {
        show: false,
        type: 'success',
        message: ''
      }
    }
  },
  methods: {
    async login() {
      this.loading = true
      try {
        const response = await api.post('/auth/login', this.loginForm)
        const { access_token, role } = response.data
        
        // 创建用户对象，使用后端返回的角色
        const user = {
          username: this.loginForm.username,
          role: role
        }
        
        localStorage.setItem('token', access_token)
        localStorage.setItem('userRole', role)
        localStorage.setItem('currentUser', JSON.stringify(user))
        
        this.$router.push('/dashboard')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Login failed')
      } finally {
        this.loading = false
      }
    },
    
    async register() {
      this.loading = true
      try {
        await api.post('/auth/register', this.registerForm)
        this.showAlert('success', 'Registration successful! Please login.')
        this.showRegister = false
        this.registerForm = {
          username: '',
          password: '',
          full_name: '',
          role: 'student'
        }
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Registration failed')
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