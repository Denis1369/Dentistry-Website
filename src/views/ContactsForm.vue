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