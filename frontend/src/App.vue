<template>
  <div>
    <NavBar />
    <div class="container mt-4">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
</script>