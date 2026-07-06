<template>
  <div>
    <h3 class="mb-4">Placement Drives</h3>

    <div class="row g-2 mb-3">
      <div class="col-md-4">
        <input v-model="filters.q" type="text" class="form-control"
          placeholder="Search by title or location" />
      </div>
      <div class="col-md-3">
        <input v-model="filters.department" type="text" class="form-control"
          placeholder="Department (e.g. CSE)" />
      </div>
      <div class="col-md-2">
        <input v-model.number="filters.min_cgpa" type="number" step="0.1"
          class="form-control" placeholder="My CGPA" />
      </div>
      <div class="col-md-2">
        <button class="btn btn-primary w-100" @click="fetchDrives">Search</button>
      </div>
    </div>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div v-if="drives.length === 0" class="alert alert-info">
        No drives found.
      </div>

      <div v-else class="row g-3">
        <div class="col-md-6" v-for="drive in drives" :key="drive.id">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ drive.job_title }}</h5>
              <h6 class="card-subtitle mb-2 text-muted">{{ drive.company_name }}</h6>
              <p class="mb-1"><strong>Location:</strong> {{ drive.location || '—' }}</p>
              <p class="mb-1"><strong>Salary:</strong> {{ drive.salary_range || '—' }}</p>
              <p class="mb-1"><strong>Min CGPA:</strong> {{ drive.min_cgpa ?? 'None' }}</p>
              <p class="mb-1"><strong>Departments:</strong> {{ drive.allowed_departments || 'All' }}</p>
              <p class="mb-1"><strong>Deadline:</strong> {{ drive.application_deadline || 'Open' }}</p>
            </div>
            <div class="card-footer">
              <RouterLink :to="`/student/drives/${drive.id}`"
                class="btn btn-primary btn-sm">
                View & Apply
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const drives = ref([])
const loading = ref(true)
const error = ref('')
const filters = ref({ q: '', department: '', min_cgpa: null })

async function fetchDrives() {
  loading.value = true
  error.value = ''
  try {
    const params = {}
    if (filters.value.q) params.q = filters.value.q
    if (filters.value.department) params.department = filters.value.department
    if (filters.value.min_cgpa) params.min_cgpa = filters.value.min_cgpa
    const response = await apiClient.get('/api/drives', { params })
    drives.value = response.data
  } catch (e) {
    error.value = 'Failed to load drives.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchDrives)
</script>