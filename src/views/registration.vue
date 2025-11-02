<script setup>
import { ref, reactive, computed } from 'vue'
import axios from 'axios'

const emit = defineEmits(['registration-success', 'switch-to-login', 'close'])

const formData = reactive({
  lastname: '',
  firstname: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  lastname: '',
  firstname: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref('')

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/user/',
  
  timeout: 10000,
  headers: {'Content-Type': 'application/json'}
});


const validateField = (fieldName) => {
  const value = formData[fieldName]
  
  switch (fieldName) {
    case 'lastname':
      if (!value.trim()) {
        errors.lastname = 'Фамилия обязательна для заполнения'
      } else if (value.length < 2) {
        errors.lastname = 'Фамилия должна содержать минимум 2 символа'
      } else if (!/^[a-zA-Zа-яА-ЯёЁ\s\-]+$/.test(value)) {
        errors.lastname = 'Фамилия может содержать только буквы, пробелы и дефисы'
      } else {
        errors.lastname = ''
      }
      break
      
    case 'firstname':
      if (!value.trim()) {
        errors.firstname = 'Имя обязательно для заполнения'
      } else if (value.length < 2) {
        errors.firstname = 'Имя должно содержать минимум 2 символа'
      } else if (!/^[a-zA-Zа-яА-ЯёЁ\s\-]+$/.test(value)) {
        errors.firstname = 'Имя может содержать только буквы, пробелы и дефисы'
      } else {
        errors.firstname = ''
      }
      break
      
    case 'email':
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!value.trim()) {
        errors.email = 'Email обязателен для заполнения'
      } else if (!emailRegex.test(value)) {
        errors.email = 'Введите корректный email адрес'
      } else {
        errors.email = ''
      }
      break
      
    case 'password':
      if (!value) {
        errors.password = 'Пароль обязателен для заполнения'
      } else if (value.length < 8) {
        errors.password = 'Пароль должен содержать минимум 8 символов'
      } else if (value.length > 12) {
        errors.password = 'Пароль должен содержать не более 12 символов'
      } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
        errors.password = 'Пароль должен содержать хотя бы одну заглавную букву, одну строчную букву и одну цифру'
      } else {
        errors.password = ''
      }
      break
      
    case 'confirmPassword':
      if (!value) {
        errors.confirmPassword = 'Подтверждение пароля обязательно'
      } else if (value !== formData.password) {
        errors.confirmPassword = 'Пароли не совпадают'
      } else {
        errors.confirmPassword = ''
      }
      break
  }
}

const isFormValid = computed(() => {
  return (
    formData.lastname &&
    formData.firstname &&
    formData.email &&
    formData.password &&
    formData.confirmPassword &&
    !errors.lastname &&
    !errors.firstname &&
    !errors.email &&
    !errors.password &&
    !errors.confirmPassword
  )
})

const handleSubmit = async () => {
  validateField('lastname')
  validateField('firstname')
  validateField('email')
  validateField('password')
  validateField('confirmPassword')
  
  if (!isFormValid.value) {
    message.value = 'Пожалуйста, исправьте ошибки в форме'
    messageType.value = 'error'
    return
  }
  
  isSubmitting.value = true
  message.value = ''
  const a = {
    username: formData.email.replace('@', '').replace('.ru', '').replace('.com',''),
      email: formData.email.trim(),
      password: formData.password,
      first_name: formData.firstname.trim(),
      last_name: formData.lastname.trim()
  }
  console.log(a)
  
  try {
    const response = await instance.post('/register/', {
      username: formData.email.replace('@', '').replace('.ru', '').replace('.com',''),
      email: formData.email.trim(),
      password: formData.password,
      first_name: formData.firstname.trim(),
      last_name: formData.lastname.trim(),
      user_role: 'пользователь'
      
    })
    const data = response.data
    if (response.status === 200) {
      message.value = data.message || 'Регистрация прошла успешно!'
      messageType.value = 'success'
      
      formData.lastname = ''
      formData.firstname = ''
      formData.email = ''
      formData.password = ''
      formData.confirmPassword = ''

      setTimeout(() => {
        emit('switch-to-login')
      }, 2000)
      
    } 
  } catch (error) {
    console.error('Ошибка при регистрации:', error)
    
    if (error.response) {
      const status = error.response.status
      const errorData = error.response.data
      
      if (status === 400) {
        if (errorData.message) {
          message.value = errorData.message
        } else if (errorData.non_field_errors) {
          message.value = errorData.non_field_errors[0]
        } else if (errorData.user_email) {
          errors.email = errorData.user_email[0]
          message.value = 'Исправьте ошибки в форме'
        } else if (errorData.user_password) {
          errors.password = errorData.user_password[0]
          message.value = 'Исправьте ошибки в форме'
        } else if (errorData.email) {
          errors.email = errorData.email[0]
          message.value = 'Исправьте ошибки в форме'
        } else if (errorData.password) {
          errors.password = errorData.password[0]
          message.value = 'Исправьте ошибки в форме'
        } else {
          message.value = 'Некорректные данные для регистрации'
        }
      } else {
        message.value = 'Произошла ошибка при регистрации' + status

      }
    } else if (error.request) {
      message.value = 'Не удалось подключиться к серверу'
    } else {
      message.value = 'Произошла непредвиденная ошибка'
    }
    
    messageType.value = 'error'
  } finally {
    isSubmitting.value = false
  }
}


const closeForm = () => {
  emit('close')
}

const switchToLogin = () => {
  emit('switch-to-login')
}
</script>

<template>
  <div class="auth-container">
    <div class="header-actions">
      <button @click="closeForm" class="close-button">×</button>
    </div>
    
    <div class="auth-header">
      <h2>Регистрация</h2>
    </div>
    
    <form @submit.prevent="handleSubmit" class="auth-form">
      <div class="input-group">
        <label class="input-label">Фамилия</label>
        <input 
          type="text" 
          v-model="formData.lastname"
          placeholder="Введите фамилию"
          :class="{'error-input': errors.lastname}"
          @blur="validateField('lastname')"
          class="form-input"
        >
        <span v-if="errors.lastname" class="error-message">{{ errors.lastname }}</span>
      </div>
      
      <div class="input-group">
        <label class="input-label">Имя</label>
        <input
          type="text"
          v-model="formData.firstname" 
          placeholder="Введите имя"
          :class="{'error-input': errors.firstname}"
          @blur="validateField('firstname')"
          class="form-input"
        >
        <span v-if="errors.firstname" class="error-message">{{ errors.firstname }}</span>
      </div>

      <div class="input-group">
        <label class="input-label">Электронная почта</label>
        <input 
          type="email" 
          v-model="formData.email"
          placeholder="example@email.com"
          :class="{'error-input': errors.email}"
          @blur="validateField('email')"
          class="form-input"
        >
        <span v-if="errors.email" class="error-message">{{ errors.email }}</span>
      </div>

      <div class="input-group">
        <label class="input-label">Пароль</label>
        <div class="password-input-wrapper">
          <input 
            :type="showPassword ? 'text' : 'password'" 
            v-model="formData.password"
            placeholder="Введите пароль"
            :class="{'error-input': errors.password}"
            @blur="validateField('password')"
            class="form-input password-input"
          >
          <span class="password-toggle" @click="showPassword = !showPassword">
            {{ showPassword ? '🙈' : '🙉' }}
          </span>
        </div>
        <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
      </div>

      <div class="input-group">
        <label class="input-label">Подтверждение пароля</label>
        <div class="password-input-wrapper">
          <input 
            :type="showConfirmPassword ? 'text' : 'password'" 
            v-model="formData.confirmPassword"
            placeholder="Повторите пароль"
            :class="{'error-input': errors.confirmPassword}"
            @blur="validateField('confirmPassword')"
            class="form-input password-input"
          >
          <span class="password-toggle" @click="showConfirmPassword = !showConfirmPassword">
            {{ showConfirmPassword ? '🙈' : '🙉' }}
          </span>
        </div>
        <span v-if="errors.confirmPassword" class="error-message">{{ errors.confirmPassword }}</span>
      </div>

      <button
        type="submit" 
        class="auth-btn"
        :disabled="!isFormValid || isSubmitting"
      >
        <span v-if="!isSubmitting">Зарегистрироваться</span>
        <span v-else>Регистрация...</span>
      </button>
      
      <div class="switch-link">
        Уже есть аккаунт? 
        <a href="#" @click.prevent="switchToLogin" class="switch-link-text">Войти</a>
      </div>
      
      <div v-if="message" :class="['message', messageType]">
        {{ message }}
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
  overflow: hidden;
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