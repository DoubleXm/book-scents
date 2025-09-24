import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: () => import('@/views/home-page/HomePage.vue')
  },
  {
    path: '/books',
    name: 'BooksPage',
    component: () => import('@/views/book-list/BookList.vue'),
  },
  {
    path: '/books/:id',
    name: 'BookDetailPage',
    component: () => import('@/views/book-detail/BookDetail.vue')
  },
  {
    path: '/book/upload',
    name: 'BookUploadPage',
    component: () => import('@/views/book-upload/BookUpload.vue')
  },
  {
    path: '/profile',
    name: 'ProfilePage',
    component: () => import('@/views/profile/UserProfile.vue')
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: () => import('@/views/profile/UserLogin.vue')
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: () => import('@/views/profile/UserRegister.vue')
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
