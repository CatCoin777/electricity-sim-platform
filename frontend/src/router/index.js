import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Scenarios from '../views/Scenarios.vue'
import ScenarioDetail from '../views/ScenarioDetail.vue'
import Bidding from '../views/Bidding.vue'
import Results from '../views/Results.vue'
import Profile from '../views/Profile.vue'
import AdminPanel from '../views/AdminPanel.vue'
import ClassManagement from '../views/ClassManagement.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/scenarios',
    name: 'Scenarios',
    component: Scenarios,
    meta: { requiresAuth: true }
  },
  {
    path: '/scenarios/:id',
    name: 'ScenarioDetail',
    component: ScenarioDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/bidding',
    name: 'Bidding',
    component: Bidding,
    meta: { requiresAuth: true }
  },
  {
    path: '/results',
    name: 'Results',
    component: Results,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: AdminPanel,
    meta: { requiresAuth: true, requiresTeacher: true }
  },
  {
    path: '/class-management',
    name: 'ClassManagement',
    component: ClassManagement,
    meta: { requiresAuth: true, requiresTeacher: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresTeacher && userRole !== 'teacher') {
    next('/dashboard')
  } else {
    next()
  }
})

export default router 