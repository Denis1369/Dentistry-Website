<script setup>
import { ref, computed } from 'vue'
import Registration from './views/registration.vue'
import MainWindow from './views/mainWindow.vue'
import LoginForm from './views/LoginForm.vue'
import Contacts from './views/ContactsForm.vue'
import ApointmentForm from './views/ApointmentForm.vue'

const currentView = ref('main') 
const showRegistration = ref(false)
const showLogin = ref(false)
const showAppointment = ref(false)

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

const openAppointment = () => {
  showAppointment.value = true
  document.body.style.overflow = 'hidden'
}

const closeAppointment = () => {
  showAppointment.value = false
  document.body.style.overflow = 'auto'
}

const handleAppointmentSuccess = (appointmentData) => {
  console.log('Запись создана:', appointmentData)
  closeAppointment()
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
  openLogin,
  openAppointment
}
</script>

<template>
  <header class="header">
      <div class="header-content">
        <div class="name-dent">
          <img src="/src/components/icons/icons8-зуб-100.png" alt="Dental Tech"/>
          <h1>Dental Tech</h1>
        </div>
        <nav class="navigation">
          <a @click="switchView('main')" style="cursor: pointer; background-color: #ffffff15;">О нас</a>
          <a href="">Услуги</a>
          <a href="">Врачи</a>
          <a @click="switchView('contacts')" style="cursor: pointer;">Контакты</a>
        </nav>
        <div class="account">
            <button @click="openLogin()" class="nav-button">
                <img src="/src/components/icons/icons8-тестовый-аккаунт-100.png" alt="Аккаунт">
          </button>
          <button @click="openAppointment" class="btn-appointment">Записаться</button>
        </div>
      </div>
    </header>
  <div id="app">
    <component 
      :is="currentComponent"
      v-bind="provideData"
      @open-registration="openRegistration"
      @open-login="openLogin"
    />

    <div v-if="showAppointment" class="modal-overlay">
      <div class="modal-content">
        <ApointmentForm
          @appointment-success="handleAppointmentSuccess"
          @close="closeAppointment"
        />
      </div>
    </div>
    
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

.header {
  width: 100%;
  background: #5285ff;
  position: fixed;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.name-dent {
  display: flex;
  align-items: center;
  gap: 12px;
}

.name-dent img {
  width: 60px;
  height: 60px;
}

.name-dent h1 {
  font-size: 24px;
  font-weight: 700;
  color: white;
}

.navigation {
  display: flex;
  gap: 25px;
}

.navigation a {
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  background-color: #ffffff15;
  border-radius: 30px;
  padding: 10px 20px;
  transition: opacity 0.3s ease;
}

.navigation a:hover {
  opacity: 0.8;
  background-color: #ffffff20;
}

.account .nav-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.account img {
  width: 32px;
  height: 32px;
}

.account {
  display: flex;
  flex-direction: row;
  gap: 20px;
}
.btn-appointment {
  background: white;
  color: #667eea;
  border: none;
  padding: 10px 30px;
  border-radius: 30px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 250px;
}

.btn-appointment:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
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