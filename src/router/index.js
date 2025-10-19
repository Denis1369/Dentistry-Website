import { createRouter, createWebHistory } from 'vue-router'
import MainWindow from '../views/mainWindow.vue'
import Contacts from '../views/ContactsForm.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router