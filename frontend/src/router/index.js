import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BooksView from '@/views/BooksView.vue'
import ReadingList from '@/views/ReadingList.vue'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/books', 
      name: 'books', 
      component: BooksView,
    }, 
    {
      path: '/reading-list', 
      name: 'reading-list', 
      component: ReadingList,
    }, 
    {
      path: '/auth/login', 
      name: 'login', 
      component: LoginView,
    }
  ],
})

export default router
