import { createRouter, createWebHistory } from 'vue-router'
import MainWindow from '../views/mainWindow.vue'
import Contacts from '../views/ContactsForm.vue'
import services from '../views/ServicesForm.vue'
import doctors from '../views/DoctorsForm.vue'
import account from '../views/AccountForm.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainWindow
  },
  {
    path: '/contacts',
    name: 'contacts',
    component: Contacts
  },
  {
    path: '/services',
    name: 'services',
    component: services
  },
  {
    path: '/doctors',
    name: 'doctors',
    component: doctors
  },
  {
    path: '/account',
    name: 'account',
    component: account
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router