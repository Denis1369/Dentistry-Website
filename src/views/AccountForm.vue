<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const router = useRouter()

const medicalRecords = ref([
  {
    id: 1,
    user_id: 123,
    doctor_id: 456,
    doctor_name: 'Др. Иванов А.С.',
    service_id: 789,
    service_name: 'Консультация стоматолога',
    appointment_date: '2024-01-15 14:30',
    status: 'completed',
    status_text: 'Завершен',
    diagnosis: 'Кариес',
    prescriptions: 'Пломбирование, полоскание рта раствором хлоргексидина',
    recommendations: 'Чистить зубы 2 раза в день, использовать зубную нить'
  },
  {
    id: 2,
    user_id: 123,
    doctor_id: 457,
    doctor_name: 'Др. Петрова М.В.',
    service_id: 790,
    service_name: 'Профессиональная чистка',
    appointment_date: '2024-02-20 10:00',
    status: 'completed',
    status_text: 'Завершен',
    diagnosis: 'Зубной камень',
    prescriptions: 'Профессиональная гигиена полости рта',
    recommendations: 'Повторить чистку через 6 месяцев'
  },
  {
    id: 3,
    user_id: 123,
    doctor_id: 456,
    doctor_name: 'Др. Иванов А.С.',
    service_id: 791,
    service_name: 'Лечение кариеса',
    appointment_date: '2024-03-25 16:00',
    status: 'scheduled',
    status_text: 'Запланирован',
    diagnosis: '',
    prescriptions: '',
    recommendations: ''
  }
])

const userData = ref(null)

onMounted(() => {
  const storedUserData = localStorage.getItem('userData')
  if (storedUserData) {
    userData.value = JSON.parse(storedUserData)
  }
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
            
            <div v-if="medicalRecords.length === 0" class="no-records">
              <p>У вас пока нет медицинских записей</p>
              <button class="btn-primary">Записаться на прием</button>
            </div>
          </div>
          
          <div class="account-actions">
            <div class="info-card">
              <h2>Общая информация</h2>
              <div class="stats-grid">
                <div class="stat-item">
                  <div class="stat-number">{{ medicalRecords.length }}</div>
                  <div class="stat-label">Всего записей</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ medicalRecords.filter(r => r.status === 'completed').length }}</div>
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

.appointment-date {
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

/* Адаптивность */
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
}
</style>