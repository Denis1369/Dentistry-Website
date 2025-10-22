<script setup>
import { ref, reactive } from 'vue'

const emit = defineEmits(['login-success', 'switch-to-registration', 'close'])

const closeForm = () => {
  emit('close')
}

const switchToRegistration = () => {
  emit('switch-to-registration')
}

const email = ref('')
const password = ref('')
const loading = ref(false)
const successMessage = ref('')
const showPassword = ref(false)

const errors = reactive({
  email: '',
  password: ''
})

const validateEmail = () => {
  errors.email = ''
  
  if (!email.value) {
    errors.email = 'Email обязателен для заполнения'
    return false
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    errors.email = 'Введите корректный email адрес'
    return false
  }
  
  return true
}

const validatePassword = () => {
  errors.password = ''
  
  if (!password.value) {
    errors.password = 'Пароль обязателен для заполнения'
    return false
  }
  
  if (password.value.length < 6) {
    errors.password = 'Пароль должен содержать минимум 6 символов'
    return false
  }
  
  return true
}

const validateForm = () => {
  const isEmailValid = validateEmail()
  const isPasswordValid = validatePassword()
  
  return isEmailValid && isPasswordValid
}

const handleLogin = async () => {
  errors.email = ''
  errors.password = ''
  successMessage.value = ''

  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    const response = await fetch('http://127.0.0.1:8000/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_email: email.value,
        user_password: password.value,
      }),
    })

    const data = await response.json()

    if (response.ok) {
      successMessage.value = 'Успешный вход! Добро пожаловать в систему!'
      email.value = ''
      password.value = ''

      setTimeout(() => {
        successMessage.value = '' 
        emit('login-success', data)
      }, 2000)

    } 
    else {
      if (data?.message) {
        errors.password = data.message
      } else {
        errors.password = 'Неверный email или пароль'
      }
    }
  } catch (error) {
    console.error('Ошибка при входе:', error)
    errors.password = 'Произошла ошибка. Попробуйте позже.'
  } finally {
    loading.value = false
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}
</script>

<template>
  <div class="auth-container">
    <div class="header-actions">
      <button @click="closeForm" class="close-button">×</button>
    </div>
    
    <div class="auth-header">
      <h2>Авторизация</h2>
    </div>
    
    <form @submit.prevent="handleLogin" class="auth-form">
      <div class="input-group">
        <label class="input-label">Электронная почта</label>
        <input 
          type="email" 
          v-model="email" 
          placeholder="example@email.com"
          required
          :class="{'error-input': errors.email}"
          @blur="validateEmail"
          class="form-input"
        >
        <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
      </div>
      
      <div class="input-group">
        <label class="input-label">Пароль</label>
        <div class="password-input-wrapper">
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="password" 
            placeholder="Введите пароль"
            required
            :class="{'error-input': errors.password}"
            @blur="validatePassword"
            class="form-input password-input"
          >
          <span class="password-toggle" @click="togglePasswordVisibility">
            {{ showPassword ? '🙈' : '🙉' }}
          </span>
        </div>
        <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
      </div>
      
      <button type="submit" class="auth-btn" :disabled="loading">
        <span v-if="!loading">Войти</span>
        <span v-else>Вход...</span>
      </button>
      
      <div class="switch-link">
        Нет аккаунта? 
        <a href="#" @click.prevent="switchToRegistration" class="switch-link-text">Зарегистрироваться</a>
      </div>
      
      <div v-if="successMessage" class="message success">
        {{ successMessage }}
      </div>
    </form>
  </div>
</template>

<style scoped>
.auth-container {
  padding: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
  position: relative;
}

.header-actions {
  position: absolute;
  top: 20px;
  right: 20px;
  z-index: 10;
}

.close-button {
  background: #f8f9fa;
  border: none;
  font-size: 28px;
  cursor: pointer;
  color: #666;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-weight: 300;
}

.close-button:hover {
  background: #e9ecef;
  color: #333;
}

.auth-header {
  padding: 40px 40px 30px 40px;
  border-bottom: 1px solid #f1f3f4;
  background: white;
}

.auth-header h2 {
  text-align: center;
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
}

.auth-form {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 30px 40px 40px 40px;
  gap: 20px;
  overflow-y: auto;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 4px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  background: white;
  color: #2d3748;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #a0aec0;
}

.error-input {
  border-color: #e53e3e !important;
  box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.1) !important;
}

.error-message {
  color: #e53e3e;
  font-size: 12px;
  font-weight: 500;
  margin-top: 4px;
}

.password-input-wrapper {
  position: relative;
  width: 100%;
}

.password-input {
  padding-right: 50px;
}

.password-toggle {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  user-select: none;
  color: #718096;
  font-size: 18px;
  background: none;
  border: none;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.password-toggle:hover {
  background: #f7fafc;
}

.auth-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.auth-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.auth-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.switch-link {
  text-align: center;
  margin-top: 20px;
  color: #718096;
  font-size: 14px;
}

.switch-link-text {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
  cursor: pointer;
}

.switch-link-text:hover {
  color: #5a67d8;
  text-decoration: underline;
}

.message {
  margin-top: 20px;
  padding: 12px 16px;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
  font-size: 14px;
}

.error {
  background-color: #fed7d7;
  color: #c53030;
  border: 1px solid #feb2b2;
}

.success {
  background-color: #c6f6d5;
  color: #276749;
  border: 1px solid #9ae6b4;
}

/* Убираем скролл для формы */
.auth-form::-webkit-scrollbar {
  width: 0px;
}

/* Адаптивность */
@media (max-width: 480px) {
  .auth-header {
    padding: 30px 20px 20px 20px;
  }
  
  .auth-form {
    padding: 20px 20px 30px 20px;
  }
  
  .header-actions {
    top: 15px;
    right: 15px;
  }
  
  .close-button {
    width: 35px;
    height: 35px;
    font-size: 24px;
  }
}
</style>