<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <h3 class="mb-4">Company Profile</h3>

      <div v-if="loading" class="text-center mt-4">
        <div class="spinner-border" role="status"></div>
      </div>

      <div v-else>
        <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
        <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

        <div class="mb-3">
          <label class="form-label">Company Name</label>
          <input v-model="form.name" type="text" class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Industry</label>
          <input v-model="form.industry" type="text" class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Website</label>
          <input v-model="form.website" type="text" class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">HR Contact</label>
          <input v-model="form.hr_contact" type="text" class="form-control" />
        </div>

        <div class="mb-3">
          <label class="form-label">Description</label>
          <textarea v-model="form.description" class="form-control" rows="3"></textarea>
        </div>

        <button class="btn btn-primary me-2" @click="handleSave" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Profile' }}
        </button>
        <RouterLink to="/company/dashboard" class="btn btn-secondary">Cancel</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import apiClient from '@/api/client'

const form = ref({
  name: '',
  industry: '',
  website: '',
  hr_contact: '',
  description: ''
})

const loading = ref(true)
const saving = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

onMounted(async () => {
  try {
    const response = await apiClient.get('/api/company/profile')
    const p = response.data
    form.value = {
      name: p.name || '',
      industry: p.industry || '',
      website: p.website || '',
      hr_contact: p.hr_contact || '',
      description: p.description || ''
    }
  } catch (e) {
    errorMessage.value = 'Failed to load profile.'
  } finally {
    loading.value = false
  }
})

async function handleSave() {
  errorMessage.value = ''
  successMessage.value = ''
  saving.value = true
  try {
    await apiClient.put('/api/company/profile', form.value)
    successMessage.value = 'Profile saved successfully.'
  } catch (e) {
    errorMessage.value = 'Failed to save profile.'
  } finally {
    saving.value = false
  }
}
</script>