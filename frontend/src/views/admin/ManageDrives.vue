<template>
  <div>
    <h3 class="page-title">Manage Drives</h3>

    <div class="mb-3">
      <select v-model="statusFilter" class="form-select w-auto d-inline-block me-2">
        <option value="">All</option>
        <option value="pending">Pending</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
        <option value="closed">Closed</option>
      </select>
      <button class="btn btn-outline-secondary btn-sm" @click="fetchDrives">
        Refresh
      </button>
    </div>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div v-if="drives.length === 0" class="alert alert-info">
        No drives found.
      </div>

      <table v-else class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Job Title</th>
            <th>Company</th>
            <th>Min CGPA</th>
            <th>Departments</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in drives" :key="drive.id">
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.company_name }}</td>
            <td>{{ drive.min_cgpa ?? '—' }}</td>
            <td>{{ drive.allowed_departments || 'All' }}</td>
            <td>{{ drive.application_deadline || '—' }}</td>
            <td>
              <span :class="statusBadge(drive.status)">
                {{ drive.status }}
              </span>
            </td>
            <td>
              <button
                v-if="drive.status === 'pending'"
                class="btn btn-success btn-sm me-1"
                @click="confirmAction('approve', drive)"
              >Approve</button>
              <button
                v-if="drive.status === 'pending'"
                class="btn btn-danger btn-sm"
                @click="confirmAction('reject', drive)"
              >Reject</button>
              <span v-if="drive.status !== 'pending'" class="text-muted">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="modal fade" id="driveModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Action</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <p>{{ modalMessage }}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button class="btn btn-danger" @click="executeAction">Confirm</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import apiClient from '@/api/client'

const drives = ref([])
const loading = ref(true)
const error = ref('')
const statusFilter = ref('')
const pendingAction = ref(null)
const pendingDrive = ref(null)
const modalMessage = ref('')
let modalInstance = null

async function fetchDrives() {
  loading.value = true
  error.value = ''
  try {
    const params = statusFilter.value ? { status: statusFilter.value } : {}
    const response = await apiClient.get('/api/admin/drives', { params })
    drives.value = response.data
  } catch (e) {
    error.value = 'Failed to load drives.'
  } finally {
    loading.value = false
  }
}

function statusBadge(status) {
  return {
    'badge bg-warning text-dark': status === 'pending',
    'badge bg-success': status === 'approved',
    'badge bg-danger': status === 'rejected',
    'badge bg-secondary': status === 'closed'
  }
}

function confirmAction(action, drive) {
  pendingAction.value = action
  pendingDrive.value = drive
  modalMessage.value = `Are you sure you want to ${action} "${drive.job_title}"?`

  if (!modalInstance) {
    const el = document.getElementById('driveModal')
    modalInstance = new window.bootstrap.Modal(el)
  }
  modalInstance.show()
}

async function executeAction() {
  modalInstance.hide()
  const { id } = pendingDrive.value
  const action = pendingAction.value

  try {
    await apiClient.put(`/api/admin/drives/${id}/${action}`)
    await fetchDrives()
  } catch (e) {
    error.value = `Failed to ${action} drive.`
  }
}

watch(statusFilter, fetchDrives)
onMounted(fetchDrives)
</script>