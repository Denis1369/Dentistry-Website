<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Registration from './views/registration.vue'
import LoginForm from './views/LoginForm.vue'
import ApointmentForm from './views/ApointmentForm.vue'
import feedbackVue from './views/feedbackVue.vue'

const router = useRouter()
const route = useRoute()

const showRegistration = ref(false)
const showLogin = ref(false)
const showAppointment = ref(false)

const navigateToMain = () => {
  router.push('/')
}

const authState = ref(!!localStorage.getItem('authToken'))

const isAuthenticated = computed(() => {
  return authState.value
})

const updateAuthState = () => {
  authState.value = !!localStorage.getItem('authToken')
}

const navigateToContacts = () => {
  router.push('/contacts')
}

const navigateToServices = () => {
  router.push('/services')
}

const navigateToDoctors = () => {
  router.push('/doctors')
}

const handleAccountClick = () => {
  if (isAuthenticated.value) {
    const userData = JSON.parse(localStorage.getItem('userData') || '{}')
    const userRole = userData.user_role
    
    if (userRole === 'врач') {
      router.push('/doctor-account')
    } else {
      router.push('/account')
    }
  } else {
    openLogin()
  }
}

const navigateToReviews = () => {
  router.push('/reviews')
}

const openAppointment = () => {
  if (!isAuthenticated.value) {
    // Если не авторизован, открываем окно авторизации с сообщением
    alert('Для записи на прием необходимо авторизоваться')
    openLogin()
    return
  }
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
  updateAuthState()
  closeLogin()
  
  const storedUserData = JSON.parse(localStorage.getItem('userData') || '{}')
  const userRole = storedUserData.user_role || storedUserData.role
  
  if (userRole === 'врач' || userRole === 'doctor' || userRole === 'доктор') {
    router.push('/doctor-account')
  }
}

const handleDoctorFormOpen = () => {
  closeLogin()
  router.push('/doctor-account')
}

const switchToRegistration = () => {
  closeLogin()
  openRegistration()
}

const switchToLogin = () => {
  closeRegistration()
  openLogin()
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
        <a 
          @click="navigateToMain" 
          :class="{ active: route.path === '/' }"
          style="cursor: pointer;"
        >
          О нас
        </a>
        <a 
          @click="navigateToServices" 
          :class="{ active: route.path === '/services' }"
          style="cursor: pointer;"
        >
          Услуги
        </a>
        <a 
          @click="navigateToDoctors" 
          :class="{ active: route.path === '/doctors' }"
          style="cursor: pointer;"
        >
          Врачи
        </a>
        <a 
          @click="navigateToContacts" 
          :class="{ active: route.path === '/contacts' }"
          style="cursor: pointer;"
        >
          Контакты
        </a>
        <a
        @click="navigateToReviews"
        :class="{active: route.path === '/reviews'}"
        style="cursor: pointer;">
          Отзывы
        </a>
      </nav>
      <div class="account">
        <button @click="handleAccountClick" class="nav-button">
          <img src="/src/components/icons/icons8-тестовый-аккаунт-100.png" alt="Аккаунт">
          <div v-if="isAuthenticated" class="auth-indicator"></div>
        </button>
        <button @click="openAppointment" class="btn-appointment">Записаться</button>
      </div>
    </div>
  </header>

  <div id="app">
    <router-view class="content"/>
    
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
          @open-doctor-form="handleDoctorFormOpen"
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
.content{
  margin-top: 10%;
}
.header {
  width: 99.2%;
  background: #5285ff;
  position: fixed;
  z-index: 800;
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