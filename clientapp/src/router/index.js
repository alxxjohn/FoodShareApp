import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/MainView.vue'
import Login from '@/views/LoginView.vue'
import HomePage from '@/views/HomePage.vue'
// import Dashboard from '@/views/Dashboard.vue'
// import store from '@/store' // Assuming you manage authentication state in Vuex or Pinia

const routes = [
  // { path: '/', redirect: '/main' }, // Redirect root to /main
  { path: '/', component:  HomePage},
  { path: '/main', component: Main },
  { path: '/login', component: Login }
  // { path: '/dashboard', component: Dashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// // Navigation Guard for Authentication
// router.beforeEach((to, from, next) => {
//   const isAuthenticated = store.state.user.isLoggedIn // Replace with actual auth logic

//   if (to.path !== '/login' && !isAuthenticated) {
//     next('/login') // Redirect to login if not authenticated
//   } else {
//     next() // Proceed as normal
//   }
// })

export default router