import { createRouter, createWebHistory } from 'vue-router'
import main from '@/views/mainView.vue'
import login from '@/views/loginView.vue'
import signUp from '@/views/signUpView.vue'
import homePage from '@/views/homePage.vue'
import termsAndConditions from '@/views/termsAndConditions.vue'
import foodMap from '@/views/FoodMapView.vue'

// import Dashboard from '@/views/Dashboard.vue'
// import store from '@/store' // Assuming you manage authentication state in Vuex or Pinia

const routes = [
  // { path: '/', redirect: '/main' }, // Redirect root to /main
  { path: '/', component:  homePage},
  { path: '/main', component: main },
  { path: '/login', component: login },
  { path: '/signup', component: signUp },
  { path: '/termsandconditions', component: termsAndConditions }
  { path: '/foodmap', component: foodMap }
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
