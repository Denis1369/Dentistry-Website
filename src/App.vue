<script setup>
import { ref, computed } from 'vue'
import Registration from './views/registration.vue'
import MainWindow from './views/mainWindow.vue'
import LoginForm from './views/LoginForm.vue'
import Contacts from './views/ContactsForm.vue'

const currentView = ref('main') 
const showRegistration = ref(false)
const showLogin = ref(false)

const currentComponent = computed(() => {
  switch (currentView.value) {
    case 'main':
      return MainWindow
    case 'contacts':
      return Contacts
    default:
      return MainWindow
  }
})

const switchView = (viewName) => {
  currentView.value = viewName
}

const openRegistration = () => {
  showRegistration.value = true
  document.body.style.overflow = 'hidden'
}

const closeRegistration = () => {
  showRegistration.value = false
  document.body.style.overflow = 'auto'
}

const handleRegistrationSuccess = (userData) => {
  console.log('Пользователь зарегистрирован:', userData)
  closeRegistration()
}

const openLogin = () => {
  showLogin.value = true
  document.body.style.overflow = 'hidden'
}

const closeLogin = () => {
  showLogin.value = false
  document.body.style.overflow = 'auto'
}

const handleLoginSuccess = (userData) => {
  console.log('Пользователь авторизован:', userData)
  closeLogin()
}

const switchToRegistration = () => {
  closeLogin()
  openRegistration()
}

const switchToLogin = () => {
  closeRegistration()
  openLogin()
}

const provideData = {
  switchView,
  openRegistration,
  openLogin
}
</script>

<template>
  <div id="app">
    <component 
      :is="currentComponent"
      v-bind="provideData"
      @open-registration="openRegistration"
      @open-login="openLogin"
    />
    
    <div v-if="showRegistration" class="modal-overlay">
      <div class="modal-content">
        <Registration 
          @registration-success="handleRegistrationSuccess"
          @switch-to-login="switchToLogin"
          @close="closeRegistration"
        />
      </div>
    </div>
    
    <div v-if="showLogin" class="modal-overlay">
      <div class="modal-content">
        <LoginForm 
          @login-success="handleLoginSuccess"
          @switch-to-registration="switchToRegistration"
          @close="closeLogin"
        />
      </div>
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: white;
  min-height: 100vh;
  overflow-x: hidden;
}

#app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  overflow-y: auto;
}

.modal-content {
  background: white;
  max-width: 480px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border-radius: 12px;
}

.modal-overlay {
  animation: fadeIn 0.3s ease;
}

.modal-content {
  animation: slideUp 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}
</style>