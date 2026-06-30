import { defineStore } from 'pinia'
import apiClient from '@/api/client'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    role: localStorage.getItem('role') || null,
    email: localStorage.getItem('email') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(email, password) {
      const response = await apiClient.post('/api/login', { email, password })

      this.accessToken = response.data.access_token
      this.refreshToken = response.data.refresh_token
      this.role = response.data.role
      this.email = response.data.email

      localStorage.setItem('access_token', this.accessToken)
      localStorage.setItem('refresh_token', this.refreshToken)
      localStorage.setItem('role', this.role)
      localStorage.setItem('email', this.email)

      return response.data
    },

    async logout() {
      try {
        await apiClient.post('/api/logout')
      } catch (e) {
        // even if the API call fails, clear local state
      }

      this.accessToken = null
      this.refreshToken = null
      this.role = null
      this.email = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('role')
      localStorage.removeItem('email')
    }
  }
})