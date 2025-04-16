import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import authService from './services/authService'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"

const app = createApp(App)

//set access_token before mounting the app
authService.loadTokenFromStorage();
app.use(router)
app.mount('#app')