<template>
  <header class="header">
    <div class="container">
      <router-link to="/" class="brand">ResumeHunter</router-link>

      <nav class="nav">
        <template v-if="!isAuthenticated">
          
        </template>

        <template v-else>
          <router-link to="/jobs" class="nav-link">Jobs</router-link>

          <template v-if="userRole === 'job_seeker'">
            <router-link to="/upload-resume" class="nav-link">Upload Resume</router-link>
            <router-link to="/my-applications" class="nav-link">My Applications</router-link>
          </template>

          <template v-else-if="userRole === 'recruiter'">
            <router-link to="/create-job" class="nav-link">Post Job</router-link>
            <router-link to="/my-listings" class="nav-link">My Listings</router-link>
            <router-link to="/recruiter-applications" class="nav-link">Applications</router-link>
          </template>

          <button @click="logout" class="logout-btn">Logout</button>
        </template>
      </nav>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      isAuthenticated: false,
      userRole: null,
    }
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('access_token')
      this.isAuthenticated = !!token
      this.userRole = localStorage.getItem('user_role')?.toLowerCase() || null
    },
    logout() {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_role')
      this.isAuthenticated = false
      this.userRole = null
      this.$router.push('/login')
    },
  },
  created() {
    this.checkAuth()
    this.$router.afterEach(() => {
      this.checkAuth()
    })
  },
}
</script>

<style scoped>
.header {
  background-color: #1c1c1e;
  padding: 1rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1300px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  font-size: 1.75rem;
  font-weight: bold;
  color: #ffffff;
  text-decoration: none;
  letter-spacing: 1px;
}

.nav {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  color: #d1d1d1;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.nav-link:hover {
  color: #ffffff;
}

.logout-btn {
  background: #333;
  border: none;
  padding: 0.5rem 1rem;
  color: #d1d1d1;
  font-weight: 500;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
}

.logout-btn:hover {
  background: #555;
  color: white;
}
</style>
