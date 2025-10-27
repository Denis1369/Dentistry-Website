<script setup>
import { ref, onMounted, computed } from 'vue'
import ServiceCard from '../components/ServiceCard.vue'

const services = ref([])
const categories = ref([])
const loading = ref(false)
const error = ref(null)
const selectedCategory = ref('all')

const fetchServices = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch('http://127.0.0.1:8000/services/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status} ${response.body} ${response.Error}`)
    }

    const data = await response.json()
     services.value = data.services
     .filter(service => service.services_status == 'активно')
     .map(service => ({
      services_id: service.services_id,
      services_title: service.services_title || 'Название услуги',
      services_description: service.services_description || 'Описание недоступно',
      services_price: service.services_price || 0,
      services_img: service.services_img && service.services_img.trim() !== '' 
        ? service.services_img 
        : null
    }))
  } catch (err) {
    console.error('Ошибка при загрузке услуг:', err)
    error.value = 'Не удалось загрузить услуги. Пожалуйста, попробуйте позже.'
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
    }
  } catch (err) {
    console.error('Ошибка при загрузке категорий:', err)
  }
}

const filteredServices = computed(() => {
  return services.value
})

const resetFilter = () => {
  selectedCategory.value = 'all'
}

onMounted(() => {
  fetchServices()
  fetchCategories()
})
</script>

<template>
  <main class="services-page">
    <div class="container">
      <h1 class="page-title">Наши услуги</h1>
      <p class="page-description">
        Широкий спектр стоматологических услуг по доступным ценам. 
        Качественное лечение и современное оборудование.
      </p>
      </div>

      <div class="filters-section" v-if="categories.length > 0">
        <div class="filters-header">
          <h3>Категории услуг</h3>
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
            Все услуги
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
          <span>Выбрана категория: 
            <strong>{{ categories.find(c => c.profession_id.toString() === selectedCategory)?.profession_title }}</strong>
          </span>
          <span class="services-count">Найдено услуг: {{ filteredServices.length }}</span>
        </div>
      </div>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка услуг...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchServices" class="retry-button">Попробовать снова</button>
      </div>

      <div v-else class="services-container">
        <div v-if="filteredServices.length === 0" class="no-services">
          <p v-if="selectedCategory === 'all'">Нет доступных услуг</p>
          <p v-else>
            В выбранной категории пока нет услуг
            <button @click="resetFilter" class="reset-link">Показать все услуги</button>
          </p>
        </div>
      </div>

      <div class="services-grid">
        <ServiceCard
          v-for="service in services"
          :key="service.services_id"
          :service="{
            id: service.services_id,
            title: service.services_title,
            description: service.services_description,
            price: service.services_price.toLocaleString(),
            image: service.services_img
          }"
        />
      </div>
    
  </main>
</template>

<style scoped>
.services-page {
  padding: 0 60px;
  min-height: 100vh;
  
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
  max-width: 600px;
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

.services-count {
  font-weight: 600;
  color: #5285ff;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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
}

.retry-button:hover {
  background: #3a75ff;
}

@media (max-width: 768px) {
  .services-page {
    padding: 100px 0 40px;
  }
  
  .page-title {
    font-size: 28px;
  }
  
  .page-description {
    font-size: 16px;
    padding: 0 10px;
  }
  
  .services-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>