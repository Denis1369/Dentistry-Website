<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToServices = () => {
  router.push('/services')
}

const navigateToDoctors = () => {
  router.push('/doctors')
}

const averageRating = ref(0)
const totalReviews = ref(0)
const isLoading = ref(true)
const error = ref(null)

const fetchReviews = async () => {
  try {
    isLoading.value = true
    error.value = null
    
    const response = await axios.get('http://127.0.0.1:8000/feedback/get_feedbacks/')
    
    if (response.data && response.data.feedbacks) {
      const reviews = response.data.feedbacks
      
      if (reviews.length > 0) {
        const total = reviews.reduce((sum, review) => sum + review.feedback_rating, 0)
        averageRating.value = parseFloat((total / reviews.length).toFixed(1))
        totalReviews.value = reviews.length
      } else {
        averageRating.value = 0
        totalReviews.value = 0
      }
      
    }
  } catch (err) {
    console.error('Error fetching reviews:', err)
    error.value = err.message
    averageRating.value = 0
    totalReviews.value = 0
  } finally {
    isLoading.value = false
  }
}
onMounted(() => {
  fetchReviews()
})
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
            <button class="btn-service" @click="navigateToServices">Выбрать услугу</button>
            <button class="btn-secondary" @click="navigateToDoctors">Смотреть врачей</button>
          </div>
          
          <!-- Блок рейтинга -->
          <div class="rating-section" v-if="!isLoading && !error">
            <div class="rating-card">
              <div class="rating-main">
                <div class="rating-score">
                  {{ averageRating }}
                </div>
                <div class="rating-info">
                  <div class="rating-text">Средняя оценка</div>
                  <div class="rating-source">на основе {{ totalReviews }} отзывов</div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="rating-loading" v-else-if="isLoading">
            Загрузка рейтинга...
          </div>
          
          <div class="rating-error" v-else-if="error">
            Ошибка загрузки: {{ error }}
          </div>
        </div>
        <div class="banner">
          <img src="/src/components/icons/i (1).png" alt="Стоматология">
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.rating-error {
  color: #e53e3e;
  background: #fed7d7;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #feb2b2;
  font-size: 14px;
}
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
  margin-bottom: 30px;
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
}

.btn-service:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
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
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

/* Стили для блока рейтинга */
.rating-section {
  margin-top: 10px;
}

.rating-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e2e8f0;
  display: inline-block;
}

.rating-main {
  display: flex;
  align-items: center;
  gap: 16px;
}

.rating-score {
  font-size: 42px;
  font-weight: 700;
  line-height: 1;
  color: #667eea;
}

.rating-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.rating-text {
  font-size: 16px;
  color: #374151;
  font-weight: 600;
}

.rating-source {
  font-size: 14px;
  color: #64748b;
}

.rating-loading {
  color: #64748b;
  font-style: italic;
  padding: 10px 0;
}

/* Адаптивность */
@media (max-width: 768px) {
  .hero-section {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }
  
  .hero-title {
    font-size: 36px;
  }
  
  .hero-buttons {
    justify-content: center;
  }
  
  .rating-card {
    padding: 16px;
  }
  
  .rating-score {
    font-size: 36px;
  }
  
  .rating-text {
    font-size: 14px;
  }
  
  .rating-source {
    font-size: 12px;
  }
}
</style>