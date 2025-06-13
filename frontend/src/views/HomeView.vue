<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import BookCard from '@/components/BookCard.vue'

const popularBooks = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:8000/books/popular/')
    popularBooks.value = response.data
  } catch (error) {
    console.error('Ошибка при загрузке популярных книг:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <main>
    <!-- Hero секция -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="font-special">Откройте для себя мир книг</h1>
          <p class="hero-subtitle">Создавайте свой список для чтения, делитесь впечатлениями и находите новые книги</p>
          <router-link to="/books" class="cta-button">Начать читать</router-link>
        </div>
      </div>
    </section>

    <!-- Популярные книги -->
    <section class="popular-books">
      <div class="container">
        <h2 class="section-title font-special">Популярные книги</h2>
        <div class="books-grid" v-if="!loading">
          <BookCard
            v-for="book in popularBooks"
            :key="book.id"
            :book="book"
          />
        </div>
        <div v-else class="loading">
          Загрузка книг...
        </div>
      </div>
    </section>

    <!-- Преимущества -->
    <section class="features">
      <div class="container">
        <h2 class="section-title font-special">Почему выбирают нас</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3>Большая библиотека</h3>
            <p>Тысячи книг различных жанров</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3>Личные списки</h3>
            <p>Создавайте и управляйте своими списками для чтения</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>Обсуждения</h3>
            <p>Делитесь мнением и общайтесь с другими читателями</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Отзывы -->
    <section class="testimonials">
      <div class="container">
        <h2 class="section-title font-special">Отзывы читателей</h2>
        <div class="testimonials-grid">
          <div class="testimonial-card">
            <p class="testimonial-text">"Отличный сервис! Нашел много интересных книг и познакомился с единомышленниками."</p>
            <div class="testimonial-author">Анна К.</div>
          </div>
          <div class="testimonial-card">
            <p class="testimonial-text">"Удобно вести список прочитанных книг и планировать новые."</p>
            <div class="testimonial-author">Михаил П.</div>
          </div>
          <div class="testimonial-card">
            <p class="testimonial-text">"Люблю общаться с другими читателями и узнавать о новых книгах."</p>
            <div class="testimonial-author">Елена С.</div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.hero {
  background: linear-gradient(135deg, var(--dark-color) 0%, var(--pale-color) 100%);
  color: white;
  padding: 120px 0;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero h1 {
  font-size: 48px;
  margin-bottom: 24px;
}

.hero-subtitle {
  font-size: 20px;
  margin-bottom: 32px;
  opacity: 0.9;
}

.cta-button {
  display: inline-block;
  background: white;
  color: var(--dark-color);
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  transition: transform 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-title {
  font-size: 32px;
  text-align: center;
  margin-bottom: 48px;
}

.popular-books {
  padding: 80px 0;
  background: #f8f9fa;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.features {
  padding: 80px 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.feature-card {
  text-align: center;
  padding: 32px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.feature-card h3 {
  font-size: 20px;
  margin-bottom: 12px;
}

.testimonials {
  padding: 80px 0;
  background: #f8f9fa;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.testimonial-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.testimonial-text {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 16px;
}

.testimonial-author {
  font-weight: 600;
  color: var(--pale-color);
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: var(--pale-color);
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 18px;
  }
  
  .section-title {
    font-size: 28px;
  }
}
</style>