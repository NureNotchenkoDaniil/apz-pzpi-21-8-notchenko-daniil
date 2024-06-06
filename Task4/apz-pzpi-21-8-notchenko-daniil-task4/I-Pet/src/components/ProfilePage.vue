<template>
    <div class="profile-container" v-if="profileData">
      <h2>{{ $t('profileTitle') }}</h2>
      <p><strong>{{ $t('username') }}</strong> {{ profileData.username }}</p>
      <p><strong>{{ $t('email') }}</strong> {{ profileData.email }}</p>
      <p><strong>{{ $t('joinDate') }}</strong> {{ profileData.join_date }}</p>
      <p><strong>{{ $t('pets') }}:</strong> {{ profileData.pets.join(', ') }}</p>
      <h3>{{ $t('rolesTitle') }}</h3>
      <p><strong>{{ $t('admin') }}</strong> {{ profileData.roles.is_admin ? $t('yes') : $t('no') }}</p>
      <p><strong>{{ $t('veterinarian') }}</strong> {{ profileData.roles.is_veterinarian ? $t('yes') : $t('no') }}</p>
      <p><strong>{{ $t('government') }}</strong> {{ profileData.roles.is_government ? $t('yes') : $t('no') }}</p>
    </div>
    <div v-else>
      <p>{{ $t('loadingData') }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ProfilePage',
    data() {
      return {
        profileData: null,
        error: null
      };
    },
    async created() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.$router.push('/signin');
        return;
      }
  
      try {
        const response = await axios.post('http://127.0.0.1:8000/user/me', {}, {
          headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        });
        this.profileData = response.data.data;
      } catch (error) {
        console.error('Error fetching profile data:', error);
        this.error = 'Не вдалося завантажити дані профілю.';
      }
    }
  };
  </script>
  
  <style scoped>
  .profile-container {
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  
  h2 {
    margin-bottom: 20px;
  }
  
  p {
    margin: 10px 0;
  }
  
  strong {
    color: #333;
  }
  </style>
  