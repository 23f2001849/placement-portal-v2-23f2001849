<template>
  <div class="row justify-content-center mt-5">
    <div class="col-md-4">
      <div class="card shadow-sm">
        <div class="card-body p-4">
          <h4 class="card-title mb-4 text-center">Placement Portal V2</h4>

          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input
              v-model="email"
              type="email"
              class="form-control"
              placeholder="Enter your email"
            />
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input
              v-model="password"
              type="password"
              class="form-control"
              placeholder="Enter your password"
            />
          </div>

          <button
            class="btn btn-primary w-100"
            @click="handleLogin"
            :disabled="loading"
          >
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>

          <p class="text-center mt-3 mb-0">
            Don't have an account?
            <RouterLink to="/register">Register</RouterLink>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

async function handleLogin() {
  errorMessage.value = ''

  if (!email.value || !password.value) {
    errorMessage.value = 'Email and password are required.'
    return
  }

  loading.value = true

  try {
    const data = await authStore.login(email.value, password.value)
    const role = data.role

    if (role === 'admin') {
      router.push({ name: 'admin-dashboard' })
    } else if (role === 'company') {
      router.push({ name: 'company-dashboard' })
    } else if (role === 'student') {
      router.push({ name: 'student-dashboard' })
    }
  } catch (error) {
    const status = error.response?.status
    if (status === 401) {
      errorMessage.value = 'Invalid email or password.'
    } else if (status === 403) {
      errorMessage.value = error.response?.data?.message || 'Access denied.'
    } else {
      errorMessage.value = 'Something went wrong. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>