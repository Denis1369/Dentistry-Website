<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const reviews = ref([])
const showReviewForm = ref(false)
const isSubmitting = ref(false)
const loading = ref(false)
const error = ref(null)

const newReview = ref({
  feedback_rating: 5,
  feedback_text: '',
  feedback_date: ''
})

const isAuthenticated = computed(() => {
  const token = localStorage.getItem('authToken')
  return !!token && token !== 'undefined' && token !== 'null'
})

const getCurrentDateTime = () => {
  const now = new Date()
  return now.toISOString()
}

const formatDate = (dateString) => {
  if (!dateString) return 'Дата не указана'
  
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) {
      return 'Неверная дата'
    }
    return date.toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    console.error('Ошибка форматирования даты:', error)
    return 'Ошибка даты'
  }
}

const createAxiosInstance = () => {
  const token = localStorage.getItem('authToken')
  return axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : ''
    }
  })
}

const getUserName = (userData) => {
  if (!userData) return 'Анонимный пользователь'
  
  if (userData.first_name && userData.last_name) {
    return `${userData.first_name} ${userData.last_name}`
  }
  if (userData.first_name) {
    return userData.first_name
  }
  
  if (userData.last_name) {
    return userData.last_name
  }
  
  if (userData.username) {
    return userData.username
  }
  return 'Анонимный пользователь'
}


const fetchReviews = async () => {
  loading.value = true
  error.value = null
  
  try {
    const instance = createAxiosInstance()
    const response = await instance.get('/feedback/get_feedbacks/')
    
      if (response.data && response.data.feedbacks && Array.isArray(response.data.feedbacks)) {
      reviews.value = response.data.feedbacks.map((review) => {
        
        return {
          user_name: getUserName(review.feedback_user),
          rating: review.feedback_rating,
          text: review.feedback_text,
          date: review.feedback_date,
          user_data: review.feedback_user
        }
      })
    } else {
      reviews.value = []
    }
    
  } catch (error) {
    console.error('Ошибка при загрузке отзывов:', error)
    error.value = 'Не удалось загрузить отзывы. Пожалуйста, попробуйте позже.'
  } finally {
    loading.value = false
  }
}

const renderStars = (rating) => {
  const stars = []
  for (let i = 1; i <= 5; i++) {
    stars.push({
      filled: i <= rating,
      number: i
    })
  }
  return stars
}

const submitReview = async () => {
  if (!isAuthenticated.value) {
    alert('Для добавления отзыва необходимо авторизоваться')
    router.push('/login')
    return
  }

  if (!newReview.value.feedback_text.trim()) {
    alert('Пожалуйста, введите текст отзыва')
    return
  }

  isSubmitting.value = true

  try {
    const instance = createAxiosInstance()
    
    const reviewData = {
      feedback_rating: newReview.value.feedback_rating,
      feedback_text: newReview.value.feedback_text.trim(),
      feedback_date: getCurrentDateTime()
    }

    const response = await instance.post('/feedback/leave_feedback/', reviewData)

    if (response.status === 200 || response.status === 201) {
      newReview.value = { 
        feedback_rating: 5, 
        feedback_text: '', 
        feedback_date: '' 
      }
      showReviewForm.value = false
      alert('Отзыв успешно добавлен! Спасибо за ваш отзыв.')
      await fetchReviews()
    }
    
  } catch (error) {
    console.error('Ошибка при добавлении отзыва:', error)
    if (error.response?.status === 401) {
      alert('Для добавления отзыва необходимо авторизоваться')
      localStorage.removeItem('authToken')
      router.push('/login')
    } else if (error.response?.status === 400) {
      alert('Ошибка при добавлении отзыва: ' + JSON.stringify(error.response.data))
    } else if (error.code === 'NETWORK_ERROR' || error.message?.includes('Network Error')) {
      alert('Ошибка сети. Проверьте подключение к интернету.')
    } else {
      alert('Произошла ошибка при добавлении отзыва: ' + (error.message || 'Неизвестная ошибка'))
    }
  } finally {
    isSubmitting.value = false
  }
}

const openReviewForm = () => {
  if (!isAuthenticated.value) {
    alert('Для добавления отзыва необходимо авторизоваться')
    return
  }
  showReviewForm.value = true
}

const closeReviewForm = () => {
  showReviewForm.value = false
  newReview.value = { 
    feedback_rating: 5, 
    feedback_text: '', 
    feedback_date: '' 
  }
}

const updateRating = (rating) => {
  newReview.value.feedback_rating = rating
}

onMounted(() => {
  fetchReviews()
})
</script>

<template>
  <div class="reviews-page">
    <div class="reviews-header">
      <h1>Отзывы наших пациентов</h1>
      
      <button 
        @click="openReviewForm" 
        class="btn-add-review"
      >
        ➕ Написать отзыв
      </button>
    </div>

    <div v-if="showReviewForm" class="modal-overlay">
      <div class="modal-content">
        <div class="review-form">
          <div class="modal-header">
            <h2>Оставить отзыв</h2>
            <button @click="closeReviewForm" class="btn-close">×</button>
          </div>
          
          <div class="rating-section">
            <label>Оценка:</label>
            <div class="star-rating">
              <span 
                v-for="star in 5" 
                :key="star"
                @click="updateRating(star)"
                :class="{ 'star-active': star <= newReview.feedback_rating }"
                class="star"
              >
                ★
              </span>
            </div>
            <div class="rating-display">
              Выбрано: {{ newReview.feedback_rating }} из 5 звезд
            </div>
          </div>
          
          <div class="comment-section">
            <label>Ваш отзыв:</label>
            <textarea 
              v-model="newReview.feedback_text"
              placeholder="Поделитесь вашими впечатлениями..."
              rows="5"
              maxlength="500"
            ></textarea>
            <div class="char-count">{{ newReview.feedback_text.length }}/500</div>
          </div>
          
          <div class="form-actions">
            <button @click="closeReviewForm" class="btn-cancel">Отмена</button>
            <button 
              @click="submitReview" 
              :disabled="isSubmitting || !newReview.feedback_text.trim()"
              class="btn-submit"
            >
              {{ isSubmitting ? 'Отправка...' : 'Отправить отзыв' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <p class="auth-info">
      {{ isAuthenticated ? '✅ Вы авторизованы и можете оставить отзыв' : '🔒 Для добавления отзыва необходимо войти в систему' }}
    </p>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка отзывов...</p>
    </div>

    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
      <button @click="fetchReviews" class="retry-button">Попробовать снова</button>
    </div>

    <div v-else-if="reviews.length > 0" class="reviews-list">
      <div 
        v-for="review in reviews" 
        :key="review.id" 
        class="review-card"
      >
        <div class="review-header">
          <div class="user-avatar">
            {{ review.user_initials }}
          </div>
          <div class="user-info">
            <div class="user-name">{{ review.user_name }}</div>
            <div class="review-date">{{ formatDate(review.date) }}</div>
          </div>
          <div class="review-rating">
            <div class="stars">
              <span 
                v-for="star in renderStars(review.rating)" 
                :key="star.number"
                :class="{ 'star-filled': star.filled }"
                class="star"
              >
                ★
              </span>
            </div>
            <div class="rating-value">{{ review.rating }}/5</div>
          </div>
        </div>
        <div class="review-text">
          {{ review.text }}
        </div>
      </div>
    </div>

    <div v-else class="reviews-placeholder">
      <div class="placeholder-content">
        <h3>Пока нет отзывов</h3>
        <p>Будьте первым, кто оставит отзыв о нашем сервисе!</p>
        <div class="placeholder-image">
          <span>💬</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reviews-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  margin-top: 70px;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  flex-wrap: wrap;
  gap: 20px;
}

.reviews-header h1 {
  color: #333;
  font-size: 2.5em;
  margin: 0;
}

.btn-add-review {
  background: #5285ff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 25px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-add-review:hover {
  background: #3a6fe8;
  transform: translateY(-2px);
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 30px;
}

.review-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.review-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.review-header {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 16px;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 16px;
  flex-shrink: 0;
}

.user-info {
  flex-grow: 1;
}

.user-name {
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
  font-size: 16px;
}

.review-date {
  color: #666;
  font-size: 14px;
}

.review-rating {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.stars {
  display: flex;
  gap: 2px;
}

.stars .star {
  color: #ddd;
  font-size: 18px;
}

.stars .star.star-filled {
  color: #ffd700;
}

.rating-value {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.review-text {
  color: #333;
  line-height: 1.6;
  font-size: 15px;
  white-space: pre-line;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #5285ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 40px 20px;
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 8px;
  margin: 20px 0;
}

.error-state p {
  color: #c53030;
  margin-bottom: 16px;
  font-size: 16px;
}

.retry-button {
  background: #5285ff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.retry-button:hover {
  background: #3a75ff;
}

.review-form {
  padding: 0;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  color: #333;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  color: #333;
  background: #f5f5f5;
  border-radius: 50%;
}

.rating-section {
  padding: 20px 30px;
  margin: 0;
}

.rating-section label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
}

.star-rating {
  display: flex;
  gap: 5px;
  font-size: 24px;
  margin-bottom: 10px;
}

.star-rating .star {
  cursor: pointer;
  color: #ddd;
  transition: all 0.2s ease;
  padding: 2px;
}

.star-rating .star:hover {
  transform: scale(1.2);
}

.star-rating .star.star-active {
  color: #ffd700;
  text-shadow: 0 0 5px rgba(255, 215, 0, 0.5);
}

.rating-display {
  font-size: 14px;
  color: #666;
  font-style: italic;
}

.comment-section {
  padding: 0 30px 20px;
  margin: 0;
}

.comment-section label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
}

.comment-section textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  transition: border-color 0.3s ease;
}

.comment-section textarea:focus {
  border-color: #5285ff;
  outline: none;
}

.char-count {
  text-align: right;
  font-size: 12px;
  color: #666;
  margin-top: 5px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding: 20px 30px;
  background: #f8f9fa;
  border-top: 1px solid #eee;
}

.btn-cancel {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-cancel:hover {
  background: #5a6268;
}

.btn-submit {
  background: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn-submit:hover:not(:disabled) {
  background: #218838;
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.auth-info {
  font-weight: 600;
  color: #28a745 !important;
  margin-bottom: 20px;
  padding: 12px;
  background: #f8fff8;
  border-radius: 8px;
  border-left: 4px solid #28a745;
}

.reviews-placeholder {
  background: white;
  border-radius: 12px;
  padding: 60px 40px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  border: 2px solid #ddd;
  margin-top: 30px;
}

.placeholder-content h3 {
  color: #666;
  margin-bottom: 15px;
  font-size: 1.5em;
}

.placeholder-content p {
  color: #888;
  margin-bottom: 30px;
}

.placeholder-image {
  font-size: 4em;
  opacity: 0.5;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  max-width: 500px;
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-height: 90vh;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .reviews-header {
    flex-direction: column;
    text-align: center;
  }
  
  .reviews-page {
    padding: 20px 15px;
  }
  
  .review-form {
    padding: 0;
  }
  
  .rating-section,
  .comment-section,
  .date-info,
  .form-actions {
    padding-left: 20px;
    padding-right: 20px;
  }
  
  .modal-header {
    padding: 15px 20px;
  }
  
  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .review-rating {
    flex-direction: row;
    align-items: center;
    gap: 12px;
    width: 100%;
    justify-content: space-between;
  }
}
</style>