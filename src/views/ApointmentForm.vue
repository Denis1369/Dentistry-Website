<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const emit = defineEmits(['appointment-success', 'close'])

const API_BASE_URL = 'http://127.0.0.1:8000'
const getAuthToken = () => localStorage.getItem('authToken')

const getCurrentUser = () => {
  const userData = localStorage.getItem('userData')
  return userData ? JSON.parse(userData) : null
}

const props = defineProps({
  selectedService: {
    type: Object,
    default: null
  },
  selectedDoctor: {
    type: Object,
    default: null
  }
})

const getUserIdFromToken = () => {
  try {
    const token = localStorage.getItem('authToken')
    if (!token) return null
    const payload = token.split('.')[1]
    const decodedPayload = JSON.parse(atob(payload))
    return decodedPayload.user_id || decodedPayload.sub
  } catch (error) {
    return null
  }
}

const fetchUserProfile = async () => {
  try {
    const token = localStorage.getItem('authToken')
    if (!token) {
      throw new Error('Токен авторизации не найден')
    }

    const response = await fetch('http://127.0.0.1:8000/user/profile/', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    })

    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`)
    }

    const data = await response.json()
    let userData = {}
    
    if (data.user) {
      userData = data.user
      if (!userData.user_id) {
        const userIdFromToken = getUserIdFromToken()
        if (userIdFromToken) {
          userData.user_id = userIdFromToken
        }
      }
    } else {
      userData = data
      if (!userData.user_id) {
        const userIdFromToken = getUserIdFromToken()
        if (userIdFromToken) {
          userData.user_id = userIdFromToken
        }
      }
    }

    localStorage.setItem('userData', JSON.stringify(userData))
    return userData
    
  } catch (err) {
    const storedUserData = localStorage.getItem('userData')
    if (storedUserData) {
      return JSON.parse(storedUserData)
    }
    throw err
  }
}

const appointmentForm = reactive({
  service: '',
  doctor: '',
  date: '',
  time: '',
  lastName: '', 
  firstName: '',
  birthDate: '',
  email: ''
})

const appointmentErrors = reactive({
  service: '',
  doctor: '',
  date: '',
  time: '',
  lastName: '',
  firstName: '',
  birthDate: '',
  email: ''
})

const services = ref([])
const allServices = ref([])
const doctors = ref([])
const allDoctors = ref([])
const professions = ref([])
const availableTimes = ref([])
const isLoading = ref(false)
const currentUser = ref(null)
const isAuthenticated = ref(false)
const profileLoading = ref(false)

const initializeAppointmentForm = async () => {
  try {
    await checkAuthentication()
    
    if (!isAuthenticated.value) {
      return
    }
    
    await Promise.all([
      loadProfessions(),
      loadAllServices(),
      loadAllDoctors()
    ])
    
    if (props.selectedService) {
      const fullService = allServices.value.find(s => s.services_id == props.selectedService.id)
      if (fullService) {
        appointmentForm.service = fullService.services_id.toString()
        if (fullService.services_profession) {
          const profession = professions.value.find(p => p.profession_id == fullService.services_profession)
          if (profession) {
            await loadDoctorsByProfession(profession.profession_title)
          }
        }
      }
    }

    if (props.selectedDoctor) {
      const fullDoctor = allDoctors.value.find(d => d.workers_id == props.selectedDoctor.id)
      if (fullDoctor) {
        appointmentForm.doctor = fullDoctor.workers_id.toString()
        
        if (fullDoctor.workers_profession) {
          const profession = professions.value.find(p => p.profession_id == fullDoctor.workers_profession)
          if (profession) {
            await loadServicesByProfession(profession.profession_title)
          }
        }
      }
    }

    await autoFillUserData()
  } catch (error) {
    console.error('Ошибка инициализации формы:', error)
  }
}

const checkAuthentication = async () => {
  const token = getAuthToken()
  
  if (token) {
    isAuthenticated.value = true
    try {
      profileLoading.value = true
      const userProfile = await fetchUserProfile()
      currentUser.value = userProfile
    } catch (error) {
      const storedUser = getCurrentUser()
      if (storedUser) {
        currentUser.value = storedUser
      } else {
        isAuthenticated.value = false
        currentUser.value = null
      }
    } finally {
      profileLoading.value = false
    }
  } else {
    isAuthenticated.value = false
    currentUser.value = null
  }
}

const autoFillUserData = () => {
  if (!isAuthenticated.value || !currentUser.value) return

  const user = currentUser.value
  appointmentForm.lastName = user.last_name || ''
  appointmentForm.firstName = user.first_name || ''
  appointmentForm.birthDate = user.user_date_birth || ''
  appointmentForm.email = user.email || ''
}

const loadProfessions = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/profession/`)
    if (response.data.profession) {
      professions.value = response.data.profession
    } else if (Array.isArray(response.data)) {
      professions.value = response.data
    }
  } catch (error) {
    professions.value = []
  }
}

const loadAllServices = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/service/get_base/`)
    if (response.data.services) {
      allServices.value = response.data.services
      services.value = response.data.services
    } else if (Array.isArray(response.data)) {
      allServices.value = response.data
      services.value = response.data
    }
  } catch (error) {
    allServices.value = []
    services.value = []
  }
}

const loadAllDoctors = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/workers/get_base_many/`)
    if (response.data.workers) {
      allDoctors.value = response.data.workers
      doctors.value = response.data.workers
    } else if (Array.isArray(response.data)) {
      allDoctors.value = response.data
      doctors.value = response.data
    }
  } catch (error) {
    allDoctors.value = []
    doctors.value = []
  }
}

watch(() => appointmentForm.service, async (newServiceId) => {
  if (!isAuthenticated.value) return
  
  if (newServiceId) {
    const selectedService = allServices.value.find(s => s.services_id == newServiceId)
    if (selectedService && selectedService.services_profession) {
      const profession = professions.value.find(p => p.profession_id == selectedService.services_profession)
      if (profession) {
        await loadDoctorsByProfession(profession.profession_title)
      }
    }
  } else {
    doctors.value = allDoctors.value
  }
  availableTimes.value = []
})

watch(() => appointmentForm.doctor, async (newDoctorId) => {
  if (!isAuthenticated.value) return
  
  if (newDoctorId) {
    const selectedDoctor = allDoctors.value.find(d => d.workers_id == newDoctorId)
    if (selectedDoctor && selectedDoctor.workers_profession) {
      const profession = professions.value.find(p => p.profession_id == selectedDoctor.workers_profession)
      if (profession) {
        await loadServicesByProfession(profession.profession_title)
      }
    }
  } else {
    services.value = allServices.value
  }
  availableTimes.value = []
})

watch([() => appointmentForm.service, () => appointmentForm.doctor], async ([service, doctor], [oldService, oldDoctor]) => {
  if (!isAuthenticated.value) return
  
  if (service && doctor) {
    const selectedService = allServices.value.find(s => s.services_id == service)
    const selectedDoctor = allDoctors.value.find(d => d.workers_id == doctor)
    
    if (selectedService && selectedDoctor) {
      const serviceProfession = selectedService.services_profession
      const doctorProfession = selectedDoctor.workers_profession
      
      if (serviceProfession !== doctorProfession) {
        if (service !== oldService) {
          appointmentForm.doctor = ''
        } else if (doctor !== oldDoctor) {
          appointmentForm.service = ''
        }
      }
    }
  }
})

watch(() => props.selectedService, (newService) => {
  if (!isAuthenticated.value) return
  
  if (newService && newService.id) {
    const fullService = allServices.value.find(s => s.services_id == newService.id)
    if (fullService) {
      appointmentForm.service = fullService.services_id.toString()
      
      if (fullService.services_profession) {
        const profession = professions.value.find(p => p.profession_id == fullService.services_profession)
        if (profession) {
          loadDoctorsByProfession(profession.profession_title)
        }
      }
    }
  }
}, { immediate: true })

watch(() => props.selectedDoctor, (newDoctor) => {
  if (!isAuthenticated.value) return
  
  if (newDoctor && newDoctor.id) {
    appointmentForm.doctor = newDoctor.id.toString()
    
    const selectedDoctorObj = allDoctors.value.find(d => d.workers_id == newDoctor.id)
    if (selectedDoctorObj && selectedDoctorObj.workers_profession) {
      const profession = professions.value.find(p => p.profession_id == selectedDoctorObj.workers_profession)
      if (profession) {
        loadServicesByProfession(profession.profession_title)
      }
    }
  }
}, { immediate: true })

const loadDoctorsByProfession = async (professionTitle) => {
  try {
    isLoading.value = true
    const response = await axios.get(`${API_BASE_URL}/workers/get_filter/`, {
      params: { profession_title: professionTitle }
    })
    if (response.data.workers) {
      doctors.value = response.data.workers
    }
  } catch (error) {
    doctors.value = allDoctors.value
  } finally {
    isLoading.value = false
  }
}

const loadServicesByProfession = async (professionTitle) => {
  try {
    isLoading.value = true
    const response = await axios.get(`${API_BASE_URL}/service/get_filter/`, {
      params: { profession_title: professionTitle }
    })
    if (response.data.services) {
      services.value = response.data.services
    }
  } catch (error) {
    services.value = allServices.value
  } finally {
    isLoading.value = false
  }
}

const getProfessionTitle = (professionId) => {
  const profession = professions.value.find(p => p.profession_id == professionId)
  return profession ? profession.profession_title : 'Неизвестная специальность'
}

const getProfessionTime = (professionId) => {
  const profession = professions.value.find(p => p.profession_id == professionId)
  return profession ? profession.profession_time : 30
}

watch([() => appointmentForm.doctor, () => appointmentForm.date], async ([doctorId, date]) => {
  if (!isAuthenticated.value) return
  
  if (doctorId && date) {
    await loadAvailableTimes(doctorId, date)
  } else {
    availableTimes.value = []
  }
})

const loadAvailableTimes = async (workerId, date) => {
  try {
    isLoading.value = true
    
    const token = getAuthToken()
    const config = {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    }
    
    const response = await axios.get(`${API_BASE_URL}/appointment/get_appointment/`, {
      ...config,
      params: { 
        worker_id: workerId, 
        date: date 
      }
    })
    
    console.log('Ответ от API для доступных слотов:', response.data)
    
    if (response.data && response.data.slots && Array.isArray(response.data.slots)) {
      // Преобразуем даты в формат времени HH:MM и сортируем
      availableTimes.value = response.data.slots.map(slot => {
        try {
          let slotDate;
          if (typeof slot === 'string') {
            slotDate = new Date(slot);
          } else {
            slotDate = slot;
          }
          
          const hours = slotDate.getHours().toString().padStart(2, '0')
          const minutes = slotDate.getMinutes().toString().padStart(2, '0')
          return `${hours}:${minutes}`
        } catch (e) {
          console.warn('Ошибка преобразования слота:', slot, e)
          return null
        }
      })
      .filter(time => time !== null)
      .sort((a, b) => a.localeCompare(b)) // Сортируем по времени
      
      console.log('Доступные времена:', availableTimes.value)
    } else {
      console.warn('Неожиданный формат ответа от сервера:', response.data)
      availableTimes.value = []
    }
    
  } catch (error) {
    console.error('Ошибка загрузки доступных времен:', error)
    if (error.response?.status === 400) {
      console.error('Ошибка валидации:', error.response.data)
    }
    availableTimes.value = []
  } finally {
    isLoading.value = false
  }
}

const createLocalDateTime = (dateStr, timeStr) => {
  const [year, month, day] = dateStr.split('-');
  const [hours, minutes] = timeStr.split(':');

  const localDate = new Date(year, month - 1, day, hours, minutes);
  
  const timezoneOffset = localDate.getTimezoneOffset() * 60000;
  const localISOTime = new Date(localDate - timezoneOffset).toISOString().slice(0, 16);
  
  return localISOTime + ':00Z';
};

const isServiceAndDoctorCompatible = computed(() => {
  if (!appointmentForm.service || !appointmentForm.doctor) return true
  const selectedService = allServices.value.find(s => s.services_id == appointmentForm.service)
  const selectedDoctor = allDoctors.value.find(d => d.workers_id == appointmentForm.doctor)
  if (!selectedService || !selectedDoctor) return true
  return selectedService.services_profession === selectedDoctor.workers_profession
})

const validateField = (fieldName, value) => {
  switch (fieldName) {
    case 'lastName':
      if (!value.trim()) appointmentErrors.lastName = 'Фамилия обязательна для заполнения'
      else if (value.length < 2) appointmentErrors.lastName = 'Фамилия должна содержать минимум 2 символа'
      else if (!/^[a-zA-Zа-яА-ЯёЁ\s\-]+$/.test(value)) appointmentErrors.lastName = 'Фамилия может содержать только буквы, пробелы и дефисы'
      else appointmentErrors.lastName = ''
      break
    case 'firstName':
      if (!value.trim()) appointmentErrors.firstName = 'Имя обязательно для заполнения'
      else if (value.length < 2) appointmentErrors.firstName = 'Имя должно содержать минимум 2 символа'
      else if (!/^[a-zA-Zа-яА-ЯёЁ\s\-]+$/.test(value)) appointmentErrors.firstName = 'Имя может содержать только буквы, пробелы и дефисы'
      else appointmentErrors.firstName = ''
      break
    case 'birthDate':
      if (!value) appointmentErrors.birthDate = 'Дата рождения обязательна для заполнения'
      else {
        const birthDate = new Date(value)
        const today = new Date()
        const minDate = new Date(today.getFullYear() - 90, today.getMonth(), today.getDate())
        const maxDate = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate())
        if (birthDate < minDate) appointmentErrors.birthDate = 'Дата рождения не может быть раньше ' + minDate.toLocaleDateString('ru-RU')
        else if (birthDate > maxDate) appointmentErrors.birthDate = 'Пациент должен быть старше 12 лет'
        else appointmentErrors.birthDate = ''
      }
      break
    case 'email':
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!value.trim()) appointmentErrors.email = 'Email обязателен для заполнения'
      else if (!emailRegex.test(value)) appointmentErrors.email = 'Введите корректный email адрес'
      else appointmentErrors.email = ''
      break
    case 'service':
      if (!value) appointmentErrors.service = 'Выберите услугу'
      else appointmentErrors.service = ''
      break
    case 'date':
      if (!value) appointmentErrors.date = 'Выберите дату'
      else appointmentErrors.date = ''
      break
    case 'time':
      if (!value) appointmentErrors.time = 'Выберите время'
      else appointmentErrors.time = ''
      break
  }
}

const isFormValid = computed(() => {
  return isAuthenticated.value && (
    appointmentForm.lastName &&
    appointmentForm.firstName &&
    appointmentForm.birthDate &&
    appointmentForm.email &&
    appointmentForm.service &&
    appointmentForm.date &&
    appointmentForm.time &&
    !appointmentErrors.lastName &&
    !appointmentErrors.firstName &&
    !appointmentErrors.birthDate &&
    !appointmentErrors.email &&
    !appointmentErrors.service &&
    !appointmentErrors.date &&
    !appointmentErrors.time
  )
})

const handleSubmit = async () => {
  // Проверяем авторизацию
  if (!isAuthenticated.value) {
    alert('Для записи на прием необходимо авторизоваться')
    return
  }
  
  Object.keys(appointmentForm).forEach(field => {
    if (field in appointmentErrors) {
      validateField(field, appointmentForm[field])
    }
  })
  
  if (!isFormValid.value) {
    alert('Пожалуйста, заполните все обязательные поля корректно')
    return
  }
  
  const selectedTime = appointmentForm.time
  if (availableTimes.value && !availableTimes.value.includes(selectedTime)) {
    alert('Выбранное время уже занято. Пожалуйста, выберите другое время.')
    return
  }
  
  try {
    isLoading.value = true
    
    const appointmentDateTime = createLocalDateTime(appointmentForm.date, appointmentForm.time)
    
    const appointmentData = {
      appointment_workers: parseInt(appointmentForm.doctor),
      appointment_services: parseInt(appointmentForm.service),
      appointment_date: appointmentDateTime,
      first_name: appointmentForm.firstName,
      last_name: appointmentForm.lastName,
      birth_date: appointmentForm.birthDate,
      email: appointmentForm.email,
      appointment_status: 'запланирован'
    }
    
    if (isAuthenticated.value && currentUser.value) {
      const userId = currentUser.value.user_id || getUserIdFromToken()
      if (userId) {
        appointmentData.user_id = userId
      }
    }
    
    const token = getAuthToken()
    const config = { 
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      } 
    }
    
    console.log('Отправляемые данные записи:', appointmentData)
    
    const response = await axios.post(`${API_BASE_URL}/appointment/post_appointment/`, appointmentData, config)
    
    await loadAvailableTimes(appointmentForm.doctor, appointmentForm.date)
    
    emit('appointment-success', {
      ...appointmentForm,
      appointmentData: appointmentData
    })
    
    alert('Запись успешно создана!')
    
    Object.keys(appointmentForm).forEach(key => { 
      if (key !== 'lastName' && key !== 'firstName' && key !== 'birthDate' && key !== 'email') {
        appointmentForm[key] = ''
      }
    })
    
  } catch (error) {
    if (error.response?.status === 401) {
      alert('Ошибка авторизации. Пожалуйста, войдите в систему заново.')
    } else if (error.response?.status === 400) {
      if (error.response.data && error.response.data.detail) {
        alert(`Ошибка: ${error.response.data.detail}`)
      } else {
        alert('Ошибка в данных: Проверьте правильность введенных данных')
      }
    } else if (error.response?.status === 409) {
      alert('Это время уже занято. Пожалуйста, выберите другое время.')
    } else {
      alert('Произошла ошибка при создании записи. Пожалуйста, попробуйте еще раз.')
    }
    console.error('Ошибка при создании записи:', error)
  } finally {
    isLoading.value = false
  }
}

const isFieldLocked = (fieldName) => {
  if (!isAuthenticated.value) return false
  
  const user = currentUser.value
  if (!user) return false
  switch (fieldName) {
    case 'lastName':
      return !!user.last_name
    case 'firstName':
      return !!user.first_name
    case 'email':
      return !!user.email
    case 'birthDate':
      return !!user.user_date_birth
    default:
      return false
  }
}

const getFieldTooltip = (fieldName) => {
  if (!isFieldLocked(fieldName)) return ''
  return 'Это поле заполнено из вашего профиля'
}

const closeForm = () => emit('close')

const getMinBirth = () => {
  const minDate = new Date()
  minDate.setFullYear(minDate.getFullYear() - 90)
  return minDate.toISOString().split('T')[0]
}

const getMaxBirth = () => {
  const maxDate = new Date()
  maxDate.setFullYear(maxDate.getFullYear() - 1)
  return maxDate.toISOString().split('T')[0]
}

const getTodayDate = () => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return tomorrow.toISOString().split('T')[0]
}

const getMaxDate = () => {
  const maxDate = new Date()
  maxDate.setMonth(maxDate.getMonth() + 1)
  return maxDate.toISOString().split('T')[0]
}

const refreshUserData = async () => {
  try {
    profileLoading.value = true
    const userProfile = await fetchUserProfile()
    currentUser.value = userProfile
    await autoFillUserData()
  } catch (error) {
    alert('Не удалось обновить данные профиля')
  } finally {
    profileLoading.value = false
  }
}

onMounted(() => {
  initializeAppointmentForm()
})
</script>

<template>
  <div class="appointment-container">
    <div class="header-actions">
      <button @click="closeForm" class="close-button">×</button>
    </div>
    
    <div class="appointment-header">
      <h2>Запись на прием</h2>
      <div class="auth-status">
        <div v-if="profileLoading" class="user-info-badge loading">
          Загрузка данных...
        </div>
        <div v-else-if="isAuthenticated" class="user-info-badge authenticated">
          <div class="user-main">
            {{ currentUser?.first_name || currentUser?.name }} {{ currentUser?.last_name || currentUser?.surname }}
          </div>
          <button @click="refreshUserData" class="refresh-btn" :disabled="profileLoading">
            Обновить
          </button>
        </div>
        <div v-else class="user-info-badge guest">
          Гостевой режим
        </div>
      </div>
    </div>
    
    <form @submit.prevent="handleSubmit" class="appointment-form">
      <div class="form-section">
        <h3 class="section-title">Выбор услуги и врача</h3>
        
        <div class="form-row">
          <div class="input-group">
            <label class="input-label">Услуга *</label>
            <select 
              v-model="appointmentForm.service"
              @blur="validateField('service', appointmentForm.service)"
              :class="{'error-input': appointmentErrors.service}"
              class="form-input"
              :disabled="isLoading"
            >
              <option value="">Выберите услугу</option>
              <option 
                v-for="service in services" 
                :key="service.services_id" 
                :value="service.services_id"
              >
                {{ service.services_title }}
                <span v-if="service.services_price"> - {{ service.services_price }} ₽</span>
              </option>
            </select>
            <span v-if="appointmentErrors.service" class="error-message">
              {{ appointmentErrors.service }}
            </span>
          </div>
          
          <div class="input-group">
            <label class="input-label">Врач *</label>
            <select 
              v-model="appointmentForm.doctor" 
              @blur="validateField('doctor', appointmentForm.doctor)"
              :class="{'error-input': appointmentErrors.doctor}"
              class="form-input"
              :disabled="isLoading"
            >
              <option value="">Выберите врача</option>
              <option 
                v-for="doctor in doctors" 
                :key="doctor.workers_id" 
                :value="doctor.workers_id"
              >
                {{ doctor.workers_last_name }} {{ doctor.workers_name }}
                <span v-if="doctor.workers_profession">
                  - {{ getProfessionTitle(doctor.workers_profession) }}
                </span>
              </option>
            </select>
            <span v-if="appointmentErrors.doctor" class="error-message">
              {{ appointmentErrors.doctor }}
            </span>
          </div>
        </div>

        <div class="selection-info" v-if="appointmentForm.doctor && appointmentForm.service">
          <div class="info-item">
            <strong>Врач:</strong> 
            {{ allDoctors.find(d => d.workers_id == appointmentForm.doctor)?.workers_last_name }} 
            {{ allDoctors.find(d => d.workers_id == appointmentForm.doctor)?.workers_name }}
          </div>
          <div class="info-item">
            <strong>Услуга:</strong> 
            {{ allServices.find(s => s.services_id == appointmentForm.service)?.services_title }}
          </div>
          <div class="info-item">
            <strong>Длительность:</strong> 
            {{ getProfessionTime(allDoctors.find(d => d.workers_id == appointmentForm.doctor)?.workers_profession) }} минут
          </div>
          
          <div v-if="!isServiceAndDoctorCompatible" class="warning-message">
            Выбранный врач не специализируется на этой услуге
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3 class="section-title">Выбор даты и времени</h3>
        <div class="form-row">
          <div class="input-group">
            <label class="input-label">Дата приема *</label>
            <input 
              type="date" 
              v-model="appointmentForm.date"
              :min="getTodayDate()"
              :max="getMaxDate()"
              @blur="validateField('date', appointmentForm.date)"
              :class="{'error-input': appointmentErrors.date}"
              class="form-input"
              :disabled="!appointmentForm.doctor || isLoading"
            >
            <span v-if="appointmentErrors.date" class="error-message">
              {{ appointmentErrors.date }}
            </span>
          </div>
          
          <div class="input-group">
            <label class="input-label">Время приема *</label>
            <select 
              v-model="appointmentForm.time"
              @blur="validateField('time', appointmentForm.time)"
              :class="{'error-input': appointmentErrors.time}"
              class="form-input"
              :disabled="!appointmentForm.date || isLoading || availableTimes.length === 0"
            >
              <option value="">Выберите время</option>
              <option v-for="time in availableTimes" :key="time" :value="time">
                {{ time }}
              </option>
            </select>
            <span v-if="appointmentErrors.time" class="error-message">
              {{ appointmentErrors.time }}
            </span>
            <div v-if="isLoading && appointmentForm.date && appointmentForm.doctor" class="loading-text">
              Загрузка доступного времени...
            </div>
            <div v-if="!isLoading && appointmentForm.date && appointmentForm.doctor && availableTimes.length === 0" class="no-slots-text">
              Нет доступных слотов для записи на выбранную дату
            </div>
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3 class="section-title">Личные данные</h3>
        
        <div class="form-row">
          <div class="input-group">
            <label class="input-label">Фамилия *</label>
            <input 
              type="text" 
              v-model="appointmentForm.lastName"
              placeholder="Введите фамилию"
              @blur="validateField('lastName', appointmentForm.lastName)"
              :class="{'error-input': appointmentErrors.lastName, 'locked-field': isFieldLocked('lastName')}"
              class="form-input"
              :disabled="isFieldLocked('lastName')"
              :title="getFieldTooltip('lastName')"
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
              :class="{'error-input': appointmentErrors.firstName, 'locked-field': isFieldLocked('firstName')}"
              class="form-input"
              :disabled="isFieldLocked('firstName')"
              :title="getFieldTooltip('firstName')"
            >
            <span v-if="appointmentErrors.firstName" class="error-message">
              {{ appointmentErrors.firstName }}
            </span>
          </div>
        </div>

        <div class="form-row">
          <div class="input-group">
            <label class="input-label">Дата рождения *</label>
            <input 
              type="date" 
              v-model="appointmentForm.birthDate"
              :min="getMinBirth()"
              :max="getMaxBirth()"
              @blur="validateField('birthDate', appointmentForm.birthDate)"
              :class="{'error-input': appointmentErrors.birthDate, 'locked-field': isFieldLocked('birthDate')}"
              class="form-input"
              :disabled="isFieldLocked('birthDate')"
              :title="getFieldTooltip('birthDate')"
            >
            <span v-if="appointmentErrors.birthDate" class="error-message">
              {{ appointmentErrors.birthDate }}
            </span>
          </div>
          
          <div class="input-group">
            <label class="input-label">Email *</label>
            <input 
              type="email" 
              v-model="appointmentForm.email"
              placeholder="example@email.com"
              @blur="validateField('email', appointmentForm.email)"
              :class="{'error-input': appointmentErrors.email, 'locked-field': isFieldLocked('email')}"
              class="form-input"
              :disabled="isFieldLocked('email')"
              :title="getFieldTooltip('email')"
            >
            <span v-if="appointmentErrors.email" class="error-message">
              {{ appointmentErrors.email }}
            </span>
          </div>
        </div>
      </div>
      
      <button 
        type="submit" 
        class="appointment-btn"
        :disabled="!isFormValid || isLoading"
      >
        <span v-if="isLoading">Отправка...</span>
        <span v-else>Записаться на прием</span>
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
  padding: 40px 40px 20px 40px;
  border-bottom: 1px solid #f1f3f4;
  background: white;
}

.appointment-header h2 {
  text-align: center;
  margin: 0 0 15px 0;
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
}

.auth-status {
  display: flex;
  justify-content: center;
}

.user-info-badge {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

.user-info-badge.authenticated {
  background: #e3f2fd;
  color: #1976d2;
}

.user-info-badge.guest {
  background: #fff3cd;
  color: #856404;
}

.user-info-badge.loading {
  background: #f8f9fa;
  color: #6c757d;
}

.refresh-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  background: #1976d2;
  color: white;
}

.refresh-btn:hover:not(:disabled) {
  background: #1565c0;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.appointment-form {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 30px 40px 40px 40px;
  gap: 25px;
  overflow-y: auto;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #4a5568;
  margin: 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #f1f3f4;
}

.auth-notice {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  color: #856404;
  margin-bottom: 10px;
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

.form-input:disabled {
  background-color: #f7fafc;
  color: #2d3748;
  cursor: not-allowed;
  opacity: 0.8;
}

.locked-field {
  background-color: #f8f9fa !important;
  border-color: #e9ecef !important;
  color: #495057 !important;
}

.error-input {
  border-color: #e53e3e;
}

.error-message {
  color: #e53e3e;
  font-size: 12px;
  margin-top: 4px;
}

.appointment-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.appointment-btn:hover:not(:disabled) {
  background: #5a6fd8;
  transform: translateY(-1px);
}

.appointment-btn:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  transform: none;
}

.form-note {
  text-align: center;
  color: #718096;
  font-size: 14px;
  margin-top: 10px;
}

.selection-info {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.info-item {
  margin-bottom: 8px;
  font-size: 14px;
}

.status-planned {
  color: #667eea;
  font-weight: 600;
  background: #e3f2fd;
  padding: 2px 8px;
  border-radius: 4px;
  margin-left: 5px;
}

.warning-message {
  color: #e53e3e;
  margin-top: 10px;
  font-size: 14px;
}

.loading-text {
  color: #667eea;
  font-size: 12px;
  margin-top: 4px;
}

.no-slots-text {
  color: #e53e3e;
  font-size: 12px;
  margin-top: 4px;
  font-style: italic;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .appointment-header {
    padding: 20px;
  }
  
  .appointment-form {
    padding: 20px;
  }
}
</style>