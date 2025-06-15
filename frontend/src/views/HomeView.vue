<script>
import axios from 'axios'
import BookCard from '@/components/BookCard.vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import 'swiper/css'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
import { Navigation, Pagination } from 'swiper/modules'

export default {
  components: {
    BookCard,
    Swiper,
    SwiperSlide
  },
  data() {
    return {
      popularBooks: [],
      loading: true,
      swiperModules: [Navigation, Pagination]
    }
  },
  mounted() {
    this.fetchPopularBooks()
  },
  methods: {
    async fetchPopularBooks() {
      try {
        const response = await axios.get('http://5.129.207.86/api/books/popular/')
        this.popularBooks = response.data.popular_books
        console.log(this.popularBooks)
      } catch (error) {
        console.error('Ошибка при загрузке популярных книг:', error)
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<template>
  <main>

    <section class="welcome-section">
      <div class="welcome-header">
        <h1>Добро пожаловать в <span class="company-name">CapyBooks</span></h1>
        <small>Ваш персональный список для чтения — удобно, просто, эффективно</small>
      </div>
      <RouterLink class="dark-button" to="/books">Перейти к каталогу</RouterLink>
    </section>

    <section class="about-section">
      <img class="about-bg-img" src="/logo.png" alt="">

      <div class="about-content">
          <h2>О приложении</h2>
          <div>
            Это современное веб-приложение для всех, кто любит читать и хочет структурировать свой книжный путь. С BookTrack вы сможете не только вести список прочитанных и запланированных книг, но и отслеживать прогресс, оставлять отзывы, формировать цели на месяц или год, а также анализировать свои привычки с помощью наглядной статистики.
          </div>
          <div class="about-buttons">
            <RouterLink class="light-button" to="/auth/login/">Начать сейчас!</RouterLink>
            <RouterLink class="light-button" to="/books">В каталог</RouterLink>
          </div>
      </div>
    </section>

    <section class="popular-section">
      <h2>Популярные книги</h2>
      <div class="popular-books">
        <Swiper
          :modules="swiperModules"
          :slides-per-view="5.5"
          :space-between="20"
          :slides-per-group="5"
          :navigation="true"
          :pagination="{ clickable: true }"
        >
          <SwiperSlide v-for="book in popularBooks" :key="book.id">
            <BookCard :book="book" />
          </SwiperSlide>
        </Swiper>
      </div>
  </section>

  </main>
</template>

<style scoped>

.welcome-section {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
  height: 80vh;
}
main {
  gap: 80px
}
h1 {
  font-size: 5.5vh;
}
.welcome-header {
  width: 28vw;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.welcome-header small {
  font-size: 20px;
  font-size: 2vh;
}
.company-name {
  font-size: 60px;
  font-size: 8vh;
}
.about-section {
  background-color: #122930;
  border-radius: 12px;
  min-height: 200px;
  width: 100%;
  position: relative;
  overflow: hidden;
  padding: 60px 80px;
}
.about-bg-img {
  position: absolute;
  right: 0;
  top: 0;
  max-height: 100%;
  max-width: 40%;
  width: 100%;
  object-fit: contain;
}
.about-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: white;
  max-width: 60%;
  line-height: 1.8rem;
}
.about-content h2 {
  font-size: 36px;
}
.about-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.book-card {
  width: 100%;
}
.popular-section h2 {
  font-size: 32px;
}
.swiper-pagination-bullet .swiper-pagination-bullet-active {
  background: var(--dark-color) !important;
}
.swiper-button-next:after {
  background: white;
  height: 80px;
  width: 80px;
  content: 'next';
  color: black;
  display: flex;
  align-items: center;
  justify-content: center;
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