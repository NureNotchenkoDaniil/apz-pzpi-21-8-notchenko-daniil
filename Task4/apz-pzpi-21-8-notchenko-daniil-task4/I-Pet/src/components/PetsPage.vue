<template>
  <div class="pets-container">
    <h4>{{ $t('myPets') }}</h4>
    <div v-if="pets.length" class="pets-list">
      <div v-for="pet in pets" :key="pet.id" class="pet-card">
        <h5>{{ pet.pet_name }}</h5>
        <p><strong>{{ $t('breed') }}:</strong> {{ pet.breed }}</p>
        <p><strong>{{ $t('vaccinated') }}:</strong> {{ pet.vaccinated ? $t('yes') : $t('no') }}</p>
        <h5>ID: {{ pet.id }}</h5>
        <div class="pet-delete-form">
          <input type="text" v-model="deletePetId" :placeholder="$t('confirmationById')" />
          <button @click="deletePet(pet.id)">{{ $t('deletePet') }}</button>
        </div>
      </div>
    </div>
    <p v-else>{{ $t('noPetsFound') }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PetsPage',
  data() {
    return {
      pets: [],
      deletePetId: ''
    };
  },
  async created() {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Token not found');
      }

      const response = await axios.get('http://127.0.0.1:8000/pets', {
        headers: {
          'accept': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });

      this.pets = response.data.data;
    } catch (error) {
      console.error('An error occurred:', error);
    }
  },
  methods: {
    async deletePet(petId) {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token not found');
        }

        await axios.delete(`http://127.0.0.1:8000/pets/${petId}`, {
          headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          params: {
            pet_id: this.deletePetId
          }
        });

        this.pets = this.pets.filter(pet => pet.id !== petId);
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

.pets-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.pet-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 15px;
  width: calc(33.333% - 20px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease-in-out;
}

.pet-card h5 {
  margin: 0 0 10px;
  font-size: 1.2em;
  color: #333;
}

.pet-card p {
  margin: 5px 0;
  color: #666;
}

.pet-card strong {
  color: #333;
}

.pet-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.pet-delete-form {
  margin-bottom: 20px;
}

.pet-delete-form input {
  margin-right: 10px;
}
</style>   