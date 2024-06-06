<template>
  <div class="pets-container">
    <h4>{{ $t('myPets') }}</h4>
    <div class="search-form">
      <input type="number" v-model="searchId" :placeholder="$t('enterPetId')">
      <button @click="searchPet">{{ $t('search') }}</button>
    </div>
    <div v-if="pet" class="pet-details">
      <h5>{{ pet.pet_name }}</h5>
      <p><strong>{{ $t('breed') }}:</strong> {{ pet.breed }}</p>
      <p><strong>{{ $t('vaccinated') }}:</strong> {{ pet.vaccinated ? $t('yes') : $t('no') }}</p>
    </div>
    <p v-else>{{ $t('noPetFound') }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PetsPage',
  data() {
    return {
      searchId: null,
      pet: null
    };
  },
  methods: {
    async searchPet() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token not found');
        }

        const response = await axios.get(`http://127.0.0.1:8000/pets/${this.searchId}`, {
          headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        this.pet = response.data.data;
      } catch (error) {
        console.error('An error occurred:', error);
      }
    }
  }
};
</script>

<style scoped>
.pets-container {
  width: 80%;
  margin: 0 auto;
  padding: 20px;
}

.search-form {
  margin-bottom: 20px;
}

.pet-details {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 50%;
}

.pet-details h5 {
  margin: 0 0 10px;
  font-size: 1.2em;
  color: #333;
}

.pet-details p {
  margin: 5px 0;
  color: #666;
}

.pet-details strong {
  color: #333;
}
</style>

  
  
  