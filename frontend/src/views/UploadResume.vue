<template>
  <div class="page-wrapper">
    <div class="container">
      <h1 class="title">Add Resume</h1>

      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>

      <form @submit.prevent="uploadResume" class="form">
        <div class="form-group">
          <label for="resume" class="label">Choose Resume (PDF/DOCX)</label>
          <div class="input-button-row">
            <input 
              type="file" 
              id="resume" 
              accept=".pdf,.docx" 
              @change="handleFileChange" 
              class="file-input" 
            />
            <button 
              type="submit" 
              class="submit-btn" 
              :disabled="!file"
            >
              Add Resume
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
import apiClient from '../api'

export default {
  name: 'UploadResumePage',
  data() {
    return {
      file: null,
      error: null,
      success: null,
    }
  },
  methods: {
    handleFileChange(event) {
      const selectedFile = event.target.files[0];
      if (selectedFile && ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'].includes(selectedFile.type)) {
        this.file = selectedFile;
        this.error = null;
      } else {
        this.file = null;
        this.error = 'Please select a PDF or DOCX file.';
      }
    },
    async uploadResume() {
      if (!this.file) {
        this.error = 'Please select a file to upload.';
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        this.error = null;
        this.success = null;
        const response = await apiClient.post('/resumes/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        this.success = response.data.message || 'Resume uploaded successfully!';
        this.file = null;
        document.getElementById('resume').value = '';
      } catch (err) {
        this.error = err.response?.data?.error || 'Failed to upload resume.';
      }
    },
  },
}
</script>

<style scoped>
.page-wrapper {
  background-color: #1f1f1f; /* dark grey */
  min-height: 100vh; /* full page */
  padding: 40px 20px;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #2c2c2c; /* slightly lighter grey */
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #ffffff;
  text-align: center;
}

.error-message,
.success-message {
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 1rem;
  width: 100%;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
}

.error-message {
  background-color: #2c2c2c;
  color: #ff4d4f;
  border: 1px solid #ff4d4f;
}

.success-message {
  background-color: #2c2c2c;
  color: #4caf50;
  border: 1px solid #4caf50;
}

.form {
  width: 100%;
}

.form-group {
  margin-bottom: 1.5rem;
}

.label {
  display: block;
  margin-bottom: 0.5rem;
  color: #cccccc;
  font-weight: 500;
}

.input-button-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.file-input {
  flex: 1;
  border: 1px solid #555;
  border-radius: 6px;
  background-color: #1f1f1f;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: #ffffff;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  outline: none;
}

.file-input::file-selector-button {
  background-color: #1d72b8;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  margin-right: 10px;
  border-radius: 6px;
  cursor: pointer;
}

.file-input::file-selector-button:hover {
  background-color: #155a8a;
}

.submit-btn {
  background-color: #1d72b8;
  color: #fff;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #155a8a;
}

.submit-btn:disabled {
  background-color: #555;
  cursor: not-allowed;
}
</style>
