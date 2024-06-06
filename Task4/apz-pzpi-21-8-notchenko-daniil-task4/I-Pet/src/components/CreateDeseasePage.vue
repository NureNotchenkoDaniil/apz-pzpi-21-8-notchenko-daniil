<template>
  <div>
    <h4>{{ $t('createDiseaseStory') }}</h4>
    <form @submit.prevent="createDiseaseStory" class="disease-form">
      <label :for="$t('petIdLabel')">{{ $t('petId') }}:</label>
      <input type="number" :id="$t('petIdId')" v-model="petId" required>
      <label :for="$t('firstVisitDateLabel')">{{ $t('firstVisitDate') }}:</label>
      <input type="date" :id="$t('firstVisitDateId')" v-model="firstVisitDate" required>
      <label :for="$t('lastVisitDateLabel')">{{ $t('lastVisitDate') }}:</label>
      <input type="date" :id="$t('lastVisitDateId')" v-model="lastVisitDate" required>
      <label :for="$t('medicationsLabel')">{{ $t('medications') }}:</label>
      <input type="text" :id="$t('medicationsId')" v-model="medications">
      <button type="submit">{{ $t('createStory') }}</button>
    </form>

    <div v-if="editingStory" class="disease-form">
      <h4>{{ $t('updateDiseaseStory') }}</h4>
      <form @submit.prevent="updateDiseaseStory" class="disease-form">
        <label :for="$t('editFirstVisitDateLabel')">{{ $t('firstVisitDate') }}:</label>
        <input type="date" :id="$t('editFirstVisitDateId')" v-model="editFirstVisitDate" required>
        <label :for="$t('editLastVisitDateLabel')">{{ $t('lastVisitDate') }}:</label>
        <input type="date" :id="$t('editLastVisitDateId')" v-model="editLastVisitDate" required>
        <label :for="$t('editMedicationsLabel')">{{ $t('medications') }}:</label>
        <input type="text" :id="$t('editMedicationsId')" v-model="editMedications">
        <button type="submit">{{ $t('updateStory') }}</button>
      </form>
    </div>

    <h4>{{ $t('diseaseStories') }}</h4>
    <div v-if="diseaseStories.length" class="disease-stories">
      <div v-for="story in diseaseStories" :key="story.id" class="disease-story">
        <p><strong>ID:</strong> {{ story.id }}</p>
        <p><strong>{{ $t('firstVisitDate') }}:</strong> {{ story.first_visit_date }}</p>
        <p><strong>{{ $t('lastVisitDate') }}:</strong> {{ story.last_visit_date }}</p>
        <p v-if="story.medications"><strong>{{ $t('medications') }}:</strong> {{ story.medications }}</p>
        <button @click="getSpecificDiseaseStory(story.id)">{{ $t('view') }}</button>
        <button @click="deleteDiseaseStory(story.id)">{{ $t('delete') }}</button>
        <button @click="editStory(story)">{{ $t('edit') }}</button>
      </div>
    </div>
    <p v-else>{{ $t('noDiseaseStories') }}</p>
  </div>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CreateDiseaseStory',
    data() {
      return {
        petId: '',
        firstVisitDate: '',
        lastVisitDate: '',
        medications: '',
        diseaseStories: [],
        editingStory: false,
        editStoryId: null,
        editFirstVisitDate: '',
        editLastVisitDate: '',
        editMedications: ''
      };
    },
    created() {
      this.getDiseaseStories();
    },
    methods: {
      async createDiseaseStory() {
        try {
          const token = localStorage.getItem('token');
          if (!token) {
            throw new Error('Token not found');
          }
  
          await axios.post('http://127.0.0.1:8000/disease_story', {
            pet: this.petId,
            first_visit_date: this.firstVisitDate,
            last_visit_date: this.lastVisitDate,
            medications: this.medications
          }, {
            headers: {
              'accept': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
  
          this.petId = '';
          this.firstVisitDate = '';
          this.lastVisitDate = '';
          this.medications = '';
  
          this.getDiseaseStories();
        } catch (error) {
          console.error('An error occurred:', error);
        }
      },
      async getDiseaseStories() {
        try {
          const token = localStorage.getItem('token');
          if (!token) {
            throw new Error('Token not found');
          }
  
          const response = await axios.get('http://127.0.0.1:8000/disease_story', {
            headers: {
              'accept': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
  
          this.diseaseStories = response.data.data;
        } catch (error) {
          console.error('An error occurred:', error);
        }
      },
      async getSpecificDiseaseStory(storyId) {
        try {
          const token = localStorage.getItem('token');
          if (!token) {
            throw new Error('Token not found');
          }
  
          const response = await axios.get(`http://127.0.0.1:8000/disease_story/${storyId}`, {
            headers: {
              'accept': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
  
          console.log(response.data.data);
        } catch (error) {
          console.error('An error occurred:', error);
        }
      },
      async updateDiseaseStory() {
        try {
          const token = localStorage.getItem('token');
          if (!token) {
            throw new Error('Token not found');
          }
  
          await axios.put(`http://127.0.0.1:8000/disease_story/${this.editStoryId}`, {
            first_visit_date: this.editFirstVisitDate,
            last_visit_date: this.editLastVisitDate,
            medications: this.editMedications
          }, {
            headers: {
              'accept': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
  
          this.editStoryId = null;
          this.editFirstVisitDate = '';
          this.editLastVisitDate = '';
          this.editMedications = '';
          this.editingStory = false;
  
          this.getDiseaseStories();
        } catch (error) {
          console.error('An error occurred:', error);
        }
      },
      async deleteDiseaseStory(storyId) {
        try {
          const token = localStorage.getItem('token');
          if (!token) {
            throw new Error('Token not found');
          }
  
          await axios.delete(`http://127.0.0.1:8000/disease_story/${storyId}`, {
            headers: {
              'accept': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
  
          this.getDiseaseStories();
        } catch (error) {
          console.error('An error occurred:', error);
        }
      },
      editStory(story) {
        this.editStoryId = story.id;
        this.editFirstVisitDate = story.first_visit_date;
        this.editLastVisitDate = story.last_visit_date;
        this.editMedications = story.medications;
        this.editingStory = true;
      }
    }
  };
  </script>
  
  <style scoped>
  .disease-form {
    margin-bottom: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .disease-stories {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .disease-story {
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 10px;
  }
  
  .disease-story p {
    margin: 5px 0;
  }
  
  .disease-story button {
    margin-right: 10px;
  }
  
  .disease-form input, .disease-form button {
    padding: 5px;
    font-size: 16px;
  }
  </style>
  