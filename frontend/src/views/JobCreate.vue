<template>
  <div class="container">
    <h1>Create Job Listing</h1>
    <form @submit.prevent="createJob" class="form">
      <div class="form-group">
        <label>Job Title</label>
        <input v-model="form.title" type="text" required />
      </div>

      <div class="form-group">
        <label>Company Name</label>
        <input v-model="form.company" type="text" required />
      </div>

      <div class="form-group">
        <label>Location</label>
        <input v-model="form.location" type="text" required />
      </div>

      <div class="form-group">
        <label>Required Experience (years)</label>
        <input v-model="form.experience_required" type="number" min="0" required />
      </div>

      <div class="form-group">
        <label>Skills (comma-separated)</label>
        <input v-model="skillsInput" type="text" placeholder="e.g. Python, Django, AWS" />
      </div>

      <div class="form-group">
        <label>Description</label>
        <textarea v-model="form.description" required></textarea>
      </div>

      <button type="submit">Create Job</button>

      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import apiClient from '../api'

export default {
  name: 'JobCreatePage',
  data() {
    return {
      form: {
        title: '',
        company: '',
        location: '',
        experience_required: '',
        skills_required: [],
        description: ''
      },
      skillsInput: '',
      error: null
    }
  },
  methods: {
    async createJob() {
      try {
        this.error = null
        this.form.skills_required = this.skillsInput
          .split(',')
          .map(skill => skill.trim())
          .filter(skill => skill.length > 0)

        await apiClient.post('/jobs/create/', this.form)

        this.$router.push('/jobs')
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to create job.'
      }
    }
  }
}
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: 40px auto;
  padding: 30px;
  background-color: #1c1c1e; /* dark background */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.8);
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #ffffff;
}

.form {
  display: flex;
  flex-direction: column;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

label {
  margin-bottom: 8px;
  color: #d1d1d1;
  font-weight: 500;
}

input,
textarea {
  background-color: #2c2c2e;
  border: 1px solid #444;
  border-radius: 6px;
  padding: 10px;
  color: #f1f1f1;
  font-size: 1rem;
  outline: none;
  transition: border 0.3s;
}

input:focus,
textarea:focus {
  border-color: #888;
}

textarea {
  min-height: 120px;
  resize: vertical;
}

button {
  background-color: #333;
  color: #ffffff;
  border: none;
  padding: 12px 20px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background-color: #555;
}

.error {
  margin-top: 20px;
  color: #ff5a5f;
  text-align: center;
  font-weight: 500;
}
</style>
