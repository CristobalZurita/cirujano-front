import axios from 'axios'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: typeof localStorage !== 'undefined' ? localStorage.getItem('auth.token') : null,
    user: null,
    error: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user ? !!state.user.is_admin : false
  },
  actions: {
    setAuthHeader() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      } else {
        delete axios.defaults.headers.common['Authorization']
      }
    },

    async login(email, password) {
      this.error = null
      try {
        const res = await axios.post('/api/v1/auth/login', { email, password })
        const data = res.data || {}
        const token = data.access_token || data.token || null
        if (!token) {
          this.error = data.detail || data.message || 'Login failed'
          throw new Error(this.error)
        }

        this.token = token
        if (typeof localStorage !== 'undefined') localStorage.setItem('auth.token', token)
        this.setAuthHeader()

        // optionally set user if returned
        if (data.user) this.user = data.user

        return true
      } catch (err) {
        this.error = err?.response?.data?.detail || err.message || 'Error during login'
        throw err
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.error = null
      if (typeof localStorage !== 'undefined') localStorage.removeItem('auth.token')
      this.setAuthHeader()
    },

    async checkAuth() {
      if (this.token) {
        this.setAuthHeader()
        try {
          // If backend exposes a profile endpoint, try to fetch user info
          const res = await axios.get('/api/v1/auth/me')
          if (res?.data) this.user = res.data
        } catch (e) {
          // ignore - token might still be valid for API use
        }
      }
    }
  }
})
/**
 * Store Pinia - auth.js
 * Gestiona el estado global de autenticación
 * 
 * Uso en componentes:
 * import { useAuthStore } from '@/stores/auth'
 * const auth = useAuthStore()
 * auth.login(email, password)
 */

import { defineStore } from 'pinia'
import { useAuth } from '@/composables/useAuth'

export const useAuthStore = defineStore('auth', () => {
  const authComposable = useAuth()

  // State properties
  const user = authComposable.user
  const token = authComposable.token
  const refreshToken = authComposable.refreshToken
  const isLoading = authComposable.isLoading
  const error = authComposable.error

  // Computed properties
  const isAuthenticated = authComposable.isAuthenticated
  const isAdmin = authComposable.isAdmin

  // Actions
  const register = authComposable.register
  const login = authComposable.login
  const logout = authComposable.logout
  const checkAuth = authComposable.checkAuth
  const fetchUserInfo = authComposable.fetchUserInfo
  const refreshAccessToken = authComposable.refreshAccessToken

  return {
    // State
    user,
    token,
    refreshToken,
    isLoading,
    error,

    // Computed
    isAuthenticated,
    isAdmin,

    // Actions
    register,
    login,
    logout,
    checkAuth,
    fetchUserInfo,
    refreshAccessToken
  }
})
