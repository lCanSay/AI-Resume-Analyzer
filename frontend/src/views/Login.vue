<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email Address</label>
          <input type="email" id="email" v-model="loginForm.email" required />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="loginForm.password" required />
        </div>
        <button type="submit">Login</button>
      </form>
      <p>Don't have an account? <router-link to="/register">Sign up</router-link></p>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        email: '',
        password: '',
      },
      error: null,
    }
  },
  methods: {
    async login() {
      try {
        this.error = null
        const response = await apiClient.post('/auth/login/', this.loginForm)
        const { access, refresh, role } = response.data

        if (!access || !refresh || !role) {
          throw new Error('Invalid login response')
        }

        localStorage.setItem('access_token', access)
        localStorage.setItem('refresh_token', refresh)
        localStorage.setItem('user_role', role)

        this.$router.push('/jobs')
      } catch (err) {
        console.error('Login error:', err)
        this.error = err.response?.data?.error || err.message || 'Login failed.'
      }
    },
  },
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1a1a1a;
  padding: 30px;
}

.login-box {
  background-color: #333;
  padding: 50px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
  width: 400px;
  max-width: 100%;
  text-align: center;
}

h2 {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 40px;
}

.form-group {
  margin-bottom: 25px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #ccc;
  font-size: 16px;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #555;
  border-radius: 6px;
  font-size: 16px;
  background-color: #444;
  color: #e0e0e0;
}

button {
  background-color: #555;
  color: #fff;
  padding: 16px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: 600;
  width: 100%;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #777;
}

.error {
  color: #ff4c4c;
  margin-top: 20px;
  font-size: 14px;
}
</style>
