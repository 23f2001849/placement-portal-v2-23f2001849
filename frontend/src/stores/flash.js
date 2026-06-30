import { defineStore } from 'pinia'

export const useFlashStore = defineStore('flash', {
  state: () => ({
    message: '',
    type: 'info'
  }),

  actions: {
    show(message, type = 'info') {
      this.message = message
      this.type = type

      setTimeout(() => {
        this.clear()
      }, 4000)
    },

    success(message) {
      this.show(message, 'success')
    },

    error(message) {
      this.show(message, 'danger')
    },

    clear() {
      this.message = ''
      this.type = 'info'
    }
  }
})