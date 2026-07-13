<template>
  <div class="row justify-content-center">
    <div class="col-md-7">
      <div v-if="loading" class="text-center mt-4">
        <div class="spinner-border" role="status"></div>
      </div>

      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-else>
        <h3 class="page-title">{{ drive.job_title }}</h3>
        <h5 class="text-muted mb-4">{{ drive.company_name }}</h5>

        <table class="table table-bordered mb-4">
          <tbody>
            <tr><th>Location</th><td>{{ drive.location || '—' }}</td></tr>
            <tr><th>Salary</th><td>{{ drive.salary_range || '—' }}</td></tr>
            <tr><th>Min CGPA</th><td>{{ drive.min_cgpa ?? 'None' }}</td></tr>
            <tr><th>Departments</th><td>{{ drive.allowed_departments || 'All' }}</td></tr>
            <tr><th>Deadline</th><td>{{ drive.application_deadline || 'Open' }}</td></tr>
          </tbody>
        </table>

        <div v-if="drive.job_description" class="mb-4">
          <h6>Job Description</h6>
          <p>{{ drive.job_description }}</p>
        </div>

        <div v-if="applySuccess" class="alert alert-success">{{ applySuccess }}</div>
        <div v-if="applyError" class="alert alert-danger">{{ applyError }}</div>

        <button class="btn btn-success me-2" @click="handleApply"
          :disabled="applying || applied">
          {{ applied ? 'Applied' : applying ? 'Applying...' : 'Apply Now' }}
        </button>
        <RouterLink to="/student/drives" class="btn btn-secondary">Back</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/api/client'

const route = useRoute()
const driveId = route.params.id

const drive = ref({})
const loading = ref(true)
const error = ref('')
const applying = ref(false)
const applied = ref(false)
const applySuccess = ref('')
const applyError = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get(`/api/drives/${driveId}`)
    drive.value = response.data
  } catch (e) {
    error.value = 'Drive not found.'
  } finally {
    loading.value = false
  }
})

async function handleApply() {
  applyError.value = ''
  applySuccess.value = ''
  applying.value = true
  try {
    await apiClient.post('/api/student/applications', { drive_id: parseInt(driveId) })
    applySuccess.value = 'Application submitted successfully.'
    applied.value = true
  } catch (e) {
    const status = e.response?.status
    if (status === 409) {
      applyError.value = 'You have already applied to this drive.'
      applied.value = true
    } else if (status === 422) {
      applyError.value = e.response?.data?.message || 'Eligibility check failed.'
    } else {
      applyError.value = 'Failed to apply.'
    }
  } finally {
    applying.value = false
  }
}
</script>