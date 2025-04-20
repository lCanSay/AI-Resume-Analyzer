<template>
  <div class="register-container">
    <div class="register-box">
      <h2>Create Account</h2>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            v-model="registerForm.email"
            type="email"
            id="email"
            placeholder="Enter your email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            v-model="registerForm.password"
            type="password"
            id="password"
            placeholder="Enter your password"
            required
          />
        </div>
        <div class="form-group">
          <label for="role">Role</label>
          <select
            v-model="registerForm.role"
            id="role"
            required
          >
            <option value="job_seeker">Job Seeker</option>
            <option value="recruiter">Recruiter</option>
          </select>
        </div>
        <button type="submit">Sign Up</button>
      </form>
      <p>
        Already have an account?
        <router-link to="/login">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import { useAuth } from '../composables/useAuth'

export default {
  name: 'RegisterPage',
  setup() {
    const { registerForm, error, register } = useAuth()
    return { registerForm, error, register }
  },
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #1a1a1a;
  padding: 30px;
}

.register-box {
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

.error-message {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #ffdddd;
  color: #cc0000;
  border-radius: 6px;
  font-size: 16px;
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

input,
select {
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

p {
  margin-top: 30px;
  font-size: 15px;
  color: #ccc;
}

router-link {
  color: #ff4c4c;
  font-weight: 600;
  text-decoration: none;
}

router-link:hover {
  text-decoration: underline;
}
</style>
