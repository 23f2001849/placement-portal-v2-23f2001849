<template>
  <div>
    <h3 class="mb-4">Manage Students</h3>

    <div class="mb-3">
      <input
        v-model="searchQuery"
        type="text"
        class="form-control w-auto d-inline-block me-2"
        placeholder="Search by name, roll, email"
      />
      <button class="btn btn-outline-secondary btn-sm" @click="fetchStudents">
        Search
      </button>
    </div>

    <div v-if="loading" class="text-center mt-4">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-else>
      <div v-if="students.length === 0" class="alert alert-info">
        No students found.
      </div>

      <table v-else class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Roll Number</th>
            <th>Department</th>
            <th>CGPA</th>
            <th>Blacklisted</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in students" :key="student.id">
            <td>{{ student.name }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.roll_number || '—' }}</td>
            <td>{{ student.department || '—' }}</td>
            <td>{{ student.cgpa ?? '—' }}</td>
            <td>
              <span v-if="student.is_blacklisted" class="badge bg-dark">Yes</span>
              <span v-else class="badge bg-secondary">No</span>
            </td>
            <td>
              <button
                v-if="!student.is_blacklisted"
                class="btn btn-danger btn-sm"
                @click="confirmBlacklist(student)"
              >Blacklist</button>
              <span v-else class="text-muted">—</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Confirm Modal -->
    <div class="modal fade" id="studentModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Blacklist</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <p>{{ modalMessage }}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button class="btn btn-danger" @click="executeBlacklist">Confirm</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const students = ref([])
const loading = ref(true)
const error = ref('')
const searchQuery = ref('')
const pendingStudent = ref(null)
const modalMessage = ref('')
let modalInstance = null

async function fetchStudents() {
  loading.value = true
  error.value = ''
  try {
    const params = searchQuery.value ? { q: searchQuery.value } : {}
    const response = await apiClient.get('/api/admin/students', { params })
    students.value = response.data
  } catch (e) {
    error.value = 'Failed to load students.'
  } finally {
    loading.value = false
  }
}

function confirmBlacklist(student) {
  pendingStudent.value = student
  modalMessage.value = `Are you sure you want to blacklist "${student.name}"?`

  if (!modalInstance) {
    const el = document.getElementById('studentModal')
    modalInstance = new window.bootstrap.Modal(el)
  }
  modalInstance.show()
}

async function executeBlacklist() {
  modalInstance.hide()
  try {
    await apiClient.put(`/api/admin/students/${pendingStudent.value.id}/blacklist`)
    await fetchStudents()
  } catch (e) {
    error.value = 'Failed to blacklist student.'
  }
}

onMounted(fetchStudents)
</script>