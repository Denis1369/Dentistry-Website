<script setup>
import { ref, reactive, computed } from 'vue'

const emit = defineEmits(['appointment-success', 'close'])

const appointmentForm = reactive({
  service: '',
  doctor: '',
  date: '',
  time: '',
  lastName: '', 
  firstName: '',
  middleName: '',
  phone: '',
  email: '',
  comment: ''
})

const appointmentErrors = reactive({
  service: '',
  doctor: '',
  date: '',
  time: '',
  lastName: '',
  firstName: '',
  middleName: '', 
  phone: '',
  email: ''
})

const services = ref([])
const doctors = ref([])
const availableTimes = ref([])

const validateField = (fieldName, value) => {
  switch (fieldName) {
    case 'lastName':
      if (!value.trim()) {
        appointmentErrors.lastName = 'Фамилия обязательна для заполнения'
      } else if (value.length < 2) {
        appointmentErrors.lastName = 'Фамилия должна содержать минимум 2 символа'
      } else if (!/^[a-zA-Zа-яА-ЯёЁ\s\-]+$/.test(value)) {
        appointmentErrors.lastName = 'Фамилия может содержать только буквы, пробелы и дефисы'
      } else {
        appointmentErrors.lastName = ''
      }
      break
      
    case 'firstName':
      if (!value.trim()) {
        appointmentErrors.firstName = 'Имя обязательно для заполнения'
      } else if (value.length < 2) {
        appointmentErrors.firstName = 'Имя должно содержать минимум 2 символа'
      } else if (!/^[a-zA-Zа-яА-ЯёЁ\s\-]+$/.test(value)) {
        appointmentErrors.firstName = 'Имя может содержать только буквы, пробелы и дефисы'
      } else {
        appointmentErrors.firstName = ''
      }
      break
      
    case 'middleName':
      if (value.trim() && !/^[a-zA-Zа-яА-ЯёЁ\s\-]+$/.test(value)) {
        appointmentErrors.middleName = 'Отчество может содержать только буквы, пробелы и дефисы'
      } else {
        appointmentErrors.middleName = ''
      }
      break
      
    case 'phone':
      const phoneRegex = /^[\+]?[7-8]?[0-9\s\-\(\)]{10,15}$/
      if (!value.trim()) {
        appointmentErrors.phone = 'Телефон обязателен для заполнения'
      } else if (!phoneRegex.test(value.replace(/\s/g, ''))) {
        appointmentErrors.phone = 'Введите корректный номер телефона'
      } else {
        appointmentErrors.phone = ''
      }
      break
      
    case 'email':
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!value.trim()) {
        appointmentErrors.email = 'Email обязателен для заполнения'
      } else if (!emailRegex.test(value)) {
        appointmentErrors.email = 'Введите корректный email адрес'
      } else {
        appointmentErrors.email = ''
      }
      break
      
    case 'service':
      if (!value) {
        appointmentErrors.service = 'Выберите услугу'
      } else {
        appointmentErrors.service = ''
      }
      break
      
    case 'date':
      if (!value) {
        appointmentErrors.date = 'Выберите дату'
      } else {
        appointmentErrors.date = ''
      }
      break
      
    case 'time':
      if (!value) {
        appointmentErrors.time = 'Выберите время'
      } else {
        appointmentErrors.time = ''
      }
      break
  }
}

const isFormValid = computed(() => {
  return (
    appointmentForm.lastName &&
    appointmentForm.firstName &&
    appointmentForm.phone &&
    appointmentForm.email &&
    appointmentForm.service &&
    appointmentForm.date &&
    appointmentForm.time &&
    !appointmentErrors.lastName &&
    !appointmentErrors.firstName &&
    !appointmentErrors.middleName &&
    !appointmentErrors.phone &&
    !appointmentErrors.email &&
    !appointmentErrors.service &&
    !appointmentErrors.date &&
    !appointmentErrors.time
  )
})

const handleSubmit = async () => {
  validateField('lastName', appointmentForm.lastName)
  validateField('firstName', appointmentForm.firstName)
  validateField('middleName', appointmentForm.middleName)
  validateField('phone', appointmentForm.phone)
  validateField('email', appointmentForm.email)
  validateField('service', appointmentForm.service)
  validateField('date', appointmentForm.date)
  validateField('time', appointmentForm.time)
  
  if (!isFormValid.value) {
    return
  }
  
  console.log('Данные записи:', appointmentForm)
  
  setTimeout(() => {
    emit('appointment-success', appointmentForm)
    alert('Запись успешно отправлена! Мы свяжемся с вами для подтверждения.')
  }, 1000)
}

const closeForm = () => {
  emit('close')
}

const getTodayDate = () => {
  const today = new Date()
  return today.toISOString().split('T')[0]
}

const getMaxDate = () => {
  const maxDate = new Date()
  maxDate.setMonth(maxDate.getMonth() + 3)
  return maxDate.toISOString().split('T')[0]
}
</script>

<template>
  <div class="appointment-container">
    <div class="header-actions">
      <button @click="closeForm" class="close-button">×</button>
    </div>
    
    <div class="appointment-header">
      <h2>Запись на прием</h2>
    </div>
    
    <form @submit.prevent="handleSubmit" class="appointment-form">
      <div class="form-row">
        <div class="input-group">
          <label class="input-label">Услуга *</label>
          <select 
            v-model="appointmentForm.service"
            @blur="validateField('service', appointmentForm.service)"
            :class="{'error-input': appointmentErrors.service}"
            class="form-input"
          >
            <option value="">Выберите услугу</option>
            <option v-for="service in services" :key="service" :value="service">
              {{ service }}
            </option>
          </select>
          <span v-if="appointmentErrors.service" class="error-message">
            {{ appointmentErrors.service }}
          </span>
        </div>
        
        <div class="input-group">
          <label class="input-label">Врач</label>
          <select 
            v-model="appointmentForm.doctor" 
            class="form-input"
          >
            <option value="">Любой доступный врач</option>
            <option v-for="doctor in doctors" :key="doctor" :value="doctor">
              {{ doctor }}
            </option>
          </select>
        </div>
      </div>
      
      <div class="form-row">
        <div class="input-group">
          <label class="input-label">Дата *</label>
          <input 
            type="date" 
            v-model="appointmentForm.date"
            :min="getTodayDate()"
            :max="getMaxDate()"
            @blur="validateField('date', appointmentForm.date)"
            :class="{'error-input': appointmentErrors.date}"
            class="form-input"
          >
          <span v-if="appointmentErrors.date" class="error-message">
            {{ appointmentErrors.date }}
          </span>
        </div>
        
        <div class="input-group">
          <label class="input-label">Время *</label>
          <select 
            v-model="appointmentForm.time"
            @blur="validateField('time', appointmentForm.time)"
            :class="{'error-input': appointmentErrors.time}"
            class="form-input"
          >
            <option value="">Выберите время</option>
            <option v-for="time in availableTimes" :key="time" :value="time">
              {{ time }}
            </option>
          </select>
          <span v-if="appointmentErrors.time" class="error-message">
            {{ appointmentErrors.time }}
          </span>
        </div>
      </div>
      
      <div class="form-row">
        <div class="input-group">
          <label class="input-label">Фамилия *</label>
          <input 
            type="text" 
            v-model="appointmentForm.lastName"
            placeholder="Введите фамилию"
            @blur="validateField('lastName', appointmentForm.lastName)"
            :class="{'error-input': appointmentErrors.lastName}"
            class="form-input"
          >
          <span v-if="appointmentErrors.lastName" class="error-message">
            {{ appointmentErrors.lastName }}
          </span>
        </div>
        
        <div class="input-group">
          <label class="input-label">Имя *</label>
          <input 
            type="text" 
            v-model="appointmentForm.firstName"
            placeholder="Введите имя"
            @blur="validateField('firstName', appointmentForm.firstName)"
            :class="{'error-input': appointmentErrors.firstName}"
            class="form-input"
          >
          <span v-if="appointmentErrors.firstName" class="error-message">
            {{ appointmentErrors.firstName }}
          </span>
        </div>
      </div>
      
      <div class="form-row">
        <div class="input-group">
          <label class="input-label">Отчество</label>
          <input 
            type="text" 
            v-model="appointmentForm.middleName"
            placeholder="Введите отчество (необязательно)"
            @blur="validateField('middleName', appointmentForm.middleName)"
            :class="{'error-input': appointmentErrors.middleName}"
            class="form-input"
          >
          <span v-if="appointmentErrors.middleName" class="error-message">
            {{ appointmentErrors.middleName }}
          </span>
        </div>
        
        <div class="input-group">
          <label class="input-label">Телефон *</label>
          <input 
            type="tel" 
            v-model="appointmentForm.phone"
            placeholder="+7 (XXX) XXX-XX-XX"
            @blur="validateField('phone', appointmentForm.phone)"
            :class="{'error-input': appointmentErrors.phone}"
            class="form-input"
          >
          <span v-if="appointmentErrors.phone" class="error-message">
            {{ appointmentErrors.phone }}
          </span>
        </div>
      </div>
      
      <div class="input-group">
        <label class="input-label">Email *</label>
        <input 
          type="email" 
          v-model="appointmentForm.email"
          placeholder="example@email.com"
          @blur="validateField('email', appointmentForm.email)"
          :class="{'error-input': appointmentErrors.email}"
          class="form-input"
        >
        <span v-if="appointmentErrors.email" class="error-message">
          {{ appointmentErrors.email }}
        </span>
      </div>
      
      <button 
        type="submit" 
        class="appointment-btn"
        :disabled="!isFormValid"
      >
        Записаться на прием
      </button>
      
      <div class="form-note">
        * Поля, обязательные для заполнения
      </div>
    </form>
  </div>
</template>

<style scoped>
.appointment-container {
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

.appointment-header {
  padding: 40px 40px 30px 40px;
  border-bottom: 1px solid #f1f3f4;
  background: white;
}

.appointment-header h2 {
  text-align: center;
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
}

.appointment-form {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 30px 40px 40px 40px;
  gap: 20px;
  overflow-y: auto;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
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
  font-family: inherit;
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

.appointment-btn {
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

.appointment-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.appointment-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.form-note {
  text-align: center;
  font-size: 12px;
  color: #718096;
  margin-top: 10px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .appointment-header {
    padding: 30px 20px 20px 20px;
  }
  
  .appointment-form {
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
  
  .appointment-header h2 {
    font-size: 24px;
  }
}
</style>