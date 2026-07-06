<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <h3 class="mb-4">Student Profile</h3>

      <div v-if="loading" class="text-center mt-4">
        <div class="spinner-border" role="status"></div>
      </div>

      <div v-else>
        <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
        <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input v-model="form.name" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Roll Number</label>
          <input v-model="form.roll_number" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Department</label>
          <input v-model="form.department" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">CGPA</label>
          <input v-model.number="form.cgpa" type="number" step="0.1" min="0" max="10" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Phone</label>
          <input v-model="form.phone" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Year of Study</label>
          <input v-model.number="form.year_of_study" type="number" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Skills (comma-separated)</label>
          <input v-model="form.skills" type="text" class="form-control" />
        </div>
        <div class="mb-3">
          <label class="form-label">Education</label>
          <textarea v-model="form.education" class="form-control" rows="2"></textarea>
        </div>

        <hr />
        <h6 class="mb-3">Resume Upload (PDF, max 2MB)</h6>
        <div v-if="form.resume_path" class="mb-2 text-success">
          Resume on file: {{ form.resume_path }}
        </div>
        <div class="mb-3">
          <input type="file" accept=".pdf" class="form-control" @change="onFileChange" />
        </div>
        <button v-if="resumeFile" class="btn btn-outline-primary btn-sm mb-3"
          @click="uploadResume" :disabled="uploading">
          {{ uploading ? 'Uploading...' : 'Upload Resume' }}
        </button>

        <div class="d-block">
          <button class="btn btn-primary me-2" @click="handleSave" :disabled="saving">
            {{ saving ? 'Saving...' : 'Save Profile' }}
          </button>
          <RouterLink to="/student/dashboard" class="btn btn-secondary">Cancel</RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const form = ref({
  name: '', roll_number: '', department: '', cgpa: null,
  phone: '', year_of_study: null, skills: '', education: '', resume_path: ''
})

const loading = ref(true)
const saving = ref(false)
const uploading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const resumeFile = ref(null)

onMounted(async () => {
  try {
    const response = await apiClient.get('/api/student/profile')
    const p = response.data
    form.value = {
      name: p.name || '',
      roll_number: p.roll_number || '',
      department: p.department || '',
      cgpa: p.cgpa,
      phone: p.phone || '',
      year_of_study: p.year_of_study,
      skills: p.skills || '',
      education: p.education || '',
      resume_path: p.resume_path || ''
    }
  } catch (e) {
    errorMessage.value = 'Failed to load profile.'
  } finally {
    loading.value = false
  }
})

function onFileChange(event) {
  resumeFile.value = event.target.files[0] || null
}

async function uploadResume() {
  if (!resumeFile.value) return
  uploading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const formData = new FormData()
    formData.append('resume', resumeFile.value)
    const response = await apiClient.post('/api/student/profile/resume', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    form.value.resume_path = response.data.resume_path
    successMessage.value = 'Resume uploaded successfully.'
  } catch (e) {
    errorMessage.value = e.response?.data?.message || 'Upload failed.'
  } finally {
    uploading.value = false
  }
}

async function handleSave() {
  errorMessage.value = ''
  successMessage.value = ''
  saving.value = true
  try {
    await apiClient.put('/api/student/profile', form.value)
    successMessage.value = 'Profile saved successfully.'
  } catch (e) {
    errorMessage.value = 'Failed to save profile.'
  } finally {
    saving.value = false
  }
}
</script>