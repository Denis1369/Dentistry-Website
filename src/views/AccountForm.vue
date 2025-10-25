<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

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
        
        <div class="account-info">
          <div class="info-card">
            <h2>Добро пожаловать в личный кабинет!</h2>
            <p>Здесь вы можете управлять своими данными и записями.</p>
          </div>
          
          <div class="actions">
            <button 
              @click="handleLogout" 
              class="logout-btn"
            >
              Выйти из аккаунта
            </button>
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
  align-items: center;
  justify-content: center;
  min-height: 80vh;
}

.content-wrapper {
  width: 100%;
  max-width: 600px;
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
}

.account-info {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.info-card h2 {
  font-size: 24px;
  margin-bottom: 15px;
  color: #34495e;
}

.info-card p {
  font-size: 16px;
  color: #7f8c8d;
  line-height: 1.5;
}

.actions {
  margin-top: 30px;
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
  max-width: 250px;
}

.logout-btn:hover {
  background: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}
</style>