<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const emit = defineEmits(['close'])

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

const token = localStorage.getItem('authToken')
if (token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

const activeTab = ref('appointments')
const loading = ref(false)
const doctorData = ref({
  first_name: '',
  last_name: '',
  user_img: '',
  workers_experience: 0,
  workers_description: '',
  workers_profession_id: null,
  workers_id: null,
  user_id: null
})
const selectedDate = ref(new Date().toISOString().split('T')[0])
const appointments = ref([])
const medicalCards = ref([])
const patients = ref([])
const doctorServices = ref([])
const professions = ref([])
const showCreateMedicalCard = ref(false)
const patientSearch = ref('')
const currentWeekStart = ref(new Date())
const currentAppointmentForMedicalCard = ref(null)

const newMedicalCard = ref({
  medical_card_user_id: null,
  medical_card_services_id: null,
  medical_card_diagnosis: '',
  medical_card_purpose: '',
})

onMounted(() => {
  loadDoctorData()
  loadProfessions()
})

const loadDoctorData = async () => {
  try {
    const token = localStorage.getItem('authToken')
    if (!token) {
      throw new Error('Токен не найден')
    }

    const payload = token.split('.')[1]
    const decodedPayload = JSON.parse(atob(payload))
    const userId = decodedPayload.user_id || decodedPayload.sub

    const response = await api.get('/workers/get_base_many/')
    const allWorkers = response.data.workers || []
    const workerData = allWorkers.find(worker => worker.user_id == userId)

    if (workerData) {
      const userData = JSON.parse(localStorage.getItem('userData') || '{}')
      doctorData.value = {
        ...userData,
        ...workerData
      }
      
      await loadDoctorServices()
      await loadAppointments()
      await loadMedicalCards()
      await loadPatients()
    } else {
      alert('Вы не зарегистрированы как врач')
      closeForm()
    }
  } catch (error) {
    closeForm()
  }
}

const loadDoctorServices = async () => {
  try {
    const profession = professions.value.find(p => p.profession_id === doctorData.value.workers_profession)
    
    if (profession && profession.profession_title) {
      const response = await api.get('service/get_filter/',{
        params: {
          profession_title: profession.profession_title
        }
      })
      doctorServices.value = response.data.services || []
    } else {
      const response = await api.get('/service/get_base/')
      doctorServices.value = response.data.services || []
    }
  } catch (error) {
    const response = await api.get('/service/get_base/')
    doctorServices.value = response.data.services || []
  }
}

const loadAppointments = async () => {
  loading.value = true
  try {
    const response = await api.get('/appointment/get_appointment_workers/',{
        params: {
          appointment_workers_id: doctorData.value.workers_id
        }
      })
    appointments.value = response.data.appointment || []
  } catch (error) {
    appointments.value = []
  } finally {
    loading.value = false
  }
}

const loadMedicalCards = async () => {
  loading.value = true
  try {
    const uniquePatientIds = [...new Set(appointments.value.map(apt => apt.appointment_user))]
    
    if (uniquePatientIds.length === 0) {
      medicalCards.value = []
      return
    }

    const allMedicalCards = []
    
    for (const patientId of uniquePatientIds) {
      try {
        const response = await api.get('/medical_card_set/get_medicalCard/', {
          params: { user_id: patientId }
        })
        
        if (response.data.medicalCard && response.data.medicalCard.length > 0) {
          const doctorCards = response.data.medicalCard
          allMedicalCards.push(...doctorCards)
        }
      } catch (error) {
        console.error(`Ошибка загрузки мед карт для пациента ${patientId}:`, error)
      }
    }
    
    medicalCards.value = allMedicalCards
  } catch (error) {
    medicalCards.value = []
  } finally {
    loading.value = false
  }
}

const loadProfessions = async () => {
  try {
    const response = await api.get('/profession/')
    professions.value = response.data.profession || []
  } catch (error) {
    professions.value = []
  }
}

const loadPatients = async () => {
  try {
    const uniquePatientIds = [...new Set(appointments.value.map(apt => apt.appointment_user))]
    
    if (uniquePatientIds.length === 0) {
      patients.value = []
      return
    }

    const realPatients = []
    
    for (const userId of uniquePatientIds) {
      try {
        const response = await api.get('/user/profile_by_id/', {
          params: { user_id: userId }
        })
        
        if (response.data.user) {
          realPatients.push(response.data.user)
        }
      } catch (error) {
        console.error(`Ошибка загрузки пользователя ${userId}:`, error)
      }
    }
    
    patients.value = realPatients
  } catch (error) {
    console.error('Ошибка загрузки пациентов:', error)
  }
}

const loadSchedule = async () => {
  loading.value = true
  try {
    await loadAppointments()
  } catch (error) {
    console.error('Ошибка загрузки расписания:', error)
  } finally {
    loading.value = false
  }
}


const doctorSpecialization = computed(() => {
  const profession = professions.value.find(p => p.profession_id ===doctorData.value.workers_profession)
  return profession ? profession.profession_title : 'Специализация не указана'
})

const isMedicalCardFormValid = computed(() => {
  return newMedicalCard.value.medical_card_user_id && 
         newMedicalCard.value.medical_card_services_id &&
         newMedicalCard.value.medical_card_diagnosis.trim() &&
         newMedicalCard.value.medical_card_purpose.trim() &&
         newMedicalCard.value.medical_card_diagnosis.length <= 75
})

const scheduleDays = computed(() => {
  const days = []
  const startDate = new Date(currentWeekStart.value)
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(startDate)
    date.setDate(startDate.getDate() + i)
    const dateStr = date.toISOString().split('T')[0]
    
    const dayAppointments = appointments.value.filter(apt => {
      const aptDate = new Date(apt.appointment_date).toISOString().split('T')[0]
      return aptDate == dateStr && apt.appointment_status == 'запланирован'
    })
    
    days.push({
      name: date.toLocaleDateString('ru-RU', { weekday: 'long' }),
      date: date.toLocaleDateString('ru-RU'),
      dateObj: date,
      appointments: dayAppointments
    })
  }
  
  return days
})

const currentWeekRange = computed(() => {
  const start = new Date(currentWeekStart.value)
  const end = new Date(start)
  end.setDate(start.getDate() + 6)
  return `${start.toLocaleDateString('ru-RU')} - ${end.toLocaleDateString('ru-RU')}`
})

const showTodayAppointments = () => {
  activeTab.value = 'appointments'
  selectedDate.value = new Date().toISOString().split('T')[0]
  loadAppointments()
}

const showPatientCards = () => {
  activeTab.value = 'medicalCards'
  loadMedicalCards()
}

const showSchedule = () => {
  activeTab.value = 'schedule'
  loadSchedule()
}

const canCompleteAppointment = (appointmentDate) => {
  try {
    const appointmentTime = new Date(appointmentDate)
    const correctedAppointmentTime = new Date(appointmentTime.getTime() - (5 * 60 * 60 * 1000))
    
    const now = new Date()
    
    const timeDiff = now.getTime() - correctedAppointmentTime.getTime()
    const minutesDiff = timeDiff / (1000 * 60)
    
    console.log('Время приема (корректное):', correctedAppointmentTime.toLocaleString('ru-RU'))
    console.log('Текущее время:', now.toLocaleString('ru-RU'))
    console.log('Разница:', minutesDiff.toFixed(1), 'минут')
    
    return minutesDiff >= 0 && minutesDiff <= 30
    
  } catch (error) {
    console.error('Ошибка:', error)
    return false
  }
}

const updateAppointmentStatus = async (appointment, newStatus) => {
  try {
    if (newStatus === 'завершен') {
      if (!canCompleteAppointment(appointment.appointment_date)) {
        return
      }
      const response = await api.put('/appointment/change_appointment_status/', {
        appointment_status: 'завершен'
      }, {
        params: {
          appointment_id: appointment.appointment_id
        }
      })
      
      if (response.status === 200) {
        appointment.appointment_status = 'завершен'
        openMedicalCardFromAppointment(appointment)
      }
    } else if (newStatus === 'отменен') {
      const response = await api.put('/appointment/change_appointment_status/', {
        appointment_status: 'отменен'
      }, {
        params: {
          appointment_id: appointment.appointment_id
        }
      })
      
      if (response.status === 200) {
        appointment.appointment_status = 'отменен'
      }
    }
  } catch (error) {
    console.error('Ошибка обновления статуса приема:', error)
  }
}

const openMedicalCardFromAppointment = (appointment) => {
  currentAppointmentForMedicalCard.value = appointment
  newMedicalCard.value = {
    medical_card_user_id: appointment.appointment_user,
    medical_card_services_id: appointment.appointment_services,
    medical_card_diagnosis: '',
    medical_card_purpose: '',
  }
  showCreateMedicalCard.value = true
}

const openMedicalCard = (userId) => {
  activeTab.value = 'medicalCards'
  loadMedicalCards()
  setTimeout(() => {
    const patient = patients.value.find(p => p.user_id === userId)
    if (patient) {
      patientSearch.value = `${patient.first_name} ${patient.last_name}`
    }
  }, 100)
}

const closeMedicalCardModal = () => {
  showCreateMedicalCard.value = false
  newMedicalCard.value = {
    medical_card_user_id: null,
    medical_card_services_id: null,
    medical_card_diagnosis: '',
    medical_card_purpose: '',
  }
}

const saveMedicalCard = async () => {
  try {
    if (newMedicalCard.value.medical_card_diagnosis.length > 75) {
      alert('Диагноз не может превышать 75 символов')
      return
    }

    if (!newMedicalCard.value.medical_card_diagnosis.trim()) {
      alert('Диагноз не может быть пустым')
      return
    }

    if (!newMedicalCard.value.medical_card_purpose.trim()) {
      alert('Назначение не может быть пустым')
      return
    }
    
    const response = await api.post('/medical_card_set/post_medicalCard/',  {
        medical_card_date: new Date().toISOString(),
        medical_card_status: "закрыта",
        medical_card_diagnosis: newMedicalCard.value.medical_card_diagnosis,
        medical_card_purpose: newMedicalCard.value.medical_card_purpose,
        medical_card_user: newMedicalCard.value.medical_card_user_id,
        medical_card_services: newMedicalCard.value.medical_card_services_id,
        medical_card_workers: doctorData.value.workers_id
    })
    
    if (response.status === 201) {
      if (currentAppointmentForMedicalCard.value) {
        await updateAppointmentStatus(currentAppointmentForMedicalCard.value, 'завершен')
      }
      
      closeMedicalCardModal()
      await loadMedicalCards()
      await loadAppointments()
      
      alert('Медицинская карта успешно создана' + (currentAppointmentForMedicalCard.value ? ' и прием завершен' : ''))
    }
    
  } catch (error) {
    console.error('Ошибка сохранения медицинской карты:', error)
    alert('Ошибка при сохранении медицинской карты')
  }
}

const previousWeek = () => {
  const newDate = new Date(currentWeekStart.value)
  newDate.setDate(newDate.getDate() - 7)
  currentWeekStart.value = newDate
}

const nextWeek = () => {
  const newDate = new Date(currentWeekStart.value)
  newDate.setDate(newDate.getDate() + 7)
  currentWeekStart.value = newDate
}

const getPatientName = (userId) => {
  const patient = patients.value.find(p => p.user_id === userId)
  return patient ? `${patient.first_name} ${patient.last_name}` : 'Пациент не найден'
}

const filteredMedicalCards = computed(() => {
  if (!patientSearch.value) return medicalCards.value
  
  return medicalCards.value.filter(card => {
    const patientName = getPatientName(card.medical_card_user).toLowerCase()
    return patientName.includes(patientSearch.value.toLowerCase())
  })
})

const getServiceName = (serviceId) => {
  const service = doctorServices.value.find(s => s.services_id === serviceId)
  return service ? service.services_title : `Услуга #${serviceId}`
}

const formatDateTime = (dateString) => {
  if (!dateString) return 'Дата не указана'
  
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return dateString
    
    return date.toLocaleString('ru-RU', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: 'UTC' 
    })
  } catch {
    return dateString
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'Дата не указана'
  
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return dateString
    
    return date.toLocaleDateString('ru-RU', {
      timeZone: 'UTC'
    })
  } catch {
    return dateString
  }
}

const formatTime = (dateString) => {
  if (!dateString) return 'Время не указано'
  
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return dateString
    
    return date.toLocaleTimeString('ru-RU', { 
      timeZone: 'UTC',
      hour: '2-digit', 
      minute: '2-digit' 
    })
  } catch {
    return dateString
  }
}

const getAppointmentStatusClass = (status) => {
  const statusClasses = {
    'запланирован': 'status-pending',
    'завершен': 'status-completed',
    'отменен': 'status-cancelled'
  }
  return statusClasses[status] || 'status-pending'
}

const getAppointmentStatusText = (status) => {
  const statusTexts = {
    'запланирован': 'Запланирован',
    'завершен': 'Завершен',
    'отменен': 'Отменен'
  }
  return statusTexts[status] || status
}

const getMedicalCardStatusClass = (status) => {
  const statusClasses = {
    'active': 'status-active',
    'completed': 'status-completed',
    'archived': 'status-archived'
  }
  return statusClasses[status] || 'status-active'
}

const getMedicalCardStatusText = (status) => {
  const statusTexts = {
    'active': 'Активна',
    'completed': 'Завершена',
    'archived': 'В архиве'
  }
  return statusTexts[status] || status
}

const closeForm = () => {
  emit('close')
}

const handleLogout = () => {
  localStorage.removeItem('authToken')
  localStorage.removeItem('userData')
  router.push('/')
  
  setTimeout(() => {
    window.location.reload()
  }, 100)
}
</script>

<template>
  <div class="doctor-form-container">
    <div class="form-header">
      <h2>Личный кабинет врача</h2>
    </div>
    
    <div class="doctor-content">
      <div class="doctor-profile">
        <div class="profile-header">
          <img v-if="doctorData?.workers_img" 
                      :src="doctorData.workers_img" 
                      alt="Фото врача" class="doctor-avatar">
          <div class="profile-info">
            <h3>Добро пожаловать, доктор {{ doctorData.first_name }} {{ doctorData.last_name }}!</h3>
            <p class="specialization">{{ doctorSpecialization }}</p>
            <p class="experience">Опыт работы: {{ doctorData.workers_experience }} лет</p>
            <p class="doctor-description">{{ doctorData.workers_description }}</p>
          </div>
        </div>
      </div>

      <div class="doctor-actions">
        <button class="action-btn primary" @click="showTodayAppointments">
          📅 Приемы
        </button>
        <button class="action-btn secondary" @click="showPatientCards">
          📋 Медицинские карты
        </button>
        <button class="action-btn secondary" @click="showSchedule">
          🕐 Мое расписание
        </button>
      </div>

      <div v-if="activeTab === 'appointments'" class="tab-content">
        <div class="section-header">
          <h4>Мои приемы</h4>
        </div>
        
        <div class="appointments-list">
          <div v-if="loading" class="loading">Загрузка...</div>
          <div v-else-if="appointments.length === 0" class="no-data">
            На выбранную дату приемов нет
          </div>
          <div v-else class="appointment-items">
            <div v-for="appointment in appointments" :key="appointment.appointment_id" 
                 class="appointment-item" :class="getAppointmentStatusClass(appointment.appointment_status)">
              <div class="appointment-info">
                <div class="patient-name">
                  {{ getPatientName(appointment.appointment_user) }}
                </div>
                <div class="appointment-time">
                  {{ formatDateTime(appointment.appointment_date) }}
                </div>
                <div class="appointment-service">
                  Услуга: {{ getServiceName(appointment.appointment_services) }}
                </div>
                <div class="appointment-status">
                  Статус: {{ getAppointmentStatusText(appointment.appointment_status) }}
                </div>
                <div v-if="appointment.appointment_status === 'запланирован'" 
                     class="appointment-time-info">
                  <small v-if="canCompleteAppointment(appointment.appointment_date)" class="time-valid">
                    ✅ Можно завершить
                  </small>
                  <small v-else class="time-invalid">
                    ⏰ Завершить можно с {{ formatTime(appointment.appointment_date) }} в течение 30 минут
                  </small>
                </div>
              </div>
              <div class="appointment-actions">
                <button @click="updateAppointmentStatus(appointment, 'завершен')" 
                        class="btn-success" 
                        v-if="(appointment.appointment_status === 'запланирован') && canCompleteAppointment(appointment.appointment_date)">
                  Завершить прием
                </button>
                <button @click="updateAppointmentStatus(appointment, 'отменен')" 
                        class="btn-danger" 
                        v-if="appointment.appointment_status !== 'отменен' && appointment.appointment_status !== 'завершен'">
                  Отменить
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'medicalCards'" class="tab-content">
        <div class="section-header">
          <h4>Медицинские карты пациентов</h4>
          <div class="header-actions">
            <button @click="loadMedicalCards" class="btn-secondary">
              🔄 Обновить
            </button>
          </div>
        </div>

        <div class="search-section">
          <input type="text" v-model="patientSearch" placeholder="Поиск пациента..." 
                 class="search-input">
        </div>

        <div class="medical-cards-list">
          <div v-if="loading" class="loading">Загрузка...</div>
          <div v-else-if="filteredMedicalCards.length === 0" class="no-data">
            Медицинские карты не найдены
          </div>
          <div v-else class="medical-card-items">
            <div v-for="card in filteredMedicalCards" :key="card.medical_card_id" 
                 class="medical-card-item" :class="getMedicalCardStatusClass(card.medical_card_status)">
              <div class="card-header">
                <div class="patient-name">
                  {{ getPatientName(card.medical_card_user) }}
                </div>
                <div class="card-date">
                  {{ formatDate(card.medical_card_date) }}
                </div>
              </div>
              <div class="card-diagnosis">
                <strong>Диагноз:</strong> {{ card.medical_card_diagnosis || 'Не указан' }}
              </div>
              <div class="card-purpose">
                <strong>Назначение:</strong> {{ card.medical_card_purpose || 'Не указано' }}
              </div>
              <div class="card-service">
                <strong>Услуга:</strong> {{ getServiceName(card.medical_card_services) }}
              </div>
              <div class="card-status">
                Статус: {{ getMedicalCardStatusText(card.medical_card_status) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'schedule'" class="tab-content">
        <div class="section-header">
          <h4>Мое расписание</h4>
          <button @click="loadSchedule" class="btn-secondary">
            🔄 Обновить
          </button>
        </div>

        <div class="schedule-controls">
          <div class="week-navigation">
            <button @click="previousWeek" class="btn-secondary">◀ Предыдущая</button>
            <span class="current-week">{{ currentWeekRange }}</span>
            <button @click="nextWeek" class="btn-secondary">Следующая ▶</button>
          </div>
        </div>

        <div class="schedule-grid">
          <div v-for="day in scheduleDays" :key="day.date" class="schedule-day">
            <div class="day-header">{{ day.name }}, {{ day.date }}</div>
            <div class="day-appointments">
              <div v-if="day.appointments.length === 0" class="no-appointments">
                Приемов нет
              </div>
              <div v-else>
                <div v-for="appointment in day.appointments" :key="appointment.appointment_id"
                     class="schedule-appointment" :class="getAppointmentStatusClass(appointment.appointment_status)">
                  <div class="appointment-time">{{ formatTime(appointment.appointment_date) }}</div>
                  <div class="appointment-patient">{{ getPatientName(appointment.appointment_user) }}</div>
                  <div class="appointment-service">{{ getServiceName(appointment.appointment_services) }}</div>
                  <div class="appointment-status-small">{{ getAppointmentStatusText(appointment.appointment_status) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="showCreateMedicalCard" class="modal-overlay">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Создать медицинскую карту</h3>
            <button @click="closeMedicalCardModal" class="close-button">×</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>Пациент:</label>
              <input type="text" :value="getPatientName(newMedicalCard.medical_card_user_id)" 
                     class="form-input" disabled>
              <small class="form-help">Пациент выбран автоматически из записи</small>
            </div>
            <div class="form-group">
              <label>Услуга:</label>
              <input type="text" :value="getServiceName(newMedicalCard.medical_card_services_id)" 
                     class="form-input" disabled>
              <small class="form-help">Услуга выбрана автоматически из записи</small>
            </div>
            <div class="form-group">
              <label>Диагноз: <span class="required">*</span></label>
              <input type="text" v-model="newMedicalCard.medical_card_diagnosis" 
                     class="form-input" placeholder="Введите диагноз" 
                     :class="{ 'error': newMedicalCard.medical_card_diagnosis.length > 75 }"
                     maxlength="75"
                     required>
              <small class="char-counter" :class="{ 'error': newMedicalCard.medical_card_diagnosis.length > 75 }">
                {{ newMedicalCard.medical_card_diagnosis.length }}/75 символов
              </small>
              <small v-if="newMedicalCard.medical_card_diagnosis.length > 75" class="error-message">
                ❌ Диагноз не может превышать 75 символов
              </small>
            </div>
            <div class="form-group">
              <label>Назначение: <span class="required">*</span></label>
              <textarea v-model="newMedicalCard.medical_card_purpose" 
                        class="form-input textarea" placeholder="Введите назначение" 
                        :class="{ 'error': !newMedicalCard.medical_card_purpose.trim() }"
                        required></textarea>
              <small v-if="!newMedicalCard.medical_card_purpose.trim()" class="error-message">
                ❌ Назначение не может быть пустым
              </small>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="closeMedicalCardModal" class="btn-secondary">Отмена</button>
            <button @click="saveMedicalCard" class="btn-primary" :disabled="!isMedicalCardFormValid">
              Создать карту и завершить прием
            </button>
          </div>
        </div>
      </div>

      <div class="logout-section">
        <button @click="handleLogout" class="logout-bottom-btn">
          🚪 Выйти из аккаунта
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.appointment-time-info {
  margin-top: 8px;
  font-size: 12px;
}

.time-valid {
  color: #48bb78;
  font-weight: 600;
}

.time-invalid {
  color: #ed8936;
}

.form-help {
  color: #718096;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.required {
  color: #e53e3e;
}

.char-counter {
  color: #718096;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.char-counter.error {
  color: #e53e3e;
}

.error-message {
  color: #e53e3e;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

.form-input.error {
  border-color: #e53e3e;
  box-shadow: 0 0 0 3px rgba(229, 62, 62, 0.1);
}

.doctor-form-container {
  padding: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: white;
  position: relative;
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

.form-header {
  padding: 20px 40px 30px 40px;
  border-bottom: 1px solid #f1f3f4;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.form-header h2 {
  text-align: center;
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
  flex: 1;
}

.logout-btn {
  background: #f8f9fa;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 600;
  color: #718096;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.logout-btn:hover {
  background: #fed7d7;
  border-color: #feb2b2;
  color: #c53030;
  transform: translateY(-1px);
}

.doctor-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 30px 40px 40px 40px;
  gap: 25px;
  overflow-y: auto;
}

.doctor-profile {
  background: #667eea;
  color: white;
  padding: 25px;
  border-radius: 12px;
  margin-bottom: 10px;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 15px;
}

.doctor-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid white;
  object-fit: cover;
}

.profile-info h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
}

.specialization {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 5px 0;
  opacity: 0.95;
}

.experience {
  font-size: 14px;
  margin: 0 0 8px 0;
  opacity: 0.9;
}

.doctor-description {
  font-size: 14px;
  margin: 0;
  opacity: 0.85;
  font-style: italic;
}

.doctor-actions {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 15px;
  margin-bottom: 10px;
}

.action-btn {
  padding: 16px 20px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.action-btn.secondary {
  background: #f7fafc;
  color: #4a5568;
  border: 2px solid #e2e8f0;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.tab-content {
  margin-top: 10px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e2e8f0;
}

.section-header h4 {
  font-size: 20px;
  color: #2d3748;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
  position: static;
}

.date-filter {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-section {
  margin-bottom: 20px;
}

.search-input, .form-input {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.search-input:focus, .form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.textarea {
  min-height: 100px;
  resize: vertical;
  font-family: inherit;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #4a5568;
  font-size: 14px;
}

.appointments-list,
.medical-cards-list {
  max-height: 500px;
  overflow-y: auto;
}

.appointment-item,
.medical-card-item {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.appointment-item:hover,
.medical-card-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-1px);
}

.appointment-info {
  flex: 1;
  margin-right: 20px;
}

.medical-card-item {
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #e2e8f0;
}

.patient-name {
  font-weight: 600;
  font-size: 16px;
  color: #2d3748;
  margin-bottom: 8px;
}

.appointment-time,
.card-date {
  color: #718096;
  font-size: 14px;
  margin-bottom: 8px;
}

.appointment-service,
.card-diagnosis,
.card-purpose,
.card-service,
.card-status {
  font-size: 14px;
  margin-bottom: 5px;
  line-height: 1.4;
}

.appointment-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 140px;
}

.btn-primary {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-primary:hover {
  background: #5a67d8;
}

.btn-primary:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

.btn-success {
  background: #48bb78;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-success:hover {
  background: #38a169;
}

.btn-danger {
  background: #f56565;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-danger:hover {
  background: #e53e3e;
}

.status-pending {
  border-left: 4px solid #ed8936;
}

.status-completed {
  border-left: 4px solid #4299e1;
}

.status-cancelled {
  border-left: 4px solid #f56565;
}

.status-active {
  border-left: 4px solid #48bb78;
}

.status-archived {
  border-left: 4px solid #a0aec0;
}

.schedule-controls {
  margin-bottom: 25px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.week-navigation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.current-week {
  font-weight: 600;
  color: #2d3748;
  font-size: 16px;
}

.schedule-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.schedule-day {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.day-header {
  font-weight: 600;
  padding: 15px;
  background: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
  color: #2d3748;
}

.day-appointments {
  padding: 15px;
  min-height: 150px;
}

.schedule-appointment {
  background: #f8f9fa;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 6px;
  border-left: 3px solid #667eea;
}

.appointment-time {
  font-weight: 600;
  font-size: 12px;
  color: #667eea;
  margin-bottom: 4px;
}

.appointment-patient {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 2px;
}

.appointment-service {
  font-size: 12px;
  color: #718096;
  margin-bottom: 4px;
}

.appointment-status-small {
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  background: #e2e8f0;
  color: #4a5568;
  display: inline-block;
}

.no-appointments {
  text-align: center;
  color: #a0aec0;
  font-style: italic;
  font-size: 14px;
  padding: 20px 0;
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
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 0;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  padding: 25px 25px 15px 25px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #2d3748;
  font-size: 20px;
}

.modal-body {
  padding: 25px;
}

.modal-footer {
  padding: 20px 25px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.loading,
.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #718096;
  font-style: italic;
  font-size: 16px;
}

.loading {
  color: #667eea;
}

.logout-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.logout-bottom-btn {
  width: 100%;
  padding: 15px 20px;
  background: #fed7d7;
  border: 2px solid #feb2b2;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #c53030;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-bottom-btn:hover {
  background: #feb2b2;
  border-color: #fc8181;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(197, 48, 48, 0.2);
}

.doctor-content::-webkit-scrollbar {
  width: 6px;
}

.doctor-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.doctor-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.doctor-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

@media (max-width: 768px) {
  .form-header {
    padding: 30px 20px 20px 20px;
    flex-direction: column;
    gap: 15px;
  }
  
  .form-header h2 {
    font-size: 24px;
  }
  
  .doctor-content {
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

  .doctor-actions {
    grid-template-columns: 1fr;
  }

  .appointment-item {
    flex-direction: column;
    gap: 15px;
  }

  .appointment-actions {
    flex-direction: row;
    justify-content: flex-start;
    flex-wrap: wrap;
    width: 100%;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .header-actions {
    position: static;
    justify-content: flex-start;
    width: 100%;
  }

  .schedule-grid {
    grid-template-columns: 1fr;
  }

  .week-navigation {
    flex-direction: column;
    gap: 10px;
  }

  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .modal-content {
    margin: 20px;
    width: calc(100% - 40px);
  }
}

@media (max-width: 480px) {
  .doctor-content {
    padding: 15px 15px 25px 15px;
  }

  .form-header {
    padding: 25px 15px 15px 15px;
  }

  .doctor-profile {
    padding: 20px;
  }

  .action-btn {
    padding: 14px 16px;
    font-size: 14px;
  }

  .btn-primary,
  .btn-secondary,
  .btn-success,
  .btn-info,
  .btn-danger {
    padding: 8px 12px;
    font-size: 12px;
  }
}
</style>