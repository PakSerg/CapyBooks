<script>
import axios from 'axios'
import router from '@/router'
import AuthService from '@/services/AuthService.js'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: null
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/users/auth/login/', {
          username: this.username,
          password: this.password
        });
        
        const token = response.data.auth_token;
        console.log(token)
        localStorage.setItem('authToken', token);
        axios.defaults.headers.common['Authorization'] = `Token ${token}`;

        localStorage.setItem('username', response.data.user.username);

        console.log('Успешный вход!', response.data);
        this.error = null;
        // router.push({ name: 'books' });
      } catch (error) {
        this.error = 'Неверный логин или пароль';
        console.error('Ошибка входа:', error.response ? error.response.data : error.message);
      }
    }
  }
}
</script>

<template>
  <main>
    <section class="container login-container">
        <form @submit.prevent="login">
            <h1 class="font-special">Вход</h1>
            <div class="input-container">
                <label class="font-special" for="username">Логин</label>
                <input type="text" id="username" name="username" v-model="username">
            </div>
            <div class="input-container">
                <label class="font-special" for="password">Пароль</label>
                <input type="password" id="password" name="password" v-model="password">
            </div>
            <div class="button-container">
                <button type="submit" class="font-special">Войти</button>
                <p class="font-special">Ещё нет аккаунта?</p>
            </div>
            <p v-if="error" class="error-message font-special">{{ error }}</p>
        </form>
    </section>
  </main>
</template>

<style scoped>
h1 {
    text-align: center;
}
.login-container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: calc((100vh) - 310px);
}
.input-container {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
form {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 360px;
}
.error-message {
    color: #ff4444;
    text-align: center;
    margin-top: 10px;
}
input {
    padding: 10px 12px;
    border: 1px solid var(--dark-color);
    border-radius: 12px;
}
.button-container {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    gap: 16px;
}
button {
    padding: 16px 52px;
    border-radius: 12px;
    width: fit-content;
    background-color: var(--dark-color);
    color: white;
    font-size: 18px;
}
form * {
    font-family: var(--font-special), sans-serif;
}
.button-container p {
    font-size: 14px;
    color: var(--pale-color);
}
</style>
