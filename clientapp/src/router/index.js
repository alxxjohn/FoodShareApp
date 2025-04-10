import { createRouter, createWebHistory } from 'vue-router'
import main from '@/views/MainView.vue'
import login from '@/views/LoginView.vue'
import signUp from '@/views/SignUpView.vue'
import homePage from '@/views/HomePage.vue'
import termsAndConditions from '@/views/TermsAndConditions.vue'
import foodMap from '@/views/FoodMapView.vue'
import userhome from '@/views/UserHome.vue'
import reservationList from '@/views/ReservationListView.vue'
import donation from '@/views/DonationView.vue'
// import Dashboard from '@/views/Dashboard.vue'
// import store from '@/store' // Assuming you manage authentication state in Vuex or Pinia

const routes = [
  // { path: '/', redirect: '/main' }, // Redirect root to /main
  { path: '/', component:  homePage},
  { path: '/main', component: main },
  { path: '/login', component: login },
  { path: '/signup', component: signUp },
  { path: '/termsandconditions', component: termsAndConditions },
  { path: '/userhome', name: userhome, component: userhome }
  { path: '/foodmap', component: foodMap },
  { path: '/reservation-list', component: reservationList },
  { path: '/donation', component: donation }
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
