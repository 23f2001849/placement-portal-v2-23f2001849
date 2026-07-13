<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <h3 class="page-title">Create New Drive</h3>

      <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

      <div class="mb-3">
        <label class="form-label">Job Title *</label>
        <input v-model="form.job_title" type="text" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Job Description</label>
        <textarea v-model="form.job_description" class="form-control" rows="3"></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label">Minimum CGPA</label>
        <input v-model.number="form.min_cgpa" type="number" step="0.1" min="0" max="10" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Allowed Departments (comma-separated)</label>
        <input v-model="form.allowed_departments" type="text" class="form-control" placeholder="CSE,ECE,ME" />
      </div>

      <div class="mb-3">
        <label class="form-label">Salary Range</label>
        <input v-model="form.salary_range" type="text" class="form-control" placeholder="8-12 LPA" />
      </div>

      <div class="mb-3">
        <label class="form-label">Location</label>
        <input v-model="form.location" type="text" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Application Deadline</label>
        <input v-model="form.application_deadline" type="date" class="form-control" />
      </div>

      <button class="btn btn-primary me-2" @click="handleSubmit" :disabled="loading">
        {{ loading ? 'Creating...' : 'Create Drive' }}
      </button>
      <RouterLink to="/company/dashboard" class="btn btn-secondary">Cancel</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'

const router = useRouter()

const form = ref({
  job_title: '',
  job_description: '',
  min_cgpa: null,
  allowed_departments: '',
  salary_range: '',
  location: '',
  application_deadline: ''
})

const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

async function handleSubmit() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!form.value.job_title) {
    errorMessage.value = 'Job title is required.'
    return
  }

  loading.value = true
  try {
    await apiClient.post('/api/company/drives', form.value)
    successMessage.value = 'Drive created successfully. Awaiting admin approval.'
    setTimeout(() => router.push({ name: 'company-dashboard' }), 1500)
  } catch (e) {
    errorMessage.value = e.response?.data?.message || 'Failed to create drive.'
  } finally {
    loading.value = false
  }
}
</script>