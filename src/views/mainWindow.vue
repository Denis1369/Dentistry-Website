<script setup>

</script>

<template>
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
              <button class="btn-secondary">Смотреть врачей</button>
            </div>
          </div>
          <div class ="banner">
            <img src="/src/components/icons/i (1).png"></img>
          </div>
        </section>
        <!-- <div class="line"></div> -->
      </div>
      <div class="banner">

      </div>
    </main>
</template>

<style scoped>
.content {
  width: 100%;
  display: flex;
  align-items: center;
}

.content-wrapper {
  width: 100%;
  padding: 0 40px;
}

.hero-section {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
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
  padding-bottom: 5px;
  margin-bottom: 25px;
  background: #2c3e50;
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
.line {

  margin-bottom: 30px;
  border: 1px solid #5a81c0;
  width: min(900px, 90%);

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
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
  padding: 16px 32px;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}
</style>