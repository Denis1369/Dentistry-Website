<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted, watch, computed } from 'vue'

const router = useRouter()

const medicalRecords = ref([])
const userData = ref(null)
const loading = ref(false)
const error = ref(null)
const showAvatarModal = ref(false)
const showEditProfileModal = ref(false)
const selectedFile = ref(null)
const avatarPreview = ref(null)
const savingProfile = ref(false)

const editForm = ref({
  first_name: '',
  last_name: '',
  user_date_birth: ''
})

const isFormValid = computed(() => {
  return editForm.value.first_name?.trim() && 
         editForm.value.last_name?.trim() && 
         editForm.value.user_date_birth
})

const getUserIdFromToken = () => {
  try {
    const token = localStorage.getItem('authToken')
    if (!token) return null

    const payload = token.split('.')[1]
    const decodedPayload = JSON.parse(atob(payload))
    
    const userId = decodedPayload.user_id || decodedPayload.sub
    
    return userId
  } catch (error) {
    return null
  }
}

watch(userData, (newUserData) => {
  if (newUserData && (newUserData.user_id || newUserData.id)) {
    console.log('🎯 User ID найден, загружаем медицинские записи...')
    fetchMedicalRecords()
  }
})

const fetchUserProfile = async () => {
  loading.value = true
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
    
    if (data.user) {
      if (data.user.user_img) {
        data.user.user_img = `${data.user.user_img}?t=${Date.now()}`
      }
      userData.value = data.user
      
      if (!userData.value.user_id) {
        const userIdFromToken = getUserIdFromToken()
        if (userIdFromToken) {
          userData.value.user_id = userIdFromToken
        }
      }
    } else {
      userData.value = data
      
      if (!userData.value.user_id) {
        const userIdFromToken = getUserIdFromToken()
        if (userIdFromToken) {
          userData.value.user_id = userIdFromToken
        }
      }
    }

    localStorage.setItem('userData', JSON.stringify(userData.value))
    
  } catch (err) {
    error.value = 'Не удалось загрузить данные пользователя'
    
    const storedUserData = localStorage.getItem('userData')
    if (storedUserData) {
      userData.value = JSON.parse(storedUserData)
    }
  } finally {
    loading.value = false
  }
}

const fetchMedicalRecords = async () => {
  try {
    const token = localStorage.getItem('authToken')
    if (!token) return

    const userId = userData.value?.user_id
    
    if (!userId) {
      return
    }

    const response = await fetch(`http://127.0.0.1:8000/medical_card_set/get_medicalCard/?user_id=${userId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    })

    console.log('📊 Ответ от API медицинской карты:', response.status)

    if (!response.ok) {
      throw new Error(`Ошибка HTTP: ${response.status}`)
    }

    const data = await response.json()

    const [workersData, servicesData] = await Promise.all([
      fetchWorkers(),
      fetchServices()
    ])

    const medicalCardData = data.medicalCard || data.medicalcard || data.medical_cards || []

    if (!medicalCardData || medicalCardData.length === 0) {
      medicalRecords.value = []
      return
    }

    medicalRecords.value = medicalCardData.map((record, index) => {
      const doctorId = record.medical_card_workers
      const serviceId = record.medical_card_services
      const doctor = workersData.find(w => w.workers_id == doctorId)
      const service = servicesData.find(s => s.services_id == serviceId)
      
      return {
        id: record.medical_card_id,
        user_id: record.medical_card_user,
        doctor_id: doctorId,
        doctor_name: doctor ? 
          `${doctor.workers_name || ''} ${doctor.workers_lastname || ''}`.trim() || 'Врач не указан' 
          : 'Врач не найден',
        service_id: serviceId,
        service_name: service ? 
          service.services_title || 'Услуга не указана' 
          : 'Услуга не найдена',
        appointment_date: formatDateTime(record.medical_card_date),
        status: getStatusFromAPI(record.medical_card_status),
        status_text: getStatusText(record.medical_card_status),
        diagnosis: record.medical_card_diagnosis,
        prescriptions: record.medical_card_purpose,
        recommendations: '' 
      }
    })

  } catch (err) {
    error.value = 'Не удалось загрузить медицинские записи'
    medicalRecords.value = []
  }
}

const fetchWorkers = async () => {
  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch('http://127.0.0.1:8000/workers/get_base_many/', {
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
    return data.workers || []
  } catch (err) {
    return []
  }
}

const fetchServices = async () => {
  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch('http://127.0.0.1:8000/service/get_base/', {
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
    return data.services || []
  } catch (err) {
    return []
  }
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
      minute: '2-digit'
    })
  } catch {
    return dateString
  }
}

const getStatusFromAPI = (status) => {
  const statusMap = {
    'completed': 'completed',
    'scheduled': 'scheduled', 
    'cancelled': 'cancelled',
    'confirmed': 'scheduled',
    'pending': 'scheduled',
    'закрыта': 'completed',
    'isspons': 'completed'
  }
  return statusMap[status] || 'scheduled'
}

const getStatusText = (status) => {
  const statusTextMap = {
    'completed': 'Завершен',
    'scheduled': 'Запланирован',
    'cancelled': 'Отменен',
    'confirmed': 'Подтвержден',
    'pending': 'Ожидание',
    'закрыта': 'Завершен',
    'isspons': 'Завершен'
  }
  return statusTextMap[status] || 'Неизвестно'
}

const validateField = (value, fieldName) => {
  if (!value) {
    return `${fieldName} обязателен для заполнения`
  }
  
  if (fieldName === 'Дата рождения') {
    const birthDate = new Date(value)
    const today = new Date()
    const minDate = new Date(today.getFullYear() - 90, today.getMonth(), today.getDate())
    const maxDate = new Date(today.getFullYear() - 12, today.getMonth(), today.getDate())
    
    if (birthDate < minDate) {
      return 'Дата рождения не может быть раньше ' + minDate.toLocaleDateString('ru-RU')
    } else if (birthDate > maxDate) {
      return 'Пациент должен быть старше 12 лет'
    }
  }
  
  return ''
}

const validateForm = () => {
  const errors = []
  
  if (!editForm.value.first_name?.trim()) {
    errors.push('Имя обязательно для заполнения')
  }
  
  if (!editForm.value.last_name?.trim()) {
    errors.push('Фамилия обязательна для заполнения')
  }
  
  if (!editForm.value.user_date_birth) {
    errors.push('Дата рождения обязательна для заполнения')
  } else {
    const birthDate = new Date(editForm.value.user_date_birth)
    const today = new Date()
    const minDate = new Date(today.getFullYear() - 90, today.getMonth(), today.getDate())
    const maxDate = new Date(today.getFullYear() - 12, today.getMonth(), today.getDate())
    
    if (birthDate < minDate) {
      errors.push('Дата рождения не может быть раньше ' + minDate.toLocaleDateString('ru-RU'))
    } else if (birthDate > maxDate) {
      errors.push('Пациент должен быть старше 12 лет')
    }
  }
  
  return errors
}


const getMaxBirth = () => {
  const max = new Date()
  max.setMonth(max.getMonth() - 12)
  return max.toISOString().split('T')[0]
}

const getMinBirth = () => {
  const min = new Date()
  min.setFullYear(min.getFullYear() - 90)
  return min.toISOString().split('T')[0]
}

const formatBirthDate = (dateString) => {
  if (!dateString) return 'Не указана'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU')
  } catch {
    return dateString
  }
}

const getInitials = (user) => {
  if (!user) return ''
  const firstName = user.first_name ? user.first_name.charAt(0) : ''
  const lastName = user.last_name ? user.last_name.charAt(0) : ''
  return `${firstName}${lastName}`.toUpperCase()
}

const getFullName = (user) => {
  if (!user) return 'Пользователь'
  return `${user.last_name || ''} ${user.first_name || ''}`.trim() || user.username || 'Пользователь'
}

const openAvatarModal = () => {
  showAvatarModal.value = true
  selectedFile.value = null
  avatarPreview.value = null
}

const closeAvatarModal = () => {
  showAvatarModal.value = false
  selectedFile.value = null
  avatarPreview.value = null
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (!file.type.startsWith('image/')) {
      alert('Пожалуйста, выберите изображение')
      return
    }
    
    if (file.size > 5 * 1024 * 1024) {
      alert('Размер файла не должен превышать 5MB')
      return
    }
    
    selectedFile.value = file
    
    const reader = new FileReader()
    reader.onload = (e) => {
      avatarPreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const uploadAvatar = async () => {
  if (!selectedFile.value) {
    alert('Пожалуйста, выберите файл')
    return
  }

  try {
    const token = localStorage.getItem('authToken')
    const formData = new FormData()
    formData.append('avatar', selectedFile.value)

    const response = await fetch('http://127.0.0.1:8000/user/update_avatar/', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || `Ошибка загрузки: ${response.status}`)
    }

    const data = await response.json()
    alert(data.message || 'Аватар успешно обновлен')
    
    await fetchUserProfile()
    closeAvatarModal()
    
  } catch (err) {
    console.error('Ошибка при загрузке аватара:', err)
    alert(err.message || 'Не удалось загрузить аватар. Пожалуйста, попробуйте еще раз.')
  }
}

const openEditProfileModal = () => {
  showEditProfileModal.value = true
  editForm.value = {
    first_name: userData.value?.first_name || '',
    last_name: userData.value?.last_name || '',
    user_date_birth: userData.value?.user_date_birth || ''
  }
}

const closeEditProfileModal = () => {
  showEditProfileModal.value = false
  editForm.value = {
    first_name: '',
    last_name: '',
    user_date_birth: ''
  }
  savingProfile.value = false
}

const saveProfile = async () => {
  const errors = validateForm()
  
  if (errors.length > 0) {
    alert(errors.join('\n'))
    return
  }

  savingProfile.value = true

  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch('http://127.0.0.1:8000/user/update_profile/', {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(editForm.value)
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.error || `Ошибка сохранения: ${response.status}`)
    }

    const data = await response.json()
    alert(data.message || 'Профиль успешно обновлен!')
    
    await fetchUserProfile()
    closeEditProfileModal()
    
  } catch (err) {
    console.error('Ошибка при сохранении профиля:', err)
    alert(err.message || 'Не удалось сохранить профиль. Пожалуйста, попробуйте еще раз.')
  } finally {
    savingProfile.value = false
  }
}

onMounted(() => {
  fetchUserProfile()
})

const getStatusClass = (status) => {
  switch (status) {
    case 'completed': return 'status-completed'
    case 'scheduled': return 'status-scheduled'
    case 'cancelled': return 'status-cancelled'
    case 'rescheduled': return 'status-rescheduled'
    default: return 'status-default'
  }
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
  <main class="content">
    <div class="content-wrapper">
      <section class="account-section">
        <div class="account-header">
          <h1>Личный кабинет</h1>
        </div>
        
        <div class="account-content">
          <div class="medical-records-section">
            <h2>Медицинская карта</h2>
            <p class="section-description">История ваших посещений и медицинских записей</p>

            <div v-if="loading" class="loading">
              Загрузка медицинских записей...
            </div>

             <div v-else-if="error" class="error">
              {{ error }}
            </div>
            
            <div class="records-list">
              <div 
                v-for="record in medicalRecords" 
                :key="record.id" 
                class="record-card"
              >
                <div class="record-header">
                  <div class="record-info">
                    <h3>{{ record.service_name }}</h3>
                    <p class="doctor-name">{{ record.doctor_name }}</p>
                    <p class="appointment-date">{{ record.appointment_date }}</p>
                    <p class="price">{{ record.price }}</p>
                  </div>
                   <div class="record-status">
                    <span :class="['status-badge', getStatusClass(record.status)]">
                      {{ record.status_text }}
                    </span>
                  </div>
                </div>
                
                <div class="record-details">
                  <div v-if="record.diagnosis" class="detail-item">
                    <strong>Диагноз:</strong>
                    <span>{{ record.diagnosis }}</span>
                  </div>
                  
                  <div v-if="record.prescriptions" class="detail-item">
                    <strong>Назначения:</strong>
                    <span>{{ record.prescriptions }}</span>
                  </div>
                  
                  <div v-if="record.recommendations" class="detail-item">
                    <strong>Рекомендации:</strong>
                    <span>{{ record.recommendations }}</span>
                  </div>
                  
                  <div v-if="!record.diagnosis && !record.prescriptions && !record.recommendations" 
                       class="no-details">
                    Информация будет доступна после приема
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="medicalRecords.length == 0 && !loading && !error" class="no-records">
              <p>У вас пока нет медицинских записей</p>
            </div>
          </div>
          
          <div class="account-actions">
            <div class="profile-card">
              <div class="profile-header">
                <div class="avatar-container">
                  <div class="avatar" @click="openAvatarModal">
                    <img 
                      v-if="userData?.user_img" 
                      :src="userData.user_img" 
                      :alt="getFullName(userData)" 
                      class="avatar-img"
                    >
                    <div v-else class="avatar-placeholder">
                      {{ getInitials(userData) }}
                    </div>
                    <div class="avatar-overlay">
                      <span class="edit-icon">✏️</span>
                    </div>
                  </div>
                </div>
                <div class="profile-info">
                  <h2>{{ getFullName(userData) }}</h2>
                  <p class="profile-email" v-if="userData?.email">{{ userData.email }}</p>
                  <p class="profile-username" v-if="userData?.username">@{{ userData.username }}</p>
                </div>
              </div>
              
              <div class="profile-details">
                <div class="detail-row">
                  <div class="detail-label">
                    <span class="detail-icon">👤</span>
                    Имя
                  </div>
                  <div class="detail-value">{{ userData?.first_name || 'Не указано' }}</div>
                </div>
                
                <div class="detail-row">
                  <div class="detail-label">
                    <span class="detail-icon">👥</span>
                    Фамилия
                  </div>
                  <div class="detail-value">{{ userData?.last_name || 'Не указана' }}</div>
                </div>
                
                <div class="detail-row">
                  <div class="detail-label">
                    <span class="detail-icon">📧</span>
                    Email
                  </div>
                  <div class="detail-value">{{ userData?.email || 'Не указан' }}</div>
                </div>
                
                <div class="detail-row">
                  <div class="detail-label">
                    <span class="detail-icon">🎂</span>
                    Дата рождения
                  </div>
                  <div class="detail-value">
                    {{ formatBirthDate(userData?.user_date_birth) }}
                  </div>
                </div>
              </div>

              <div class="profile-actions">
                <button @click="openEditProfileModal" class="edit-profile-btn">
                  <span class="edit-icon">✏️</span>
                  Редактировать профиль
                </button>
              </div>
            </div>
            <div class="info-card">
              <h2>Общая информация</h2>
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-number">{{ medicalRecords.length }}</div>
                  <div class="stat-label">Всего записей</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ medicalRecords.filter(r => r.status == 'completed').length }}</div>
                  <div class="stat-label">Завершенных приемов</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ medicalRecords.filter(r => r.status === 'scheduled').length }}</div>
                  <div class="stat-label">Предстоящих приемов</div>
                </div>
              </div>
            </div>
            
            <div class="actions">
              <button @click="handleLogout" class="logout-btn">
                Выйти из аккаунта
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
     <div v-if="showAvatarModal" class="modal-overlay" @click="closeAvatarModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Изменение аватара</h3>
          <button class="close-btn" @click="closeAvatarModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="avatar-preview">
            <div class="preview-container">
              <img 
                v-if="avatarPreview" 
                :src="avatarPreview" 
                alt="Предпросмотр" 
                class="preview-img"
              >
              <div v-else class="preview-placeholder">
                {{ getInitials(userData) }}
              </div>
            </div>
          </div>
          
          <div class="file-input-container">
            <label class="file-input-label">
              <input 
                type="file" 
                accept="image/*" 
                class="file-input"
                @change="handleFileSelect"
              >
              <span class="file-input-text">
                {{ selectedFile ? 'Файл выбран' : 'Выберите изображение' }}
              </span>
              <span class="file-input-btn">Выбрать файл</span>
            </label>
            <p class="file-hint">Поддерживаемые форматы: JPG, PNG, GIF. Максимальный размер: 5MB</p>
          </div>
        </div>
        
        <div class="modal-actions">
          <button @click="closeAvatarModal" class="btn-secondary">Отмена</button>
          <button @click="uploadAvatar" class="btn-primary" :disabled="!selectedFile">
            Сохранить
          </button>
        </div>
      </div>
    </div>

    <div v-if="showEditProfileModal" class="modal-overlay" @click="closeEditProfileModal">
      <div class="modal-content profile-modal" @click.stop>
        <div class="modal-header">
          <h3>Редактирование профиля</h3>
          <button class="close-btn" @click="closeEditProfileModal">×</button>
        </div>
        
        <div class="modal-body">
          <div class="edit-profile-form">
            <div class="form-section">
              <h4 class="section-title">Основная информация</h4>
              
              <div class="form-group">
                <label class="form-label">Имя:</label>
                <input 
                  type="text" 
                  v-model="editForm.first_name"
                  class="form-input"
                  placeholder="Введите ваше имя" required
                  :class="{ 'input-error': !editForm.first_name?.trim() }"
                >
                <p v-if="!editForm.first_name?.trim()" class="error-text">Имя обязательно для заполнения</p>
              </div>
              
              <div class="form-group">
                <label class="form-label">Фамилия:</label>
                <input 
                  type="text" 
                  v-model="editForm.last_name"
                  class="form-input"
                  placeholder="Введите вашу фамилию" required
                  :class="{ 'input-error': !editForm.last_name?.trim() }"
                >
                <p v-if="!editForm.last_name?.trim()" class="error-text">Фамилия обязательна для заполнения</p>
              </div>
            </div>

            <div class="form-section">
              <h4 class="section-title">Дополнительная информация</h4>
              
              <div class="form-group">
                <label class="form-label">Дата рождения:</label>
                <input 
                  type="date" 
                  v-model="editForm.user_date_birth"
                  :min="getMinBirth()"
                  :max="getMaxBirth()"
                  @blur="validateField(editForm.user_date_birth)"
                  class="form-input" required
                  :class="{ 'input-error': !editForm.user_date_birth }"
                >
                <p v-if="!editForm.user_date_birth" class="error-text">Дата рождения обязательна для заполнения</p>
                <p class="form-hint">Возраст должен быть от 1 до 90 лет</p>
              </div>
            </div>
            <div class="current-values" v-if="userData">
              <h4 class="section-title">Текущие значения</h4>
              <div class="current-values-list">
                <div class="current-value-item">
                  <span class="current-label">Имя:</span>
                  <span class="current-value">{{ userData.first_name || 'Не указано' }}</span>
                </div>
                <div class="current-value-item">
                  <span class="current-label">Фамилия:</span>
                  <span class="current-value">{{ userData.last_name || 'Не указана' }}</span>
                </div>
                <div class="current-value-item">
                  <span class="current-label">Дата рождения:</span>
                  <span class="current-value">{{ formatBirthDate(userData.user_date_birth) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="closeEditProfileModal" class="btn-secondary">Отмена</button>
          <button 
            @click="saveProfile" 
            class="btn-primary" 
            :disabled="savingProfile || !isFormValid"
            :class="{ 'btn-disabled': !isFormValid }"
          >
            <span v-if="savingProfile" class="loading-spinner"></span>
            {{ savingProfile ? 'Сохранение...' : 'Сохранить изменения' }}
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.content {
  width: 100%;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  min-height: 100vh;
  padding: 0 0;
}

.content-wrapper {
  width: 100%;
  max-width: 1200px;
  padding: 0 40px;
}

.account-section {
  width: 100%;
}

.account-header {
  text-align: center;
  margin-bottom: 40px;
}

.account-header h1 {
  font-size: 36px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 10px;
}

.user-welcome {
  font-size: 18px;
  color: #7f8c8d;
}

.account-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
  align-items: start;
}

.medical-records-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.loading, .error {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  font-size: 16px;
}

.error {
  color: #e74c3c;
}

.medical-records-section h2 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #34495e;
}

.section-description {
  color: #7f8c8d;
  margin-bottom: 25px;
  font-size: 14px;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.record-card {
  border: 1px solid #e1e8ed;
  border-radius: 8px;
  padding: 20px;
  background: #fafbfc;
  transition: all 0.3s ease;
}

.record-card:hover {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.record-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.record-info h3 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 5px;
}

.doctor-name {
  color: #667eea;
  font-weight: 500;
  margin-bottom: 5px;
}

.appointment-date, .price {
  color: #7f8c8d;
  font-size: 14px;
}

.record-status {
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.status-completed {
  background: #d4edda;
  color: #155724;
}

.status-scheduled {
  background: #d1ecf1;
  color: #0c5460;
}

.status-cancelled {
  background: #f8d7da;
  color: #721c24;
}

.status-rescheduled {
  background: #fff3cd;
  color: #856404;
}

.record-details {
  margin-bottom: 15px;
}

.detail-item {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item strong {
  color: #34495e;
  font-size: 14px;
}

.detail-item span {
  color: #2c3e50;
  line-height: 1.4;
}

.no-details {
  color: #7f8c8d;
  font-style: italic;
  text-align: center;
  padding: 20px;
}

.record-id {
  font-size: 12px;
  color: #95a5a6;
  text-align: right;
}

.no-records {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
}

.no-records p {
  margin-bottom: 20px;
  font-size: 16px;
}

.btn-primary {
  background: #667eea;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #5a67d8;
  transform: translateY(-1px);
}

.account-actions {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f1f5f9;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  background: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 18px;
}

.edit-icon {
  font-size: 20px;
  color: white;
}

.profile-info h2 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 4px 0;
}

.profile-email {
  color: #667eea;
  font-size: 14px;
  margin: 0 0 2px 0;
}

.profile-username {
  color: #7f8c8d;
  font-size: 12px;
  margin: 0;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f8f9fa;
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
}

.detail-icon {
  font-size: 16px;
}

.detail-value {
  color: #2c3e50;
  font-weight: 600;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.profile-actions {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #f1f5f9;
  text-align: center;
}

.edit-profile-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  justify-content: center;
}

.edit-profile-btn:hover {
  background: #5a67d8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.birth-date {
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 4px 8px;
  border-radius: 6px;
}

.birth-date.editable {
  background: #f0f9ff;
  border: 1px dashed #0ea5e9;
}

.birth-date.editable:hover {
  background: #e0f2fe;
  transform: translateY(-1px);
}

.date-lock {
  font-size: 12px;
  opacity: 0.6;
  margin-left: 6px;
}

.date-add {
  font-size: 12px;
  margin-left: 6px;
  color: #0ea5e9;
}

.birth-date-form {
  text-align: center;
}

.form-description {
  color: #64748b;
  margin-bottom: 20px;
  font-size: 14px;
  line-height: 1.5;
}

.date-input-container {
  margin-bottom: 20px;
}

.date-label {
  display: block;
  margin-bottom: 8px;
  color: #374151;
  font-weight: 500;
}

.date-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.date-input:focus {
  outline: none;
  border-color: #667eea;
}

.date-hint {
  font-size: 12px;
  color: #6b7280;
  margin-top: 6px;
}

.selected-date {
  padding: 12px;
  background: #f0f9ff;
  border-radius: 8px;
  color: #0369a1;
  font-size: 14px;
  margin-top: 16px;
}

.loading-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.profile-username {
  color: #7f8c8d;
  font-size: 12px;
  margin: 0;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.info-card h2 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #34495e;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
}

.stat-item {
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  color: #7f8c8d;
  text-transform: uppercase;
  font-weight: 600;
}

.actions {
  text-align: center;
}

.logout-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.logout-btn:hover {
  background: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 0 20px;
  }
  
  .account-content {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .medical-records-section,
  .info-card {
    padding: 20px;
  }
  
  .record-header {
    flex-direction: column;
    gap: 10px;
  }
  
  .record-status {
    align-self: flex-start;
  }
  .birth-date.editable {
    padding: 8px 12px;
    text-align: center;
  }
  
  .date-input {
    font-size: 14px;
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.3s ease;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 0;
  max-width: 400px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  border-radius: 12px 12px 0 0;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #64748b;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #e2e8f0;
  color: #2c3e50;
}

.modal-body {
  padding: 24px;
}

.modal-actions {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  border-radius: 0 0 12px 12px;
}

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  flex: 1;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #cbd5e0;
  transform: translateY(-1px);
}

.btn-primary {
  background: #667eea;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  flex: 1;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary:hover:not(:disabled) {
  background: #5a67d8;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  background: #a0aec0;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.profile-modal {
  max-width: 500px;
}

.edit-profile-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  background: #f8fafc;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e2e8f0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e2e8f0;
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  color: #374151;
  font-weight: 500;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background: white;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #9ca3af;
}

.form-hint {
  font-size: 12px;
  color: #6b7280;
  margin-top: 6px;
  line-height: 1.4;
}

.current-values {
  background: #f0f9ff;
  border: 1px solid #e0f2fe;
  border-radius: 8px;
  padding: 20px;
}

.current-values-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.current-value-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #e0f2fe;
}

.current-value-item:last-child {
  border-bottom: none;
}

.current-label {
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
}

.current-value {
  color: #0369a1;
  font-weight: 600;
  font-size: 14px;
  background: white;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #bae6fd;
}

.avatar-preview {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.preview-container {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  background: #f7fafc;
  border: 2px dashed #cbd5e0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.3s ease;
}

.preview-container:hover {
  border-color: #667eea;
}

.preview-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 32px;
}

.file-input-container {
  text-align: center;
}

.file-input-label {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: #f7fafc;
  border: 2px dashed #cbd5e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
  justify-content: center;
}

.file-input-label:hover {
  border-color: #667eea;
  background: #edf2f7;
  transform: translateY(-1px);
}

.file-input {
  display: none;
}

.file-input-text {
  color: #4a5568;
  font-weight: 500;
  font-size: 14px;
}

.file-input-btn {
  background: #667eea;
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.file-input-label:hover .file-input-btn {
  background: #5a67d8;
}

.file-hint {
  font-size: 12px;
  color: #718096;
  margin-top: 8px;
  line-height: 1.4;
}

.avatar-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  background: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease;
  border: 3px solid white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.avatar:hover .avatar-overlay {
  opacity: 1;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 24px;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 50%;
}

.edit-icon {
  font-size: 20px;
  color: white;
}

.remove-avatar-btn {
  background: #e53e3e;
  color: white;
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(229, 62, 62, 0.3);
}

.remove-avatar-btn:hover {
  background: #c53030;
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(229, 62, 62, 0.4);
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
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

@media (max-width: 768px) {
  .modal-overlay {
    padding: 10px;
  }
  
  .modal-content {
    max-width: 100%;
    margin: 20px;
  }
  
  .modal-header {
    padding: 16px 20px;
  }
  
  .modal-body {
    padding: 20px;
  }
  
  .modal-actions {
    padding: 16px 20px;
    flex-direction: column;
  }
  
  .btn-secondary,
  .btn-primary {
    width: 100%;
  }
  
  .file-input-label {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
  
  .preview-container {
    width: 100px;
    height: 100px;
  }
  
  .preview-placeholder {
    font-size: 24px;
  }

  .profile-modal {
    max-width: 90%;
    margin: 20px;
  }
  
  .form-section {
    padding: 16px;
  }
  
  .current-values {
    padding: 16px;
  }
  
  .current-value-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
  
  .current-value {
    align-self: flex-start;
  }
}

@media (max-width: 480px) {
  .modal-content {
    margin: 10px;
  }
  
  .modal-header h3 {
    font-size: 16px;
  }
  
  .modal-body {
    padding: 16px;
  }

  .profile-modal {
    max-width: 95%;
    margin: 10px;
  }
  
  .form-section {
    padding: 12px;
  }
  
  .form-input {
    padding: 10px;
    font-size: 16px;
  }
  
  .current-values {
    padding: 12px;
  }
}
</style>