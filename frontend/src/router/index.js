import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BooksView from '@/views/BooksView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ReadingListView from '@/views/ReadingListView.vue'

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
      component: ReadingListView,
    }, 
    {
      path: '/auth/login', 
      name: 'login', 
      component: LoginView,
    },
    {
      path: '/auth/register', 
      name: 'register', 
      component: RegisterView,
    },
  ],
})

export default router
