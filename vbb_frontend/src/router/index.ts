import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import SearchView from '../views/SearchView.vue'
import LiveBoardView from '../views/LiveBoardView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/live',
      name: 'LiveBoard',
      component: LiveBoardView
    }
  ]
})

export default router