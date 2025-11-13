<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Registration from './views/registration.vue'
import LoginForm from './views/LoginForm.vue'
import ApointmentForm from './views/ApointmentForm.vue'
import VerificationForm from './views/VerificationForm.vue'

const router = useRouter()
const route = useRoute()

const showRegistration = ref(false)
const showLogin = ref(false)
const showAppointment = ref(false)
const showVerification = ref(false)
const pendingEmail = ref('')

const userData = ref(JSON.parse(localStorage.getItem('userData') || '{}'))

const navigateToMain = () => {
  if (shouldDisableNavigation.value) return
  router.push('/')
}

const authState = ref(!!localStorage.getItem('authToken'))

const isAuthenticated = computed(() => {
  return authState.value && Object.keys(userData.value).length > 0
})

const userRole = computed(() => {
  if (!isAuthenticated.value) return null
  return userData.value.user_role || userData.value.role || null
})

const isDoctor = computed(() => {
  return userRole.value === 'врач'
})

const shouldShowAppointmentButton = computed(() => {
  if (!isAuthenticated.value) return true
  if (!isDoctor.value) return true
  return false
})

const shouldDisableNavigation = computed(() => {
  return isAuthenticated.value && isDoctor.value
})

const updateAuthState = () => {
  const token = localStorage.getItem('authToken')
  const storedUserData = localStorage.getItem('userData')
  
  authState.value = !!token
  
  if (storedUserData) {
    try {
      userData.value = JSON.parse(storedUserData)
    } catch (error) {
      console.error('Error parsing userData:', error)
      userData.value = {}
    }
  } else {
    userData.value = {}
  }
  
  console.log('Auth updated:', {
    isAuthenticated: isAuthenticated.value,
    userRole: userRole.value,
    isDoctor: isDoctor.value,
    shouldShowAppointment: shouldShowAppointmentButton.value,
    shouldDisableNavigation: shouldDisableNavigation.value
  })
}

watch(() => localStorage.getItem('userData'), (newValue) => {
  if (newValue) {
    try {
      userData.value = JSON.parse(newValue)
    } catch (error) {
      console.error('Error parsing userData:', error)
      userData.value = {}
    }
  } else {
    userData.value = {}
  }
  
  console.log('UserData changed:', {
    userData: userData.value,
    isDoctor: isDoctor.value
  })
})

watch(() => localStorage.getItem('authToken'), (newValue) => {
  authState.value = !!newValue
})

const navigateToContacts = () => {
  if (shouldDisableNavigation.value) return
  router.push('/contacts')
}

const navigateToServices = () => {
  if (shouldDisableNavigation.value) return
  router.push('/services')
}

const navigateToDoctors = () => {
  if (shouldDisableNavigation.value) return
  router.push('/doctors')
}

const handleAccountClick = () => {
  if (isAuthenticated.value) {
    if (isDoctor.value) {
      router.push('/doctor-account')
    } else {
      router.push('/account')
    }
  } else {
    openLogin()
  }
}

const navigateToReviews = () => {
  if (shouldDisableNavigation.value) return
  router.push('/reviews')
}

const openAppointment = () => {
  if (!isAuthenticated.value) {
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

const openVerification = (email) => {
  pendingEmail.value = email
  showVerification.value = true
  document.body.style.overflow = 'hidden'
}

const closeVerification = () => {
  showVerification.value = false
  document.body.style.overflow = 'auto'
  pendingEmail.value = ''
}

const handleSwitchToVerification = (email) => {
  closeRegistration()
  openVerification(email)
}

const handleVerificationSuccess = (email) => {
  console.log('Email подтвержден:', email)
  closeVerification()
  openLoginWithEmail(email)
}

const handleLoginSuccess = (loginData) => {
  console.log('Пользователь авторизован:', loginData)
  updateAuthState()
  closeLogin()
  
  if (isDoctor.value) {
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

const switchToLoginFromVerification = () => {
  closeVerification()
  openLogin()
}

const switchToRegistrationFromVerification = () => {
  closeVerification()
  openRegistration()
}

const openLoginWithEmail = (email) => {
  pendingEmail.value = email
  openLogin()
}

onMounted(() => {
  updateAuthState()
})

watch(() => route.path, () => {
  updateAuthState()
})

updateAuthState()
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
          :class="{ 
            active: route.path === '/', 
            disabled: shouldDisableNavigation 
          }"
          :style="{
            cursor: shouldDisableNavigation ? 'not-allowed' : 'pointer',
            opacity: shouldDisableNavigation ? 0.5 : 1
          }"
        >
          О нас
        </a>
        <a 
          @click="navigateToServices" 
          :class="{ 
            active: route.path === '/services', 
            disabled: shouldDisableNavigation 
          }"
          :style="{
            cursor: shouldDisableNavigation ? 'not-allowed' : 'pointer',
            opacity: shouldDisableNavigation ? 0.5 : 1
          }"
        >
          Услуги
        </a>
        <a 
          @click="navigateToDoctors" 
          :class="{ 
            active: route.path === '/doctors', 
            disabled: shouldDisableNavigation 
          }"
          :style="{
            cursor: shouldDisableNavigation ? 'not-allowed' : 'pointer',
            opacity: shouldDisableNavigation ? 0.5 : 1
          }"
        >
          Врачи
        </a>
        <a 
          @click="navigateToContacts" 
          :class="{ 
            active: route.path === '/contacts', 
            disabled: shouldDisableNavigation 
          }"
          :style="{
            cursor: shouldDisableNavigation ? 'not-allowed' : 'pointer',
            opacity: shouldDisableNavigation ? 0.5 : 1
          }"
        >
          Контакты
        </a>
        <a
          @click="navigateToReviews"
          :class="{
            active: route.path === '/reviews',
            disabled: shouldDisableNavigation
          }"
          :style="{
            cursor: shouldDisableNavigation ? 'not-allowed' : 'pointer',
            opacity: shouldDisableNavigation ? 0.5 : 1
          }"
        >
          Отзывы
        </a>
      </nav>
      <div class="account">
        <button @click="handleAccountClick" class="nav-button">
          <img src="/src/components/icons/icons8-тестовый-аккаунт-100.png" alt="Аккаунт">
          <div v-if="isAuthenticated" class="auth-indicator"></div>
        </button>
        <button 
          v-if="shouldShowAppointmentButton" 
          @click="openAppointment" 
          class="btn-appointment"
        >
          Записаться
        </button>
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
          @switch-to-verification="handleSwitchToVerification"
          @close="closeRegistration"
        />
      </div>
    </div>
    
    <div v-if="showVerification" class="modal-overlay">
      <div class="modal-content">
        <VerificationForm 
          :email="pendingEmail"
          @verification-success="handleVerificationSuccess"
          @switch-to-login="switchToLoginFromVerification"
          @switch-to-registration="switchToRegistrationFromVerification"
          @close="closeVerification"
        />
      </div>
    </div>
    
    <div v-if="showLogin" class="modal-overlay">
      <div class="modal-content">
        <LoginForm 
          :initial-email="pendingEmail"
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

.content {
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
  transition: all 0.3s ease;
}

.navigation a:hover:not(.disabled) {
  opacity: 0.8;
  background-color: #ffffff20;
}

.navigation a.disabled {
  cursor: not-allowed !important;
  opacity: 0.5 !important;
}

.navigation a.disabled:hover {
  background-color: #ffffff15 !important;
  opacity: 0.5 !important;
}

.account .nav-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
  position: relative;
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

.auth-indicator {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 8px;
  height: 8px;
  background: #4CAF50;
  border-radius: 50%;
  border: 2px solid white;
}

.btn-appointment {
  background: white;
  color: #5285ff;
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

@media (max-width: 480px) {
  .modal-content {
    max-width: 95%;
    max-height: 90vh;
  }
  
  .header-content {
    padding: 15px;
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .navigation {
    order: 3;
    width: 100%;
    justify-content: center;
    gap: 10px;
  }
  
  .navigation a {
    font-size: 14px;
    padding: 8px 15px;
  }
}
</style>