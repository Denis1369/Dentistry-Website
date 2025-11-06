<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const emit = defineEmits(['verification-success', 'switch-to-login', 'close', 'switch-to-registration'])

const props = defineProps({
  email: {
    type: String,
    required: true
  }
})

const verificationCode = ref(['', '', '', '', '', ''])
const isSubmitting = ref(false)
const message = ref('')
const messageType = ref('')
const timer = ref(60)
const canResend = ref(false)

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8000/user/',
  timeout: 10000,
  headers: {'Content-Type': 'application/json'}
})

const inputs = ref([])

onMounted(() => {
  startTimer()
  if (inputs.value[0]) {
    inputs.value[0].focus()
  }
})

const startTimer = () => {
  timer.value = 60
  canResend.value = false
  const interval = setInterval(() => {
    timer.value--
    if (timer.value <= 0) {
      clearInterval(interval)
      canResend.value = true
    }
  }, 1000)
}

const handleInput = (index, event) => {
  const value = event.target.value
  
  if (!/^\d*$/.test(value)) {
    verificationCode.value[index] = ''
    return
  }
  
  verificationCode.value[index] = value.charAt(value.length - 1)
  
  if (value && index < 5) {
    inputs.value[index + 1].focus()
  }
  
  if (verificationCode.value.every(code => code !== '') && index === 5) {
    handleVerification()
  }
}

const handleKeyDown = (index, event) => {
  if (event.key === 'Backspace') {
    if (!verificationCode.value[index] && index > 0) {
      inputs.value[index - 1].focus()
    } else {
      verificationCode.value[index] = ''
    }
  }
  
  if (event.key === 'ArrowLeft' && index > 0) {
    inputs.value[index - 1].focus()
  }
  if (event.key === 'ArrowRight' && index < 5) {
    inputs.value[index + 1].focus()
  }
}

const handlePaste = (event) => {
  event.preventDefault()
  const pasteData = event.clipboardData.getData('text')
  const numbers = pasteData.replace(/\D/g, '').split('').slice(0, 6)
  
  numbers.forEach((num, index) => {
    if (index < 6) {
      verificationCode.value[index] = num
    }
  })
  
  const lastFilledIndex = numbers.length - 1
  if (lastFilledIndex < 5) {
    inputs.value[lastFilledIndex + 1].focus()
  } else if (numbers.length === 6) {
    handleVerification()
  }
}

const handleVerification = async () => {
  const code = verificationCode.value.join('')
  
  if (code.length !== 6) {
    message.value = 'Введите полный код из 6 цифр'
    messageType.value = 'error'
    return
  }
  
  isSubmitting.value = true
  message.value = ''
  
  try {
    console.log('Отправка данных верификации:', {
      email: props.email,
      code: code
    })

    const response = await instance.post('/register_last_step/', {
      email: props.email,
      code: code
    })
    if (response.status === 200 || response.status === 201) {
      message.value = 'Регистрация успешно завершена!'
      messageType.value = 'success'
      
      setTimeout(() => {
        emit('verification-success', props.email)
      }, 1500)
    } else {
      setTimeout(() => {
        emit('verification-success', props.email)
      }, 1500)
    }

  } catch (error) {
    console.error('Полная ошибка при верификации:', error)
    if (messageType.value === 'error') {
      verificationCode.value = ['', '', '', '', '', '']
      if (inputs.value[0]) {
        inputs.value[0].focus()
      }
    }
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

const switchToRegistration = () => {
  emit('switch-to-registration')
}
</script>

<template>
  <div class="auth-container">
    <div class="header-actions">
      <button @click="closeForm" class="close-button">×</button>
    </div>
    
    <div class="auth-header">
      <h2>Подтверждение email</h2>
      <p class="verification-subtitle">
        Код отправлен на <strong>{{ email }}</strong>
      </p>
    </div>
    
    <form @submit.prevent="handleVerification" class="auth-form">
      <div class="input-group">
        <label class="input-label">Введите 6-значный код</label>
        <div class="code-inputs">
          <input
            v-for="(digit, index) in 6"
            :key="index"
            :ref="el => inputs[index] = el"
            v-model="verificationCode[index]"
            type="text"
            maxlength="1"
            :class="['code-input', { 'filled': verificationCode[index] }]"
            @input="handleInput(index, $event)"
            @keydown="handleKeyDown(index, $event)"
            @paste="handlePaste"
            :disabled="isSubmitting"
          >
        </div>
      </div>

      <button
        type="submit" 
        class="auth-btn"
        :disabled="verificationCode.some(code => !code) || isSubmitting"
      >
        <span v-if="!isSubmitting">Подтвердить</span>
        <span v-else>Проверка...</span>
      </button>
      
      
      
      <div class="switch-links">
        <a href="#" @click.prevent="switchToRegistration" class="switch-link-text">Вернуться к регистрации</a>
        <span>|</span>
        <a href="#" @click.prevent="switchToLogin" class="switch-link-text">Войти в аккаунт</a>
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
  padding: 40px 40px 20px 40px;
  border-bottom: 1px solid #f1f3f4;
  background: white;
  text-align: center;
}

.auth-header h2 {
  margin: 0 0 10px 0;
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
}

.verification-subtitle {
  margin: 0;
  color: #718096;
  font-size: 14px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 30px 40px 40px 40px;
  gap: 25px;
  overflow-y: auto;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  color: #4a5568;
  text-align: center;
}

.code-inputs {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.code-input {
  width: 50px;
  height: 60px;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  text-align: center;
  font-size: 24px;
  font-weight: 600;
  transition: all 0.3s ease;
  background: white;
  color: #2d3748;
}

.code-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.code-input.filled {
  border-color: #667eea;
  background-color: #f7faff;
}

.code-input:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
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

.resend-section {
  text-align: center;
  margin-top: 10px;
}

.resend-section p {
  margin: 0 0 10px 0;
  color: #718096;
  font-size: 14px;
}

.resend-btn {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  text-decoration: underline;
  transition: color 0.3s ease;
}

.resend-btn:hover:not(:disabled) {
  color: #5a67d8;
}

.resend-btn:disabled {
  color: #cbd5e0;
  cursor: not-allowed;
  text-decoration: none;
}

.switch-links {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
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
  font-size: 13px;
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

.auth-form::-webkit-scrollbar {
  width: 0px;
}

@media (max-width: 480px) {
  .auth-header {
    padding: 30px 20px 15px 20px;
  }
  
  .auth-form {
    padding: 20px 20px 30px 20px;
  }

  .code-inputs {
    gap: 8px;
  }
  
  .code-input {
    width: 45px;
    height: 55px;
    font-size: 20px;
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
  
  .switch-links {
    flex-direction: column;
    gap: 10px;
  }
}
</style>