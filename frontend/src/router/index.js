import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/admin/dashboard',
    name: 'admin-dashboard',
    component: () => import('@/views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/companies',
    name: 'admin-companies',
    component: () => import('@/views/admin/ManageCompanies.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/students',
    name: 'admin-students',
    component: () => import('@/views/admin/ManageStudents.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/drives',
    name: 'admin-drives',
    component: () => import('@/views/admin/ManageDrives.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/applications',
    name: 'admin-applications',
    component: () => import('@/views/admin/ViewApplications.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/company/dashboard',
    name: 'company-dashboard',
    component: () => import('@/views/company/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/company/drives/create',
    name: 'company-drive-create',
    component: () => import('@/views/company/DriveCreate.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/company/drives/:id/edit',
    name: 'company-drive-edit',
    component: () => import('@/views/company/DriveEdit.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/company/drives/:id/applications',
    name: 'company-drive-applications',
    component: () => import('@/views/company/DriveApplications.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/company/profile',
    name: 'company-profile',
    component: () => import('@/views/company/Profile.vue'),
    meta: { requiresAuth: true, role: 'company' }
  },
  {
    path: '/student/dashboard',
    name: 'student-dashboard',
    component: () => import('@/views/student/Dashboard.vue'),
    meta: { requiresAuth: true, role: 'student' }
  },
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
    return
  }

  if (to.meta.role && authStore.role !== to.meta.role) {
    if (['admin', 'company', 'student'].includes(authStore.role)) {
      next({ name: `${authStore.role}-dashboard` })
    } else {
      next({ name: 'login' })
    }
    return
  }

  next()
})

export default router