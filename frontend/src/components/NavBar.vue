<template>
  <nav class="navbar navbar-expand-lg navbar-dark custom-navbar px-3">
    <RouterLink class="navbar-brand" to="/">Placement Portal V2</RouterLink>

    <button
      class="navbar-toggler"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#navbarNav"
    >
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">

        <template v-if="authStore.isAuthenticated">

          <template v-if="authStore.role === 'admin'">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/dashboard">Dashboard</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/companies">Companies</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/students">Students</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/drives">Drives</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/applications">Applications</RouterLink>
            </li>
          </template>

          <template v-if="authStore.role === 'company'">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/company/dashboard">Dashboard</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/company/drives/create">New Drive</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/company/profile">Profile</RouterLink>
            </li>
          </template>

          <template v-if="authStore.role === 'student'">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/student/dashboard">Dashboard</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/student/drives">Drives</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/student/applications">Applications</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/student/profile">Profile</RouterLink>
            </li>
          </template>

          <li class="nav-item">
            <span class="nav-link text-light">
              {{ authStore.email }} ({{ authStore.role }})
            </span>
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