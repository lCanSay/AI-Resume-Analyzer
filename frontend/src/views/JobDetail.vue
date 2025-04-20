<template>
  <div class="container">
    <div v-if="error" class="alert error">{{ error }}</div>
    <div v-if="success" class="toast success">
      {{ success }}
      <div v-if="match_score !== null" class="feedback">
        <p><strong>Match Score:</strong> {{ formatScore(match_score) }}/10</p>
        <p><strong>Suggestions:</strong> {{ suggestions }}</p>
      </div>
    </div>


    <div v-if="job" class="job-card">
      <h1 class="job-title">{{ job.title }}</h1>
      <p><strong>Company:</strong> {{ job.company }}</p>
      <p><strong>Location:</strong> {{ job.location }}</p>
      <p><strong>Experience Required:</strong> {{ job.experience_required }} years</p>
      <p><strong>Skills:</strong> {{ job.skills_required.join(', ') }}</p>
      <p class="job-description">{{ job.description }}</p>
      <p class="posted-date">Posted on {{ formatDate(job.created_at) }}</p>

      <button
        v-if="isJobSeeker"
        @click="applyJob"
        :disabled="applying"
        class="apply-btn"
      >
        {{ applying ? 'Applying...' : 'Apply Now' }}
      </button>
    </div>

    <div v-else class="loading">Loading job details...</div>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'JobDetailPage',
  data() {
    return {
      job: null,
      error: null,
      success: null,
      applying: false,
      match_score: null,
      suggestions: null
    }
  },
  computed: {
    isJobSeeker() {
      return localStorage.getItem('user_role') === 'job_seeker'
    }
  },
  async created() {
    await this.fetchJob()
  },
  methods: {
    async fetchJob() {
      try {
        const jobId = this.$route.params.id
        const response = await apiClient.get(`/jobs/job-detail/${jobId}/`)
        this.job = response.data
      } catch {
        this.error = 'Failed to load job details.'
      }
    },
    async applyJob() {
      if (this.applying) return
      this.applying = true
      try {
        const jobId = this.$route.params.id
        const response = await apiClient.post(`/jobs/${jobId}/apply/`)
        this.success = 'Application submitted successfully!'
        this.match_score = response.data.match_score
        this.suggestions = response.data.suggestions
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to apply.'
      } finally {
        this.applying = false
      }
    },
    formatDate(value) {
      if (!value) return ''
      return new Date(value).toLocaleDateString()
    },
    formatScore(score) {
      if (score === null || score === undefined) return '';
      return score.toFixed(1);
    }

  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 40px auto;
  padding: 30px;
}

.alert {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-weight: 500;
}

.alert.error {
  background-color: #331111;
  color: #ff4c4c;
}

.alert.success {
  background-color: #113311;
  color: #4cff4c;
}

.feedback {
  margin-top: 10px;
  color: #cccccc;
}

.job-card {
  background: #1e1e20;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.7);
  color: #e0e0e0;
}

.job-title {
  font-size: 2.2rem;
  margin-bottom: 20px;
  color: #ffffff;
}

.job-card p {
  margin-bottom: 12px;
}

.job-description {
  margin-top: 20px;
  line-height: 1.7;
  color: #d1d1d1;
}

.posted-date {
  margin-top: 20px;
  color: #999;
  font-size: 0.9rem;
}

.apply-btn {
  background-color: #333333;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  margin-top: 30px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.apply-btn:hover {
  background-color: #555555;
}

.apply-btn:disabled {
  background-color: #222;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #777;
}
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: #224422;
  color: #ccffcc;
  padding: 16px 24px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  z-index: 1000;
  animation: fadeIn 0.5s ease;
  max-width: 300px;
}

.toast.success {
  background-color: #224422;
  color: #ccffcc; 
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

</style>
