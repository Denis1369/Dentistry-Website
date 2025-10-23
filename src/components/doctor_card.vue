<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  employee: {
    type: Object,
    required: true,
    default: () => ({
      name: '',
      lastname: '',
      position: '',
      experience: '',
      description:''
    })
  }
})

const emit = defineEmits(['book-appointment', 'show-details'])

const handleBookAppointment = () => {
  emit('book-appointment', props.employee)
}

const handleShowDetails = () => {
  emit('show-details', props.employee)
}
</script>

<template>
  <div class="employee-card">
    <div class="employee-photo">
      <div class="photo-placeholder">
        <span>Фото</span>
      </div>
    </div>
    
    <div class="employee-info">
      <h3 class="employee-name">{{ employee.name }} {{ employee.lastname }} </h3>
      <p class="employee-position">{{ employee.position }}</p>
      <p class="employee-experience">Стаж {{ employee.experience }} лет</p>
      <p class="employee-description">{{ employee.description }}</p>
      
      <div class="employee-actions">
        <button class="btn-primary" @click="handleBookAppointment">
          Записаться →
        </button>
        <button class="btn-secondary" @click="handleShowDetails">
          Подробнее
        </button>
      </div>
    </div>
  </div>
</template>



<style scoped>
.employee-card {
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 320px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.employee-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.employee-photo {
  margin-bottom: 16px;
}

.photo-placeholder {
  width: 100%;
  height: 200px;
  background-color: #f5f5f5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 14px;
  border: 1px dashed #ddd;
}

.employee-info {
  text-align: center;
}

.employee-name {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #333;
}

.employee-position {
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 8px 0;
  color: #666;
}

.employee-experience {
  font-size: 14px;
  margin: 0 0 12px 0;
  color: #888;
}

.employee-description {
  font-size: 14px;
  line-height: 1.4;
  margin: 0 0 20px 0;
  color: #555;
}

.employee-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s ease;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-secondary {
  background: transparent;
  color: #007bff;
  border: 1px solid #007bff;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #007bff;
  color: white;
}
</style>