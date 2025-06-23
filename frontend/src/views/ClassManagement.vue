<template>
  <Layout>
    <div>
      <h2>Class Management</h2>
      
      <!-- Create New Class -->
      <div class="result-card mb-4">
        <h5>{{ editingClass ? 'Edit Class' : 'Create New Class' }}</h5>
        <form @submit.prevent="editingClass ? saveClassEdit() : createClass()">
          <div class="row">
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label">Class Name</label>
                <input type="text" class="form-control" v-model="classForm.name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="classForm.description" rows="3" placeholder="(optional)"></textarea>
              </div>
            </div>
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label">Max Students</label>
                <input type="number" class="form-control" v-model="classForm.max_students" min="1">
              </div>
              <div class="mb-3">
                <label class="form-label">Academic Year</label>
                <input type="text" class="form-control" v-model="classForm.academic_year" placeholder="e.g., 2024-2025">
              </div>
            </div>
          </div>
          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? (editingClass ? 'Updating...' : 'Creating...') : (editingClass ? 'Update Class' : 'Create Class') }}
            </button>
            <button 
              v-if="editingClass" 
              type="button" 
              class="btn btn-secondary" 
              @click="cancelEdit"
              :disabled="loading"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      <!-- Class List -->
      <div class="result-card mb-4">
        <h5>My Classes</h5>
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Class Name</th>
                <th>Students</th>
                <th>Max Students</th>
                <th>Academic Year</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="classItem in classes" :key="classItem.id">
                <td>{{ classItem.name }}</td>
                <td>{{ classItem.student_count || 0 }}</td>
                <td>{{ classItem.max_students || 'Unlimited' }}</td>
                <td>{{ classItem.academic_year || '-' }}</td>
                <td>{{ formatDate(classItem.created_at) }}</td>
                <td>
                  <button 
                    class="btn btn-info btn-sm me-2"
                    @click="viewClassDetails(classItem.id)"
                  >
                    View Details
                  </button>
                  <button 
                    class="btn btn-warning btn-sm me-2"
                    @click="editClass(classItem)"
                    :disabled="editingClass"
                  >
                    Edit
                  </button>
                  <button 
                    class="btn btn-danger btn-sm"
                    @click="deleteClass(classItem.id)"
                    :disabled="editingClass"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Class Details Modal -->
      <div v-if="selectedClass" class="result-card">
        <h5>Class Details: {{ selectedClass.name }}</h5>
        
        <!-- Add Student -->
        <div class="mb-4">
          <h6>Add Student</h6>
          <div class="row">
            <div class="col-md-6">
              <div class="mb-3">
                <label class="form-label">Student Username</label>
                <input type="text" class="form-control" v-model="addStudentForm.username" placeholder="Enter student username">
              </div>
            </div>
            <div class="col-md-6">
              <button 
                class="btn btn-success mt-4"
                @click="addStudentToClass"
                :disabled="!addStudentForm.username"
              >
                Add Student
              </button>
            </div>
          </div>
        </div>

        <!-- Student List -->
        <div>
          <h6>Students in Class</h6>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Full Name</th>
                  <th>Email</th>
                  <th>Joined</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in selectedClass.students" :key="student.id">
                  <td>{{ student.username }}</td>
                  <td>{{ student.full_name }}</td>
                  <td>{{ student.email || '-' }}</td>
                  <td>{{ formatDate(student.joined_at) }}</td>
                  <td>
                    <button 
                      class="btn btn-danger btn-sm"
                      @click="removeStudentFromClass(student.id)"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
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
  name: 'ClassManagement',
  components: {
    Layout
  },
  data() {
    return {
      loading: false,
      classes: [],
      selectedClass: null,
      editingClass: null,
      classForm: {
        name: '',
        description: '',
        max_students: '',
        academic_year: ''
      },
      addStudentForm: {
        username: ''
      },
      alert: {
        show: false,
        type: 'success',
        message: ''
      }
    }
  },
  async mounted() {
    await this.loadClasses()
  },
  methods: {
    async loadClasses() {
      try {
        const response = await api.get('/classes/')
        this.classes = response.data
      } catch (error) {
        console.error('Error loading classes:', error)
      }
    },
    
    async createClass() {
      this.loading = true
      try {
        await api.post('/classes/', this.classForm)
        
        // Reset form
        this.classForm = {
          name: '',
          description: '',
          max_students: '',
          academic_year: ''
        }
        
        await this.loadClasses()
        this.showAlert('success', 'Class created successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to create class')
      } finally {
        this.loading = false
      }
    },
    
    async viewClassDetails(classId) {
      try {
        const response = await api.get(`/classes/${classId}`)
        this.selectedClass = response.data
      } catch (error) {
        console.error('Error loading class details:', error)
      }
    },
    
    async addStudentToClass() {
      if (!this.selectedClass || !this.addStudentForm.username) return
      
      try {
        await api.post(`/classes/${this.selectedClass.id}/add-student`, {
          username: this.addStudentForm.username
        })
        
        this.addStudentForm.username = ''
        await this.viewClassDetails(this.selectedClass.id)
        this.showAlert('success', 'Student added to class successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to add student')
      }
    },
    
    async removeStudentFromClass(studentId) {
      if (!this.selectedClass) return
      
      if (!confirm('Are you sure you want to remove this student from the class?')) return
      
      try {
        await api.delete(`/classes/${this.selectedClass.id}/remove-student/${studentId}`)
        await this.viewClassDetails(this.selectedClass.id)
        this.showAlert('success', 'Student removed from class successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to remove student')
      }
    },
    
    editClass(classItem) {
      this.editingClass = { ...classItem }
      this.classForm = {
        name: classItem.class_name || classItem.name,
        description: classItem.description || '',
        max_students: classItem.max_students || '',
        academic_year: classItem.academic_year || ''
      }
    },
    
    async saveClassEdit() {
      if (!this.editingClass) return
      
      this.loading = true
      try {
        await api.put(`/classes/${this.editingClass.id}`, this.classForm)
        
        // Reset form and editing state
        this.classForm = {
          name: '',
          description: '',
          max_students: '',
          academic_year: ''
        }
        this.editingClass = null
        
        await this.loadClasses()
        this.showAlert('success', 'Class updated successfully!')
      } catch (error) {
        this.showAlert('danger', error.response?.data?.detail || 'Failed to update class')
      } finally {
        this.loading = false
      }
    },
    
    cancelEdit() {
      this.editingClass = null
      this.classForm = {
        name: '',
        description: '',
        max_students: '',
        academic_year: ''
      }
    },
    
    async deleteClass(classId) {
      if (!confirm('Are you sure you want to delete this class?')) return
      
      try {
        console.log('Deleting class:', classId)
        const response = await api.delete(`/classes/${classId}`)
        console.log('Delete response:', response.data)
        
        // Clear selected class if it's the one being deleted
        if (this.selectedClass && this.selectedClass.id === classId) {
          this.selectedClass = null
        }
        
        // Clear editing class if it's the one being deleted
        if (this.editingClass && this.editingClass.id === classId) {
          this.editingClass = null
          this.classForm = {
            name: '',
            description: '',
            max_students: '',
            academic_year: ''
          }
        }
        
        // Reload classes list
        await this.loadClasses()
        this.showAlert('success', 'Class deleted successfully!')
      } catch (error) {
        console.error('Error deleting class:', error)
        this.showAlert('danger', error.response?.data?.detail || 'Failed to delete class')
      }
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