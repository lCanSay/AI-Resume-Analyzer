<template>
  <div class="page-wrapper">
    <div class="content-wrapper">
      <h1 class="page-title">Applications for Your Jobs</h1>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="filteredApplications.length" class="applications-list">
        <div v-for="app in filteredApplications" :key="app.applied_at" class="application-card">
          <h2 class="job-title">{{ app.job_title }}</h2>
          <p class="application-detail"><strong>Applicant:</strong> {{ app.applicant_email }}</p>
          <p><strong>Match Score:</strong> {{ formatScore(app.match_score) }}/10</p>


          <div v-if="app.resume_url" class="resume-link">
            <a :href="app.resume_url" download>Download Resume</a>
          </div>


          <p class="applied-date">Applied on {{ formatDate(app.applied_at) }}</p>
        </div>
      </div>

      <div v-else class="info-text">
        No applications found.
      </div>
    </div>
  </div>
</template>


<script>
import apiClient from '../api'

export default {
  name: 'RecruiterApplicationsPage',
  data() {
    return {
      applications: [],
      jobTitles: [],
      selectedJobTitle: '',
      error: null,
      filteredApplications: []
    }
  },
  async created() {
    await this.fetchApplications();
  },
  methods: {
    async fetchApplications() {
      try {
        this.error = null;
        const response = await apiClient.get('/jobs/applications/');
        this.applications = response.data;
        this.filteredApplications = [...this.applications];
        this.jobTitles = [...new Set(this.applications.map(app => app.job_title))];
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to load applications.';
      }
    },
    filterApplicationsByJobTitle() {
      if (!this.selectedJobTitle) {
        this.filteredApplications = [...this.applications];
      } else {
        this.filteredApplications = this.applications.filter(app => app.job_title === this.selectedJobTitle);
      }
    },
    formatDate(value) {
      if (!value) return '';
      return new Date(value).toLocaleString();
    },
    formatScore(score) {
      if (score === null || score === undefined) return '';
      return score.toFixed(1);
    }
  }
}
</script>

<style scoped>
.page-wrapper {
  background-color: #1f1f1f;
  min-height: 100vh;
  padding: 40px 20px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
}

.error-message {
  background-color: #2c2c2c;
  color: #ff4d4f;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  text-align: center;
  border: 1px solid #ff4d4f;
}

.applications-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.application-card {
  background-color: #2c2c2c;
  border: 1px solid #333;
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.job-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.75rem;
  color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.application-detail {
  color: #cccccc;
  margin-bottom: 0.5rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.resume-link a {
  color: #ff4d4f;
  text-decoration: underline;
  font-weight: bold;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.applied-date {
  color: #aaaaaa;
  margin-top: 1rem;
  font-size: 0.9rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.info-text {
  color: #cccccc;
  text-align: center;
  margin-top: 2rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>

