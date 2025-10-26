<script setup>
import { ref, onMounted } from 'vue'
import ServiceCard from '../components/ServiceCard.vue'

const services = ref([])

const loading = ref(false)
const error = ref(null)

const fetchServices = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await fetch('http://localhost:8000/services/', {
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

onMounted(() => {
  fetchServices()
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

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка услуг...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchServices" class="retry-button">Попробовать снова</button>
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