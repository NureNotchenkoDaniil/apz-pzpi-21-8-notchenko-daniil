<template>
    <nav class="navbar navbar-expand navbar-light">
      <div class="container">
        <a href="/" class="navbar-brand">I-Pet</a>
        <div class="collapse navbar-collapse">
          <!-- Left Menu -->
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link">{{ $t('home') }}</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated && !roles.is_admin && !roles.is_veterinarian && !roles.is_government">
              <router-link to="/newpet" class="nav-link">{{ $t('newPet') }}</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link to="/pets" class="nav-link">{{ $t('pets') }}</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated && (roles.is_admin || roles.is_veterinarian)">
              <router-link to="/petsserch" class="nav-link">{{ $t('petSearch') }}</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link to="/newdesease" class="nav-link">{{ $t('diseaseHistory') }}</router-link>
            </li>
          </ul>
          <!-- Right Menu -->
          <ul class="navbar-nav ms-auto">
            <li class="nav-item" v-if="!isAuthenticated">
              <router-link to="/signin" class="nav-link">{{ $t('signIn') }}</router-link>
            </li>
            <li class="nav-item" v-if="!isAuthenticated">
              <router-link to="/signup" class="nav-link">{{ $t('signUp') }}</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <router-link to="/profile" class="nav-link">{{ $t('profile') }}</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated && roles.is_admin">
              <router-link to="/admin" class="nav-link">{{ $t('adminPanel') }}</router-link>
            </li>
            <li class="nav-item" v-if="isAuthenticated">
              <button @click="logout" class="btn btn-link nav-link">{{ $t('logOut') }}</button>
            </li>
            <!-- Language Switch Button -->
            <li class="nav-item">
              <button @click="toggleLanguage" class="btn btn-link nav-link">{{ $t('language') }}</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  import axios from 'axios';
 
  
  export default {
    name: 'NavBar',
    data() {
      return {
        roles: {
          is_admin: false,
          is_veterinarian: false,
          is_government: false,
        },
        isAuthenticated: false,
      };
    },
    async created() {
      const token = localStorage.getItem('token');
      if (token) {
        this.isAuthenticated = true;
        try {
          const response = await axios.post('http://127.0.0.1:8000/user/me', {}, {
            headers: {
              'accept': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });
          this.roles = response.data.data.roles;
        } catch (error) {
          console.error('Error fetching user data:', error);
        }
      }
    },
    methods: {
      logout() {
        localStorage.removeItem('token');
        this.isAuthenticated = false;
        this.roles = {
          is_admin: false,
          is_veterinarian: false,
          is_government: false,
        };
        this.$router.push('/signin');
      },
      toggleLanguage() {
        const newLocale = this.$i18n.locale === 'en' ? 'uk' : 'en';
        this.$i18n.locale = newLocale;
      }
    }
  };
  </script>
  
  <style scoped>
  .navbar {
    background-color: #f8f9fa;
  }
  .nav-link {
    color: #555;
  }
  .nav-link:hover {
    color: #000;
  }
  </style>
  
  