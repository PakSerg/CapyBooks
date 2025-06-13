import './assets/reset.css'
import './assets/style.css'
import './assets/config.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import AuthService from './services/AuthService'

const app = createApp(App)

AuthService.initializeAxios();

app.use(router)

app.mount('#app')
