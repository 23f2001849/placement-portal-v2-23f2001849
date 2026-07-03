<template>
  <div>
    <h3 class="mb-4">Manage Companies</h3>

    <div class="mb-3">
      <select v-model="statusFilter" class="form-select w-auto d-inline-block me-2">
        <option value="">All</option>
        <option value="pending">Pending</option>
        <option value="approved">Approved</option>
        <option value="rejected">Rejected</option>
      </select>
      <button class="btn btn-outline-secondary btn-sm" @click="fetchCompanies">
        Refresh
      </button>
    </div>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div v-if="companies.length === 0" class="alert alert-info">
        No companies found.
      </div>

      <table v-else class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Industry</th>
            <th>Status</th>
            <th>Blacklisted</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in companies" :key="company.id">
            <td>{{ company.name }}</td>
            <td>{{ company.email }}</td>
            <td>{{ company.industry || '—' }}</td>
            <td>
              <span :class="statusBadge(company.approval_status)">
                {{ company.approval_status }}
              </span>
            </td>
            <td>
              <span v-if="company.is_blacklisted" class="badge bg-dark">Yes</span>
              <span v-else class="badge bg-secondary">No</span>
            </td>
            <td>
              <button
                v-if="company.approval_status === 'pending'"
                class="btn btn-success btn-sm me-1"
                @click="confirmAction('approve', company)"
              >Approve</button>
              <button
                v-if="company.approval_status === 'pending'"
                class="btn btn-warning btn-sm me-1"
                @click="confirmAction('reject', company)"
              >Reject</button>
              <button
                v-if="!company.is_blacklisted"
                class="btn btn-danger btn-sm"
                @click="confirmAction('blacklist', company)"
              >Blacklist</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Confirm Modal -->
    <div class="modal fade" id="confirmModal" tabindex="-1">
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

const companies = ref([])
const loading = ref(true)
const error = ref('')
const statusFilter = ref('')
const pendingAction = ref(null)
const pendingCompany = ref(null)
const modalMessage = ref('')
let modalInstance = null

async function fetchCompanies() {
  loading.value = true
  error.value = ''
  try {
    const params = statusFilter.value ? { status: statusFilter.value } : {}
    const response = await apiClient.get('/api/admin/companies', { params })
    companies.value = response.data
  } catch (e) {
    error.value = 'Failed to load companies.'
  } finally {
    loading.value = false
  }
}

function statusBadge(status) {
  return {
    'badge bg-warning text-dark': status === 'pending',
    'badge bg-success': status === 'approved',
    'badge bg-danger': status === 'rejected'
  }
}

function confirmAction(action, company) {
  pendingAction.value = action
  pendingCompany.value = company
  modalMessage.value = `Are you sure you want to ${action} "${company.name}"?`

  if (!modalInstance) {
    const el = document.getElementById('confirmModal')
    modalInstance = new window.bootstrap.Modal(el)
  }
  modalInstance.show()
}

async function executeAction() {
  modalInstance.hide()
  const { id } = pendingCompany.value
  const action = pendingAction.value

  try {
    await apiClient.put(`/api/admin/companies/${id}/${action}`)
    await fetchCompanies()
  } catch (e) {
    error.value = `Failed to ${action} company.`
  }
}

watch(statusFilter, fetchCompanies)
onMounted(fetchCompanies)
</script>