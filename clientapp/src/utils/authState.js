import { ref } from 'vue'

export const isLoggedIn = ref(!!localStorage.getItem('access_token'));
export const isBusiness = ref(localStorage.getItem('is_business'));