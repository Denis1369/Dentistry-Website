<script setup>
import { ref } from 'vue'
import EmployeeCard from '../components/doctor_card.vue'

const doctor1 = ref({
  name: 'Дмитрий',
  lastname: 'Сафронов',
  position: 'Ортопед',
  experience: '15',
  description: 'Профи в эстетическом протезировании. Улыбка — его точная работа.'
})

const doctor2 = ref({
  name: 'Иван',
  lastname: 'Петров',
  position: 'Терапевт',
  experience: '10',
  description: 'Специалист по лечению и профилактике заболеваний зубов.'
})

const handleAppointment = (employee) => {
  console.log('Запись к:', employee)
  // Логика записи на прием
}

const handleDetails = (employee) => {
  console.log('Подробнее о:', employee)
  // Логика показа детальной информации
}
</script>

<template>
    <main class="main">
<div class="container">
            <h1>Врачи</h1>
            <p>Наша клиника предоставляет лучших врачей этого города!</p>
            
    
  </div>
  <div class="employees-grid">
        <EmployeeCard 
        :employee="doctor1"
        @book-appointment="handleAppointment"
        @show-details="handleDetails"
        />
        
        <EmployeeCard 
        :employee="doctor2"
        @book-appointment="handleAppointment"
        @show-details="handleDetails"
        />
    </div>
    </main>

</template>



<style>
.main {
    margin-top: 100px;
}
.main h1 {

    color: #2c3e50;
    font-size: 2.5rem;
    margin-bottom: 20px;
    text-align: center;
    font-weight: 700;
}

.main p {
    color: #555;
    font-size: 1.1rem;
    margin-bottom: 15px;
}
.container{
    display: flex;
    flex-direction: column;
    align-items: center;
}
.employees-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 400px));
  padding: 10px;
}
</style>