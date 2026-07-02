<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
    <RouterLink class="navbar-brand" to="/">Placement Portal V2</RouterLink>

    <div class="collapse navbar-collapse">
      <ul class="navbar-nav ms-auto">

        <template v-if="authStore.isAuthenticated">
          <li class="nav-item">
            <span class="nav-link text-light">
              {{ authStore.email }} ({{ authStore.role }})
            </span>
          </li>
          <li class="nav-item">
            <RouterLink
              class="nav-link"
              :to="`/${authStore.role}/dashboard`"
            >
              Dashboard
            </RouterLink>
          </li>
          <li class="nav-item">
            <button class="btn btn-outline-light btn-sm ms-2" @click="handleLogout">
              Logout
            </button>
          </li>
        </template>

        <template v-else>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/login">Login</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/register">Register</RouterLink>
          </li>
        </template>

      </ul>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await authStore.logout()
  router.push({ name: 'login' })
}
</script>