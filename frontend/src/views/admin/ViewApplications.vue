<template>
  <div>
    <h3 class="page-title">View Applications</h3>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div v-if="applications.length === 0" class="alert alert-info">
        No applications found.
      </div>

      <table v-else class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Student</th>
            <th>Email</th>
            <th>Drive</th>
            <th>Company</th>
            <th>Status</th>
            <th>Remark</th>
            <th>Applied At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.student_name }}</td>
            <td>{{ app.student_id }}</td>
            <td>{{ app.drive_title }}</td>
            <td>{{ app.company_name }}</td>
            <td>
              <span :class="statusBadge(app.status)">
                {{ app.status }}
              </span>
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

async function fetchApplications() {
  loading.value = true
  error.value = ''
  try {
    const response = await apiClient.get('/api/admin/applications')
    applications.value = response.data
  } catch (e) {
    error.value = 'Failed to load applications.'
  } finally {
    loading.value = false
  }
}

function statusBadge(status) {
  return {
    'badge bg-warning text-dark': status === 'applied',
    'badge bg-info text-dark': status === 'shortlisted',
    'badge bg-success': status === 'selected',
    'badge bg-danger': status === 'rejected'
  }
}

onMounted(fetchApplications)
</script>