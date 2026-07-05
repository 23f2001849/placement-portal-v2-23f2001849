<template>
  <div>
    <h3 class="mb-4">Company Profile</h3>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div class="mb-4">
        <h5>{{ data.company_name }}</h5>
        <span class="badge bg-success">{{ data.approval_status }}</span>
        <span class="ms-3 text-muted">Total Drives: {{ data.total_drives }}</span>
      </div>

      <div class="mb-3">
        <RouterLink to="/company/drives/create" class="btn btn-primary me-2">
          Create New Drive
        </RouterLink>
        <RouterLink to="/company/profile" class="btn btn-outline-secondary">
          Edit Profile
        </RouterLink>
      </div>

      <div v-if="data.drives && data.drives.length === 0" class="alert alert-info">
        No drives created yet.
      </div>

      <table v-else class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Job Title</th>
            <th>Status</th>
            <th>Applicants</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in data.drives" :key="drive.id">
            <td>{{ drive.job_title }}</td>
            <td>
              <span :class="statusBadge(drive.status)">{{ drive.status }}</span>
            </td>
            <td>{{ drive.applicant_count }}</td>
            <td>
              <RouterLink
                v-if="drive.status === 'pending'"
                :to="`/company/drives/${drive.id}/edit`"
                class="btn btn-warning btn-sm me-1"
              >Edit</RouterLink>
              <RouterLink
                :to="`/company/drives/${drive.id}/applications`"
                class="btn btn-info btn-sm"
              >Applications</RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const data = ref({})
const loading = ref(true)
const error = ref('')

function statusBadge(status) {
  return {
    'badge bg-warning text-dark': status === 'pending',
    'badge bg-success': status === 'approved',
    'badge bg-danger': status === 'rejected',
    'badge bg-secondary': status === 'closed'
  }
}

onMounted(async () => {
  try {
    const response = await apiClient.get('/api/company/dashboard')
    data.value = response.data
  } catch (e) {
    error.value = 'Failed to load dashboard.'
  } finally {
    loading.value = false
  }
})
</script>