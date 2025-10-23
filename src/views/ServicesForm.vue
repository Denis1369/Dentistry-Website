<script setup>
import { ref, onMounted } from 'vue'
import ServiceCard from '../components/ServiceCard.vue'

const services = ref([])

const generateMockServices = () => {
  const serviceTitles = [
    'Лечение кариеса и установка пломб',
    'Имплантация зубов',
    'Профессиональная чистка',
    'Отбеливание зубов',
    'Установка брекетов',
    'Лечение десен',
    'Удаление зубов',
    'Детская стоматология',
    'Протезирование',
    'Керамические виниры'
  ]

  const serviceDescriptions = [
    'Качественное лечение кариеса с установкой современных пломб',
    'Современная имплантация с гарантией результата',
    'Комплексная чистка зубов с удалением налета и камня',
    'Безопасное отбеливание с сохранением эмали',
    'Коррекция прикуса современными брекет-системами',
    'Комплексное лечение заболеваний пародонта',
    'Безболезненное удаление зубов любой сложности',
    'Специализированная стоматология для детей',
    'Изготовление и установка зубных протезов',
    'Эстетическая реставрация с помощью виниров'
  ]

  return serviceTitles.map((title, index) => ({
    services_id: index + 1,
    services_title: title,
    services_description: serviceDescriptions[index],
    services_price: Math.floor(Math.random() * 10000) + 2000,
    services_img: null,
    services_profession_id: Math.floor(Math.random() * 5) + 1,
    services_status: 'akтивно'
  }))
}

onMounted(() => {
  services.value = generateMockServices()
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
      <div class="services-grid">
        <ServiceCard
          v-for="service in services"
          :key="service.services_id"
          :service="{
            id: service.services_id,
            title: service.services_title,
            description: service.services_description,
            price: service.services_price.toLocaleString(),
            image: null
          }"
        />
      </div>
    
  </main>
</template>

<style scoped>
.services-page {
  padding: 120px 60px 60px;
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