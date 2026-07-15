<template>
  <div>
    <h3 class="page-title">My Applications</h3>

    <div class="mb-3 d-flex align-items-center gap-2">
      <button class="btn btn-outline-primary btn-sm" @click="triggerExport" :disabled="exporting">
        {{ exporting ? 'Exporting...' : 'Export as CSV' }}
      </button>
      <span v-if="exportStatus === 'completed'">
        <a :href="`/api/exports/${exportId}/download`" class="btn btn-success btn-sm">
          Download CSV
        </a>
      </span>
      <span v-if="exportStatus === 'failed'" class="text-danger small">
        Export failed. Try again.
      </span>
    </div>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div v-if="applications.length === 0" class="alert alert-info">
        No applications yet.
      </div>

      <table v-else class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Drive</th>
            <th>Company</th>
            <th>Status</th>
            <th>Remark</th>
            <th>Applied At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.drive_title }}</td>
            <td>{{ app.company_name }}</td>
            <td>
              <span :class="statusBadge(app.status)">{{ app.status }}</span>
            </td>
            <td>{{ app.remark || '—' }}</td>
            <td>{{ new Date(app.applied_at).toLocaleDateString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const applications = ref([])
const loading = ref(true)
const error = ref('')

const exporting = ref(false)
const exportId = ref(null)
const exportStatus = ref('')
let pollInterval = null

function statusBadge(status) {
  return {
    'badge bg-warning text-dark': status === 'applied',
    'badge bg-info text-dark': status === 'shortlisted',
    'badge bg-success': status === 'selected',
    'badge bg-danger': status === 'rejected'
  }
}

onMounted(async () => {
  try {
    const response = await apiClient.get('/api/student/applications')
    applications.value = response.data
  } catch (e) {
    error.value = 'Failed to load applications.'
  } finally {
    loading.value = false
  }
})

async function triggerExport() {
  exporting.value = true
  exportStatus.value = ''
  try {
    const response = await apiClient.post('/api/exports/applications')
    exportId.value = response.data.export_id
    pollInterval = setInterval(pollExport, 2000)
  } catch (e) {
    exporting.value = false
    exportStatus.value = 'failed'
  }
}

async function pollExport() {
  try {
    const response = await apiClient.get(`/api/exports/${exportId.value}`)
    exportStatus.value = response.data.status
    if (response.data.status === 'completed' || response.data.status === 'failed') {
      clearInterval(pollInterval)
      exporting.value = false
    }
  } catch (e) {
    clearInterval(pollInterval)
    exporting.value = false
  }
}
</script>