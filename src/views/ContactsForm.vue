<script setup>

</script>

<template>
    <main class="main">
        <div class="container">
            <h1>Контакты</h1>
            <p>Мы всегда рады вашим вопросам и предложениям. Свяжитесь с нами удобным для вас способом.</p>

            <div class="contact-info">
                <h2>Наши контакты</h2>
                <p><strong>Телефон:</strong> <a href="tel:+74951234567">+7 (495) 123-45-67</a></p>
                <p><strong>Электронная почта:</strong> <a href="mailto:info@example.com">info@example.com</a></p>
                <p><strong>Адрес:</strong> г. Уфа, пр. Октября, д. 10</p>
            </div>

            <div class="work-hours">
                <h2>Режим работы</h2>
                <p>Пн-Пт: с 9:00 до 18:00</p>
                <p>Сб-Вс: выходной</p>
            </div>
        </div>
    </main>
</template>

<style scoped>
.main{
    margin-top: auto;
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
  background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-description {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 40px;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.btn-service {
  background: #fff;
  color: #294381;
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
  color: #fff;
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

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
}

.main h1 {
    color: #2c3e50;
    font-size: 2.5rem;
    margin-bottom: 20px;
    text-align: center;
    font-weight: 700;
}

.main h2 {
    color: #34495e;
    font-size: 1.5rem;
    margin-bottom: 15px;
    font-weight: 600;
}

.main p {
    color: #555;
    font-size: 1.1rem;
    margin-bottom: 15px;
}

.contact-info,
.work-hours {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 30px;
}

.contact-info h2,
.work-hours h2 {
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

.contact-info p,
.work-hours p {
    margin-bottom: 12px;
    display: flex;
    align-items: center;
}


.work-hours strong {
    color: #2c3e50;
    min-width: 160px;
    display: inline-block;
}

.contact-info strong{
    margin-right: 7px;
}

.contact-info a {
    color: #3498db;
    text-decoration: none;
    transition: color 0.3s ease;
}

.contact-info a:hover {
    color: #2980b9;
    text-decoration: underline;
}

@media (max-width: 768px) {
    .main {
        padding: 40px 0;
    }
    
    .main h1 {
        font-size: 2rem;
    }
    
    .container {
        padding: 0 15px;
    }
    
    .contact-info,
    .work-hours {
        padding: 20px;
    }
    
    .contact-info p,
    .work-hours p {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .contact-info strong,
    .work-hours strong {
        min-width: auto;
        margin-bottom: 5px;
    }
}
</style>