<template>
  <form @submit.prevent="handleSubmit">
  <h1 class="h3 mb-3 fw-normal">{{ $t('authorization') }}</h1>

  <div class="form-floating">
    <input type="text" class="form-control" id="login" v-model="username"
    :placeholder="$t('enterYourLogin')">
    <label for="login">{{ $t('login') }}:</label>
  </div>
  <div class="form-floating">
    <input type="password" class="form-control" id="passw" v-model="password"
    :placeholder="$t('enterYourPassword')" autocomplete>
    <label for="passw">{{ $t('password') }}:</label>
  </div>

  <div class="form-check text-start my-3">
    <input class="form-check-input" type="checkbox" value="remember-me" id="remember">
    <label class="remember" for="flexCheckDefault">
      {{ $t('stayLoggedIn') }}
    </label>
  </div>
  <button class="btn btn-primary w-50 py-2" type="submit">{{ $t('signIn') }}</button>
</form>
</template>


<script>

import axios from 'axios';

export default {
name: 'SignInPage',
data() {
  return {
    username: '',
    password: ''
  }
},
methods: {
  async handleSubmit() {
    const data = new URLSearchParams();
    data.append('username', this.username);
    data.append('password', this.password);
      const response = await axios.post('/token', data, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      console.log('Server Response:', response.data);
    
    const token = response.data.access_token
    localStorage.setItem('token', token);
  }
}
}

</script> 


<style>
  .component-panel{
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
