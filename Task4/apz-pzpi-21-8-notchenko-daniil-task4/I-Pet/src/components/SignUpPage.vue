<template>
  <div>
    <form @submit.prevent="handleSubmit">
      <h1 class="h3 mb-3 fw-normal">{{ $t('registration') }}</h1>
  
      <div class="form-floating">
        <input type="text" class="form-control" id="username" v-model="username"
         :placeholder="$t('enterYourUsername')">
        <label for="username">{{ $t('username') }}:</label>
      </div>
      <div class="form-floating">
        <input type="email" class="form-control" id="email" v-model="email"
         :placeholder="$t('enterYourEmail')">
        <label for="email">{{ $t('email') }}:</label>
      </div>
      <div class="form-floating">
        <input type="password" class="form-control" id="passw" v-model="password"
         :placeholder="$t('enterYourPassword')" autocomplete>
        <label for="passw">{{ $t('password') }}:</label>
      </div>
  
      <button class="btn btn-primary w-50 py-2" type="submit">{{ $t('register') }}</button>
    </form>

    <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
      {{ successMessage }}
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';

export default {
  name: 'SignUpPage',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      successMessage: ''
    }
  },
  methods: {
    async handleSubmit() {
      const response = await axios.post('registration',{
        username: this.username,
        email: this.email,
        password: this.password
      });
      console.log(response.data);
      this.successMessage = response.data.message;
      this.$router.push('/signin')
    }
  }
}
</script>

<style>
.component-panel {
  border: 1px solid silver;
  border-radius: 15px; 
  margin-top: 30px;
  padding: 20px; 
}
form {
  width: 50%;
  margin: 20px auto;
}
</style>

  