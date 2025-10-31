<script setup>
const props = defineProps({
  service: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['appointment'])

const hasValidImage = (image) => {
  return image && image.trim() !== '' && image !== 'null'
}

const handleAppointment = () => {
  emit('appointment', props.service)
}
</script>

<template>
  <div class="service-card">
    <div class="card-image">
      <img 
        v-if="hasValidImage(service.image)" 
        :src="service.image" 
        :alt="service.title"
      >
      <div class="image-placeholder" v-else>
        <span>Изображение услуги</span>
      </div>
    </div>
    <div class="card-content">
       <div v-if="service.category" class="service-category">
        {{ service.category }}
      </div>
      <h3 class="service-title">{{ service.title }}</h3>
      <p class="service-description">{{ service.description }}</p>
      <div class="card-footer">
        <div class="service-price">от {{ service.price }} ₽</div>
        <button class="appointment-btn" @click="handleAppointment">
          Записаться
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.service-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(82, 133, 255, 0.15);
  background: #f8fbff;
  border-color: #5285ff;
}

.card-image {
  height: 200px;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  color: #667eea;
  font-size: 14px;
  text-align: center;
  padding: 20px;
}

.card-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  position: relative;
}

.service-category {
  position: absolute;
  top: -12px;
  left: 16px;
  background: #5285ff;
  color: white;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(82, 133, 255, 0.3);
  z-index: 1;
  white-space: nowrap;
  max-width: calc(100% - 32px);
  overflow: hidden;
  text-overflow: ellipsis;
}

.service-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 12px;
  line-height: 1.3;
  min-height: 46px;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-top: 8px;
}

.service-description {
  font-size: 14px;
  color: #5a6c7d;
  line-height: 1.5;
  margin-bottom: 16px;
  flex-grow: 1;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 63px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: auto;
  flex-shrink: 0;
}

.service-price {
  font-size: 20px;
  font-weight: 700;
  color: #5285ff;
  white-space: nowrap;
}

.appointment-btn {
  background: #5285ff;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 120px;
  flex-shrink: 0;
}

.appointment-btn:hover {
  background: #3a75ff;
  transform: translateY(-1px);
}

@media (max-width: 480px) {
  .card-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 8px;
  }
  
  .appointment-btn {
    min-width: auto;
  }
}
</style>