<script setup>
// Получаем props от родительского компонента
const props = defineProps({
  switchView: {
    type: Function,
    required: true
  },
  openRegistration: {
    type: Function,
    required: true
  },
  openLogin: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['open-registration', 'open-login'])

const openRegistrationForm = () => {
  emit('open-registration')
}

const openLoginForm = () => {
  emit('open-login')
}

// Функция для перехода на страницу контактов
const goToContacts = () => {
  props.switchView('contacts')
}
</script>

<template>
    <header class="header">
      <div class="header-content">
        <div class="name-dent">
          <img src="/src/components/icons8-зуб-100.png" alt="Dental Tech"/>
          <h1>Dental Tech</h1>
        </div>
        <nav class="navigation">
          <a @click="goToContacts" style="cursor: pointer; background-color: #ffffff15;">О нас</a>
          <a href="">Услуги</a>
          <a href="">Врачи</a>
          <a @click="goToContacts" style="cursor: pointer;">Контакты</a>
        </nav>
        <div class="account">
            <button @click="openLoginForm" class="nav-button">
                <img src="/src/components/icons8-тестовый-аккаунт-100.png" alt="Аккаунт">
          </button>
          <button class="btn-appointment">Записаться</button>
        </div>
      </div>
    </header>
    
    <main class="content">
      <div class="content-wrapper">
        <section class="hero-section">
          <div class="hero-content">
            <h1 class="hero-title">Современная стоматология по доступным ценам</h1>
            <p class="hero-description">
              Наши цены на 30% ниже, чем в большинстве клиник.<br>
              Без потери качества: сертифицированные материалы, врачи с опытом 10+ лет, гарантия лечения.
            </p>
            <div class="hero-buttons">
              <button class="btn-service">Выбрать услугу</button>
              <button class="btn-secondary">Смотреть цены</button>
            </div>
          </div>
        </section>
      </div>
    </main>
</template>

<style scoped>
.header {
  width: 100%;
  background: #5285ff;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.name-dent {
  display: flex;
  align-items: center;
  gap: 12px;
}

.name-dent img {
  width: 60px;
  height: 60px;
}

.name-dent h1 {
  font-size: 24px;
  font-weight: 700;
  color: white;
}

.navigation {
  display: flex;
  gap: 25px;
}

.navigation a {
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  background-color: #ffffff15;
  border-radius: 30px;
  padding: 10px 20px;
  transition: opacity 0.3s ease;
}

.navigation a:hover {
  opacity: 0.8;
  background-color: #ffffff20;
}

.account .nav-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.account img {
  width: 32px;
  height: 32px;
}

.account {
  display: flex;
  flex-direction: row;
  gap: 20px;
}

.content {
  width: 100%;
  flex: 1;
  display: flex;
  align-items: center;
  min-height: calc(100vh - 80px);
}

.content-wrapper {
  width: 100%;
  padding: 0 40px;
}

.hero-section {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 80px;
  align-items: center;
  width: 100%;
}

.hero-content {
  width: 100%;
  max-width: 600px;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 24px;
  background: #2c3e50;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 18px;
  line-height: 1.6;
  color: #34495e;
  margin-bottom: 40px;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-service {
  background: #667eea;
  color: white;
  border: none;
  padding: 16px 32px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: #294381;
}

.btn-service:hover {
  transform: translateY(-2px);
  box-shadow: #294381;
}

.btn-secondary {
  background: #667eea;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  padding: 16px 32px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.btn-appointment {
  background: white;
  color: #667eea;
  border: none;
  padding: 10px 30px;
  border-radius: 30px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 250px;
}

.btn-appointment:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}
</style>