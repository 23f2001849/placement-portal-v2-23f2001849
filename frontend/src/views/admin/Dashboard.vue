<template>
  <div>
    <h3 class="mb-4">Admin Dashboard</h3>

    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else class="row g-3">
      <div class="col-md-3">
        <div class="card text-white bg-primary">
          <div class="card-body">
            <h6 class="card-title">Students</h6>
            <h2>{{ stats.total_students }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-success">
          <div class="card-body">
            <h6 class="card-title">Companies</h6>
            <h2>{{ stats.total_companies }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-warning">
          <div class="card-body">
            <h6 class="card-title">Drives</h6>
            <h2>{{ stats.total_drives }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-danger">
          <div class="card-body">
            <h6 class="card-title">Applications</h6>
            <h2>{{ stats.total_applications }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-3">
        <div class="card text-white bg-dark">
          <div class="card-body">
            <h6 class="card-title">Placements</h6>
            <h2>{{ stats.total_placements }}</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-4">
      <RouterLink to="/admin/companies" class="btn btn-outline-primary me-2">
        Manage Companies
      </RouterLink>
      <RouterLink to="/admin/students" class="btn btn-outline-secondary me-2">
        Manage Students
      </RouterLink>
      <RouterLink to="/admin/drives" class="btn btn-outline-warning me-2">
        Manage Drives
      </RouterLink>
      <RouterLink to="/admin/applications" class="btn btn-outline-danger">
        View Applications
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const stats = ref({})
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get('/api/admin/dashboard')
    stats.value = response.data
  } catch (e) {
    error.value = 'Failed to load dashboard stats.'
  } finally {
    loading.value = false
  }
})
</script>