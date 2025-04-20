<template>
  <div class="container">
    <h1 class="page-title">Job Listings</h1>

    <div v-if="error" class="alert error">{{ error }}</div>

    <div class="content-wrapper">
      <div class="filter-section">
        <input v-model="filters.location" placeholder="Location" />
        <input v-model="filters.experience" placeholder="Experience (years)" type="number" min="0" />
        <button @click="applyFilters">Apply</button>
      </div>

      <div class="jobs-section">
        <div v-if="jobs.length === 0" class="no-jobs">No jobs found.</div>

        <div v-else class="job-grid">
          <router-link
            v-for="job in jobs"
            :key="job.id"
            :to="'/jobs/' + job.id"
            class="job-card"
          >
            <h2 class="job-title">{{ job.title }}</h2>
            <p><strong>Company:</strong> {{ job.company }}</p>
            <p><strong>Location:</strong> {{ job.location }}</p>
            <p><strong>Experience:</strong> {{ job.experience_required }} years</p>
            <p><strong>Skills:</strong> {{ job.skills_required.join(', ') }}</p>
          </router-link>
        </div>

        <div class="pagination">
          <button v-if="prevPage" @click="fetchJobs(prevPage)">Previous</button>
          <button v-if="nextPage" @click="fetchJobs(nextPage)">Next</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import apiClient from '../api'

export default {
  name: 'JobListPage',
  data() {
    return {
      jobs: [],
      nextPage: null,
      prevPage: null,
      filters: {
        location: '',
        experience: '',
      },
      sortBy: 'created_at',
      error: null
    }
  },
  created() {
    this.fetchJobs('/jobs/job-list/')
  },
  methods: {
    async fetchJobs(url) {
      try {
        this.error = null
        const response = await apiClient.get(url)
        this.jobs = response.data.results
        this.nextPage = response.data.next
        this.prevPage = response.data.previous
      } catch (err) {
        this.error = 'Failed to load jobs.'
      }
    },
    async applyFilters() {
      let params = []
      if (this.filters.location) params.push(`location=${this.filters.location}`)
      if (this.filters.experience) params.push(`experience_required=${this.filters.experience}`)
      if (this.sortBy) params.push(`ordering=${this.sortBy}`)

      const query = params.length ? '?' + params.join('&') : ''
      await this.fetchJobs('/jobs/job-list/' + query)
    },
    capitalize(value) {
      if (!value) return ''
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
  }
}
</script>

<style scoped>

.container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 30px;
  color: #e0e0e0;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #ffffff;
}

.alert {
  background-color: #331111;
  color: #ff4c4c;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-weight: 500;
}


.content-wrapper {
  display: flex;
  gap: 2rem;
}

.filter-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-section input {
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #555;
  background-color: #2a2a2a;
  color: #e0e0e0;
}

.filter-section button {
  padding: 0.75rem 1.5rem;
  background-color: #3399ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.filter-section button:hover {
  background-color: #267acc;
}

/* Right side: jobs */
.jobs-section {
  flex: 3;
}

.no-jobs {
  color: #888;
  text-align: center;
  font-size: 1.2rem;
  margin-top: 2rem;
}

.job-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.job-card {
  background: #1e1e20;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.7);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}

.job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.8);
}

.job-title {
  font-size: 1.5rem;
  color: #3399ff;
  margin-bottom: 0.8rem;
}

.pagination {
  margin-top: 3rem;
  text-align: center;
}

.pagination button {
  margin: 0 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #3399ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination button:hover {
  background-color: #267acc;
}

</style>