import { loginUser } from '../api/auth'

const handleLogin = async () => {
  try {
    const res = await loginUser(user_id.value, password.value)
    if (res.data.authenticated) {
      localStorage.setItem('authenticated', 'true')
      localStorage.setItem('user_id', user_id.value)
      router.push('/dashboard')
    }
  } catch (err) {
    errorMsg.value = 'Login failed'
  }
}
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="bg-white p-8 rounded-2xl shadow-md w-full max-w-md">
      <h2 class="text-2xl font-semibold text-center text-blue-600 mb-6">Welcome Back</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label for="userId" class="block text-sm font-medium text-gray-700">User ID</label>
          <input
            v-model="userId"
            type="text"
            id="userId"
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
            required
          />
        </div>
        <div v-if="loginFailed" class="text-red-500 text-sm mb-4">Login failed</div>
        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition"
        >
          Login
        </button>
        <div class="mt-4 text-center text-sm text-gray-600">
          New user? <router-link to="/register" class="text-blue-600 hover:underline">Register here</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userId: '',
      password: '',
      loginFailed: false
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await fetch('http://localhost:8000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_id: this.userId, password: this.password })
        })

        if (!response.ok) throw new Error('Login failed')

        const data = await response.json()
        localStorage.setItem('authenticated', 'true')
        localStorage.setItem('user_id', this.userId)
        this.$router.push('/dashboard')
      } catch (error) {
        this.loginFailed = true
      }
    }
  }
}
</script>
