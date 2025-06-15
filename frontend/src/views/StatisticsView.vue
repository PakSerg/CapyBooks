<script>
import axios from 'axios'

export default {
  name: 'UserStatisticsView',
  data() {
    return {
      loading: false,
      error: null,
      topAuthors: [],
      topGenres: [],
      topMonth: null,
    }
  },
  methods: {
    async fetchStatistics() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.get('http://5.129.207.86/api/reading-list/statistics/');
        this.topAuthors = response.data.top_authors || [];
        this.topGenres = response.data.top_genres || [];
        this.topMonth = response.data.top_month || null;
      } catch (error) {
        this.error = 'Ошибка при загрузке статистики';
        console.error('Ошибка при загрузке статистики:', error);
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    this.fetchStatistics();
  }
}
</script>

<template>
  <main class="container">
    <section class="statistics-section">
        <h1 class="font-special">Статистика пользователя</h1>

        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="loading" class="loader"></div>

        <div v-if="!loading && !error">
        <section class="stat-section">
            <h2>Топ 3 любимых автора</h2>
            <ul v-if="topAuthors.length">
            <li v-for="author in topAuthors" :key="author.id">
                {{ author.author_name }} — книг прочитано: {{ author.books_count }}
            </li>
            </ul>
            <p v-else>Нет данных</p>
        </section>

        <section class="stat-section">
            <h2>Топ 3 любимых жанра</h2>
            <ul v-if="topGenres.length">
            <li v-for="genre in topGenres" :key="genre.id">
                {{ genre.genre_name }} — книг прочитано: {{ genre.books_count }}
            </li>
            </ul>
            <p v-else>Нет данных</p>
        </section>
        </div>
    </section>
  </main>
</template>

<style scoped>
.container.statistics {
  max-width: 600px;
  margin: 40px auto;
  font-family: Arial, sans-serif;
}
.font-special {
  font-weight: 700;
  margin-bottom: 20px;
}
.stat-section {
  margin-bottom: 30px;
}
.error {
  color: #ff4444;
  text-align: center;
  margin-bottom: 20px;
}
.loader {
  text-align: center;
  margin: 40px 0;
  font-size: 1.2em;
}
ul {
  padding-left: 20px;
}
li {
  margin-bottom: 8px;
}
.statistics-section {
    display: flex;
    flex-direction: column;
    gap: 80px;
    height: 90vh;
}
h2 {
    font-size: 32px;
}
</style>
