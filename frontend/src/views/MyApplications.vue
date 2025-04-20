<template>
  <div class="max-w-5xl mx-auto p-6">
    <h1 class="text-4xl font-bold mb-8 text-gray-900 font-sans">My Applications</h1>

    <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded-md mb-6">
      {{ error }}
    </div>

    <div v-else-if="loading" class="text-gray-500">
      Loading your applications...
    </div>

    <div v-else-if="applications.length" class="flex flex-col gap-6">
      <div v-for="app in applications" :key="app.applied_at" class="bg-gray-900 shadow-lg border border-gray-700 rounded-lg p-6 text-white">
        <h2 class="text-2xl font-semibold mb-4 text-white">{{ app.job_title }}</h2>
        
        <p><strong>Company:</strong> {{ app.company }}</p>

        <p>
          <strong>Resume:</strong>
          <a v-if="app.resume_url" :href="app.resume_url" target="_blank" class="text-blue-500 underline">View Resume</a>
          <span v-else>N/A</span>
        </p>

        <p><strong>Match Score:</strong> {{ formatScore(app.match_score) }}/10</p>

        <p v-if="app.suggestions" class="text-gray-400 mb-2">
          <strong>Suggestions:</strong> {{ app.suggestions }}
        </p>

        <p class="text-gray-400 text-sm mt-4">
          Applied on {{ formatDate(app.applied_at) }}
        </p>
      </div>
    </div>

    <div v-else class="text-gray-500">
      You haven't applied to any jobs yet.
    </div>
  </div>
</template>

<script>
import apiClient from '../api';
import { ref, onMounted } from 'vue';

export default {
  name: 'MyApplications',
  setup() {
    const applications = ref([]);
    const error = ref(null);
    const loading = ref(true);

    const fetchApplications = async () => {
      try {
        const response = await apiClient.get('/jobs/my-applications/');
        applications.value = response.data;
      } catch (err) {
        error.value = 'Failed to load your applications.';
        console.error(err);
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (dateStr) => {
      return new Date(dateStr).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    };

    const formatScore = (score) => {
      if (score === null || score === undefined) return '';
      return score.toFixed(1);
    };

    onMounted(fetchApplications);

    return { applications, error, loading, formatDate, formatScore };
  },
};
</script>

<style scoped>
/* Main container */
.max-w-5xl {
  max-width: 75%;
}

/* Heading style */
h1 {
  color: #333;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Job Application Cards */
.bg-gray-900 {
  background-color: #1a1a1a;
}

.text-white {
  color: #fff;
}

.border-gray-700 {
  border-color: #333;
}

.text-gray-500 {
  color: #8e8e8e;
}

.text-gray-400 {
  color: #b0b0b0;
}

/* Button or clickable links */
.text-blue-500 {
  color: #1d72b8;
}

.text-blue-500:hover {
  text-decoration: underline;
}

/* Error message style */
.bg-red-100 {
  background-color: #f8d7da;
}

.text-red-700 {
  color: #721c24;
}

.bg-gray-900 {
  background-color: #1c1c1c;
}

.shadow-lg {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Responsive padding */
.p-6 {
  padding: 1.5rem;
}
</style>
