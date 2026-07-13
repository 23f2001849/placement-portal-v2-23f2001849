<template>
  <div>
    <h3 class="page-title">Student Dashboard</h3>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div class="mb-4">
        <h5>Welcome, {{ data.student_name }}</h5>
      </div>

      <div class="row g-3 mb-4">
        <div class="col-md-4">
          <div class="card text-white bg-primary">
            <div class="card-body">
              <h6 class="card-title">Open Drives</h6>
              <h2>{{ data.approved_drives }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-success">
            <div class="card-body">
              <h6 class="card-title">My Applications</h6>
              <h2>{{ data.my_applications }}</h2>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-dark">
            <div class="card-body">
              <h6 class="card-title">Placements</h6>
              <h2>{{ data.my_placements }}</h2>
            </div>
          </div>
        </div>
      </div>

      <div>
        <RouterLink to="/student/drives" class="btn btn-primary me-2">
          Browse Drives
        </RouterLink>
        <RouterLink to="/student/applications" class="btn btn-outline-secondary me-2">
          My Applications
        </RouterLink>
        <RouterLink to="/student/profile" class="btn btn-outline-secondary">
          Edit Profile
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const data = ref({})
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get('/api/student/dashboard')
    data.value = response.data
  } catch (e) {
    error.value = 'Failed to load dashboard.'
  } finally {
    loading.value = false
  }
})
</script>