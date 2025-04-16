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

const routes = [
  // { path: '/', redirect: '/main' }, // Redirect root to /main
  { path: '/', component:  homePage},
  { path: '/main', component: main, meta: { requiresAuth: true } },
  { path: '/login', component: login },
  { path: '/signup', component: signUp },
  { path: '/termsandconditions', component: termsAndConditions },
  { path: '/userhome', name: userhome, component: userhome, meta: { requiresAuth: true } },
  { path: '/foodmap', component: foodMap, meta: { requiresAuth: true } },
  { path: '/reservation-list', component: reservationList, meta: { requiresAuth: true } },
  { path: '/donation', component: donation, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Global navigation guard
router.beforeEach((to, from, next) => {
  const token = !!localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/signup') && token) {
    next('/main')
  } else {
    next()
  }
})


export default router
