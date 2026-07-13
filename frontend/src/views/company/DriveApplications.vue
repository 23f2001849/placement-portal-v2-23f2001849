<template>
  <div>
    <h3 class="page-title">Drive Applications</h3>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div v-if="applications.length === 0" class="alert alert-info">
        No applications yet for this drive.
      </div>

      <table v-else class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Name</th>
            <th>Roll No</th>
            <th>Department</th>
            <th>CGPA</th>
            <th>Status</th>
            <th>Remark</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.student_name }}</td>
            <td>{{ app.roll_number || '—' }}</td>
            <td>{{ app.department || '—' }}</td>
            <td>{{ app.cgpa ?? '—' }}</td>
            <td>
              <span :class="statusBadge(app.status)">{{ app.status }}</span>
            </td>
            <td>{{ app.remark || '—' }}</td>
            <td>
              <div v-if="app.status === 'applied'">
                <button class="btn btn-info btn-sm me-1"
                  @click="updateStatus(app.id, 'shortlisted')">Shortlist</button>
                <button class="btn btn-danger btn-sm"
                  @click="updateStatus(app.id, 'rejected')">Reject</button>
              </div>
              <div v-else-if="app.status === 'shortlisted'">
                <button class="btn btn-success btn-sm me-1"
                  @click="updateStatus(app.id, 'selected')">Select</button>
                <button class="btn btn-danger btn-sm"
                  @click="updateStatus(app.id, 'rejected')">Reject</button>
              </div>
              <span v-else class="text-muted">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <RouterLink to="/company/dashboard" class="btn btn-secondary mt-3">
      Back to Dashboard
    </RouterLink>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import apiClient from '@/api/client'

const route = useRoute()
const driveId = route.params.id

const applications = ref([])
const loading = ref(true)
const error = ref('')

async function fetchApplications() {
  loading.value = true
  error.value = ''
  try {
    const response = await apiClient.get(`/api/company/drives/${driveId}/applications`)
    applications.value = response.data
  } catch (e) {
    error.value = 'Failed to load applications.'
  } finally {
    loading.value = false
  }
}

async function updateStatus(applicationId, newStatus) {
  try {
    await apiClient.put(`/api/company/applications/${applicationId}/status`, {
      status: newStatus
    })
    await fetchApplications()
  } catch (e) {
    error.value = e.response?.data?.message || 'Failed to update status.'
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