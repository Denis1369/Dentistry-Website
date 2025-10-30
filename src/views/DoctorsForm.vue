<script setup>
import { ref, onMounted, computed } from 'vue'
import DoctorsCard from '../components/doctor_card.vue'
import defaultDoctorImage from '../components/icons/dricon.jpg'

const doctors = ref([])
const categories = ref([])
const loading = ref(false)
const error = ref(null)
const selectedCategory = ref('all')

const filteredDoctors = computed(() => {
  if (selectedCategory.value === 'all') {
    return doctors.value
  }
  
  return doctors.value.filter(doctor => 
    doctor.specialty && 
    doctor.specialty.toString() === selectedCategory.value
  )
})

const fetchDoctors = async () => {
  loading.value = true
  error.value = null
  try {
    console.log('Загрузка врачей...')
    
    const response = await fetch('http://127.0.0.1:8000/workers/get_base/', {
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

    const categoryMap = {}
    categories.value.forEach(cat => {
      categoryMap[cat.profession_id] = cat.profession_title
    })

    let doctorsData = data.doctors || data.workers || data
    
    if (!Array.isArray(doctorsData)) {
      doctorsData = []
    }

    doctors.value = doctorsData
      .filter(doctor => 
        doctor.workers_status === 'активен'
      )
      .map(doctor => {
        // Получаем название специализации из карты категорий
        const specialtyName = doctor.workers_profession ? 
          categoryMap[doctor.workers_profession] : 'Общая категория'
        
        return {
          id: doctor.workers_id,
          name: doctor.workers_last_name + ' ' + doctor.workers_name,
          experience: doctor.workers_experience,
          description: doctor.workers_description,
          image: defaultDoctorImage,
          category: specialtyName, // Отображаем название категории
          specialty: doctor.workers_profession, // Оставляем ID для фильтрации
          specialtyName: specialtyName // Добавляем название для отображения
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

const fetchCategories = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/profession/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })

    if (response.ok) {
      const data = await response.json()
      categories.value = data.profession || []
      await fetchDoctors()
    }
  } catch (err) {
    console.error('Ошибка при загрузке категорий:', err)
    await fetchDoctors()
  }
}

const resetFilter = () => {
  selectedCategory.value = 'all'
}

onMounted(() => {
  fetchCategories()
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
      
      <div class="filters-section" v-if="categories.length > 0">
        <div class="filters-header">
          <h3>Специализации врачей</h3>
          <button 
            v-if="selectedCategory !== 'all'" 
            @click="resetFilter" 
            class="reset-filter"
          >
            Сбросить фильтр
          </button>
        </div>
        <div class="categories-filter">
          <button
            class="category-btn"
            :class="{ active: selectedCategory === 'all' }"
            @click="selectedCategory = 'all'"
          >
            Все специализации
          </button>
          <button
            v-for="category in categories"
            :key="category.profession_id"
            class="category-btn"
            :class="{ active: selectedCategory === category.profession_id.toString() }"
            @click="selectedCategory = category.profession_id.toString()"
          >
            {{ category.profession_title }}
          </button>
        </div>
        
        <div v-if="selectedCategory !== 'all'" class="filter-info">
          <span>Выбрана специализация: 
            <strong>{{ categories.find(c => c.profession_id.toString() === selectedCategory)?.profession_title }}</strong>
          </span>
          <span class="doctors-count">Найдено врачей: {{ filteredDoctors.length }}</span>
        </div>
      </div>

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
          v-for="doctor in filteredDoctors"
          :key="doctor.id"
          :doctor="doctor"
        />
        <div v-if="filteredDoctors.length === 0" class="no-doctors">
          <p>Врачи по выбранной специализации не найдены</p>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.doctors-page {
  padding: 40px 0;
  min-height: 100vh;
  background: #fff;
}

.container {
  max-width: 1300px;
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

.filters-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.filters-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.reset-filter {
  background: #718096;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.reset-filter:hover {
  background: #4a5568;
}

.categories-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
}

.category-btn {
  background: white;
  color: #4a5568;
  border: 2px solid #e2e8f0;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.category-btn:hover {
  border-color: #5285ff;
  color: #5285ff;
}

.category-btn.active {
  background: #5285ff;
  color: white;
  border-color: #5285ff;
}

.filter-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  border-left: 4px solid #5285ff;
}

.doctors-count {
  font-weight: 600;
  color: #5285ff;
}

.doctors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 285px));
  gap: 40px;
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
}

.retry-button:hover {
  background: #3a75ff;
}

.no-doctors {
  text-align: center;
  padding: 40px;
  color: #5a6c7d;
  grid-column: 1 / -1;
  background: #f8fafc;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
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
  
  .filter-info {
    flex-direction: column;
    gap: 8px;
    align-items: flex-start;
  }
  
  .categories-filter {
    justify-content: center;
  }
}
</style>