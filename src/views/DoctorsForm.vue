<script setup>
import { ref, onMounted } from 'vue'
import DoctorsCard from '../components/doctor_card.vue'
import defaultDoctorImage from '../components/icons/dricon.jpg'

const doctors = ref([])
const loading = ref(false)
const error = ref(null)


const fetchDoctors = async () => {
  loading.value = true
  error.value = null
  try {
    console.log('Загрузка врачей...')
    
    const response = await fetch('http://127.0.0.1:8000/workers/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })

    console.log('Ответ сервера:', response)

    if (!response.ok) {
      const errorText = await response.text()
      console.error('Ошибка ответа:', errorText)
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    console.log('Полученные данные:', data)

    let doctorsData = data.doctors || data.workers || data
    
    if (!Array.isArray(doctorsData)) {
      doctorsData = []
    }

    doctors.value = doctorsData
      .filter(doctor => 
        doctor.workers_status === 'активный'
      )
      .map(doctor => {
        return {
          id: doctor.workers_id,
          name: doctor.workers_last_name + doctor.workers_name,
          specialty: doctor.workers_profession_id,
          experience: doctor.workers_experience,
          description: doctor.workers_description,
          image: defaultDoctorImage
        }
      })

    console.log('Обработанные врачи:', doctors.value)

  } catch (err) {
    console.error('Ошибка при загрузке врачей:', err)
    error.value = 'Не удалось загрузить информацию о врачах. Пожалуйста, попробуйте позже.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDoctors()
})
</script>

<template>
  <main class="doctors-page">
    <div class="container">
      <h1 class="page-title">Наши врачи</h1>
      <p class="page-description">
        Профессиональная команда стоматологов с многолетним опытом работы. 
        Каждый специалист обладает высокой квалификацией и постоянно совершенствует свои навыки.
      </p>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка информации о врачах...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchDoctors" class="retry-button">Попробовать снова</button>
        
      </div>

      <div v-else class="doctors-grid">
        <DoctorsCard
          v-for="doctor in doctors"
          :key="doctor.id"
          :doctor="doctor"
        />
        <div v-if="doctors.length === 0" class="no-doctors">
          <p>Врачи не найдены</p>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.doctors-page {
  padding: 40px 0;
  min-height: 100vh;
  background: #f8f9fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  font-size: 36px;
  font-weight: 700;
  color: #2c3e50;
  text-align: center;
  margin-bottom: 16px;
}

.page-description {
  font-size: 18px;
  color: #5a6c7d;
  text-align: center;
  max-width: 700px;
  margin: 0 auto 40px;
  line-height: 1.6;
}

.doctors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  margin-top: 40px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #5285ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-state p {
  color: #5a6c7d;
  font-size: 16px;
}

.error-state {
  text-align: center;
  padding: 40px 20px;
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 8px;
  margin: 20px 0;
}

.error-state p {
  color: #c53030;
  margin-bottom: 16px;
  font-size: 16px;
}

.retry-button {
  background: #5285ff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
  margin: 0 8px;
}

.retry-button:hover {
  background: #3a75ff;
}

.test-data-button {
  background: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
  margin: 0 8px;
}

.test-data-button:hover {
  background: #218838;
}

.no-doctors {
  text-align: center;
  padding: 40px;
  color: #5a6c7d;
  grid-column: 1 / -1;
}

@media (max-width: 768px) {
  .doctors-page {
    padding: 100px 0 40px;
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .page-description {
    font-size: 16px;
    padding: 0 10px;
  }
  
  .doctors-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .error-state {
    padding: 20px;
  }
  
  .retry-button,
  .test-data-button {
    display: block;
    width: 100%;
    margin: 8px 0;
  }
}
</style>