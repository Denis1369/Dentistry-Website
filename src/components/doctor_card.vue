<script setup>
import defaultDoctorImage from '../components/icons/dricon.jpg'
defineProps({
  doctor: {
    type: Object,
    required: true
  }
})

const handleAppointment = () => {
  console.log('Запись к врачу')
}

</script>

<template>
  <div class="doctor-card">
    <div class="card-image">
      <img :src= defaultDoctorImage
      >
      <div class="image-placeholder" v-if="!doctor.image">
        <span>Фото врача</span>
      </div>
    </div>
    <div class="card-content">
      <h3 class="doctor-name">{{ doctor.name }}</h3>
      <p class="doctor-specialty">{{ doctor.specialty }}</p>
      <p class="doctor-experience">Опыт работы: {{ doctor.experience }}</p>
      <p class="doctor-description">{{ doctor.description }}</p>
      <div class="card-footer">
        <button class="appointment-btn" @click="handleAppointment">
          Записаться
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.doctor-card {
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

.doctor-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(82, 133, 255, 0.15);
  background: #f8fbff;
  border-color: #5285ff;
}

.card-image {
  height: 307px;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
  position: relative;
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
}

.doctor-name {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
  line-height: 1.3;
}

.doctor-specialty {
  font-size: 16px;
  font-weight: 500;
  color: #5285ff;
  margin-bottom: 8px;
}

.doctor-experience {
  font-size: 14px;
  color: #5a6c7d;
  margin-bottom: 12px;
  font-weight: 500;
}

.doctor-description {
  font-size: 14px;
  color: #5a6c7d;
  line-height: 1.5;
  margin-bottom: 16px;
  flex-grow: 1;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: auto;
  flex-shrink: 0;
}

.doctor-rating {
  font-size: 14px;
  font-weight: 600;
  color: #ffa726;
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
  
  .card-image {
    height: 200px;
  }
}
</style>