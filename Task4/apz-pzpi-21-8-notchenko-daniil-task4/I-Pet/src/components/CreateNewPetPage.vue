<template>
  <div>
    <h4>{{ $t('createNewPet') }}</h4>
    <form @submit.prevent="createPet">
      <input v-model="petName" :placeholder="$t('petNamePlaceholder')" />
      <input v-model="breed" :placeholder="$t('breedPlaceholder')" />
      <input v-model="vaccinated" type="checkbox" /> {{ $t('vaccinated') }}
      <input v-model.number="petType" :placeholder="$t('petTypePlaceholder')" type="number" />
      <button type="submit">{{ $t('create') }}</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateNewPetPage',
  data() {
    return {
      petName: '',
      breed: '',
      vaccinated: false,
      petType: null
    };
  },
  methods: {
    async createPet() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token not found');
        }

        const response = await axios.post('http://127.0.0.1:8000/pets', {
          pet_name: this.petName,
          breed: this.breed,
          vaccinated: this.vaccinated,
          pet_type: this.petType
        }, {
          headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });

        console.log('Pet created:', response.data);
      } catch (error) {
        console.error('An error occurred:', error);
      }
    }
  }
};
</script>

<style scoped>
</style>

  
  