<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-5">
      <div class="card shadow-sm">
        <div class="card-body p-4">
          <h4 class="card-title mb-4 text-center">Create Account</h4>

          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
          </div>

          <div v-if="successMessage" class="alert alert-success">
            {{ successMessage }}
          </div>

          <div class="mb-3">
            <label class="form-label">Register as</label>
            <select v-model="role" class="form-select">
              <option value="student">Student</option>
              <option value="company">Company</option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">
              {{ role === 'company' ? 'Company Name' : 'Full Name' }}
            </label>
            <input
              v-model="name"
              type="text"
              class="form-control"
              placeholder="Enter name"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="Enter email"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="Enter password"
            />
          </div>

          <button
            class="btn btn-success w-100"
            @click="handleRegister"
            :disabled="loading"
          >
            {{ loading ? 'Registering...' : 'Register' }}
          </button>

          <p class="text-center mt-3 mb-0">
            Already have an account?
            <RouterLink to="/login">Login</RouterLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'

const router = useRouter()

const role = ref('student')
const name = ref('')
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const loading = ref(false)

async function handleRegister() {
  errorMessage.value = ''
  successMessage.value = ''

  if (!name.value || !email.value || !password.value) {
    errorMessage.value = 'All fields are required.'
    return
  }

  if (password.value.length < 4) {
    errorMessage.value = 'Password must be at least 4 characters.'
    return
  }

  loading.value = true

  try {
    const endpoint = role.value === 'student'
      ? '/api/register/student'
      : '/api/register/company'

    await apiClient.post(endpoint, {
      name: name.value,
      email: email.value,
      password: password.value
    })

    if (role.value === 'student') {
      successMessage.value = 'Registration successful! You can now login.'
    } else {
      successMessage.value = 'Registration successful! Wait for admin approval before logging in.'
    }

    name.value = ''
    email.value = ''
    password.value = ''

  } catch (error) {
    const status = error.response?.status
    if (status === 409) {
      errorMessage.value = 'This email is already registered.'
    } else if (status === 400) {
      errorMessage.value = error.response?.data?.message || 'Invalid input.'
    } else {
      errorMessage.value = 'Something went wrong. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>