<template>
    <div>
      <h4>{{ $t('homePageTitle') }}</h4>
      <h5 v-if="user">{{ $t('loggedInMessage') }}, {{ user.username }}!</h5>
      <h5 v-else>{{ $t('notLoggedInMessage') }}</h5>
      <h5>{{ $t('halloMassage') }}</h5>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'HomePage',
    data() {
      return {
        user: null
      };
    },
    async created() {
      try {
        const response = await axios.post('user/me');
        this.user = response.data.data;
        console.log(this.user);
      } catch (error) {
        console.error('An error occurred:', error);
      }
    }
  };
  </script>
  
  <style>
  </style>
  