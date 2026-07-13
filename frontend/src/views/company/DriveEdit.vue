<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <h3 class="page-title">Edit Drive</h3>

      <div v-if="loading" class="text-center mt-4">
        <div class="spinner-border" role="status"></div>
      </div>

      <div v-else>
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
          <input v-model="form.allowed_departments" type="text" class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Salary Range</label>
          <input v-model="form.salary_range" type="text" class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Location</label>
          <input v-model="form.location" type="text" class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Application Deadline</label>
          <input v-model="form.application_deadline" type="date" class="form-control" />
        </div>

        <button class="btn btn-primary me-2" @click="handleSubmit" :disabled="submitting">
          {{ submitting ? 'Saving...' : 'Save Changes' }}
        </button>
        <RouterLink to="/company/dashboard" class="btn btn-secondary">Cancel</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/api/client'

const route = useRoute()
const router = useRouter()
const driveId = route.params.id

const form = ref({
  job_title: '',
  job_description: '',
  min_cgpa: null,
  allowed_departments: '',
  salary_range: '',
  location: '',
  application_deadline: ''
})

const loading = ref(true)
const submitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get('/api/company/drives')
    const drive = response.data.find(d => d.id === parseInt(driveId))
    if (!drive) {
      errorMessage.value = 'Drive not found.'
      return
    }
    form.value = {
      job_title: drive.job_title || '',
      job_description: drive.job_description || '',
      min_cgpa: drive.min_cgpa,
      allowed_departments: drive.allowed_departments || '',
      salary_range: drive.salary_range || '',
      location: drive.location || '',
      application_deadline: drive.application_deadline || ''
    }
  } catch (e) {
    errorMessage.value = 'Failed to load drive.'
  } finally {
    loading.value = false
  }
})

async function handleSubmit() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!form.value.job_title) {
    errorMessage.value = 'Job title is required.'
    return
  }

  submitting.value = true
  try {
    await apiClient.put(`/api/company/drives/${driveId}`, form.value)
    successMessage.value = 'Drive updated successfully.'
    setTimeout(() => router.push({ name: 'company-dashboard' }), 1500)
  } catch (e) {
    errorMessage.value = e.response?.data?.message || 'Failed to update drive.'
  } finally {
    submitting.value = false
  }
}
</script>