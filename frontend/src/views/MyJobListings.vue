<template>
  <div class="page-wrapper">
    <div class="content-wrapper">
      <h1 class="page-title">My Job Listings</h1>

      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <div v-if="jobs.length" class="jobs-grid">
        <div v-for="job in jobs" :key="job.id" class="job-card">
          <div>
            <h2 class="job-title">{{ job.title }}</h2>
            <p class="job-detail"><strong>Company:</strong> {{ job.company_name }}</p>
            <p class="job-detail"><strong>Location:</strong> {{ job.location }}</p>
            <p class="job-detail"><strong>Type:</strong> {{ capitalize(job.employment_type) }}</p>
            <p class="job-detail"><strong>Experience:</strong> {{ job.required_experience }} years</p>
            <p class="job-detail"><strong>Skills:</strong> {{ job.skills_required.join(', ') }}</p>
            <p class="job-description">{{ truncate(job.description, 200) }}</p>
          </div>
        </div>
      </div>

      <div v-else-if="!loading" class="info-text">
        No job listings created yet.
      </div>

      <div v-else class="info-text">
        Loading job listings...
      </div>
    </div>
  </div>
</template>

  
  <script>
  import apiClient from '../api'
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'MyJobListings',
    setup() {
      const jobs = ref([]);
      const error = ref(null);
      const loading = ref(true);
      const router = useRouter();
  
      const fetchMyJobs = async () => {
        try {
          const response = await apiClient.get('/jobs/my-jobs/');
          jobs.value = response.data.results;
        } catch (err) {
          error.value = 'Failed to load your job listings.';
          console.error('Error loading recruiter jobs:', err);
        } finally {
          loading.value = false;
        }
      };
  
      const deleteJob = async (jobId) => {
        if (confirm('Are you sure you want to delete this job listing?')) {
          try {
            await apiClient.delete(`/jobs/${jobId}/`);
            jobs.value = jobs.value.filter(job => job.id !== jobId);
          } catch (err) {
            error.value = 'Failed to delete the job listing.';
            console.error('Error deleting job:', err);
          }
        }
      };
  
      const editJob = (jobId) => {
        router.push(`/recruiter/edit-job/${jobId}`);
      };
  
      const capitalize = (value) => {
        if (!value) return '';
        return value.charAt(0).toUpperCase() + value.slice(1);
      };
  
      const truncate = (value, length) => {
        if (!value) return '';
        return value.length > length ? value.substring(0, length) + '...' : value;
      };
  
      onMounted(fetchMyJobs);
  
      return { jobs, error, loading, capitalize, truncate, deleteJob, editJob };
    },
  };
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
  
  .jobs-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }
  
  .job-card {
    background-color: #2c2c2c;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  
  .job-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.75rem;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  .job-detail {
    color: #cccccc;
    margin-bottom: 0.5rem;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  .job-description {
    color: #aaaaaa;
    margin-top: 0.75rem;
    font-size: 0.9rem;
    line-height: 1.4;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  .info-text {
    color: #cccccc;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    text-align: center;
    margin-top: 2rem;
  }
  </style>
  