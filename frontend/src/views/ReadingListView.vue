<script>
import axios from 'axios'

export default {
  data() {
    return {
      userBooks: [],
      loading: false,
      error: null
    }
  },
  methods: {
    async fetchUserBooks() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:8000/reading-list');
        this.userBooks = response.data.books;
        console.log(response.data)
      } catch (error) {
        this.error = 'Ошибка при загрузке книг'
        console.error('Ошибка при загрузке книг:', error)
      } finally {
        this.loading = false
      }
    },
    async handleDelete(bookId) {
      try {
        await axios.post('http://localhost:8000/reading-list/delete-book/', {
          book_id: bookId
        });
        this.userBooks = this.userBooks.filter(book => book.id !== bookId);
        console.log('Книга удалена из списка чтения');
      } catch (error) {
        console.error('Ошибка при удалении книги:', error);
      }
    }
  },
  mounted() {
    this.fetchUserBooks();
  }
}
</script>

<template>
  <main>
    <section class="container">
      <h1 class="font-special">Список чтения</h1>
      <div class="reading-list-container">
        <div v-if="loading" class="loader"></div>
        <div v-else-if="error" class="error">
          {{ error }}
        </div>
        <div v-else-if="userBooks.length === 0" class="empty-list">
          Список чтения пуст
        </div>
        <div v-else v-for="book in userBooks" :key="book.id" class="book-row">
          <div class="book-img-wrapper">
            <img 
              :src="book.image || '/book-default.png'" 
              :alt="book.name"
              class="book-row-cover"
            >
          </div>
          <p class="book-name">{{ book.name }}</p>
          <p class="book-description">{{ book.description }}</p>
          <p class="book-author">{{ book.author.name }}</p>
          <p class="book-year">{{ book.year }} г.</p>
          <button class="delete-button" @click="handleDelete(book.id)">
            <img src="/delete-icon.svg" alt="">
          </button>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.reading-list-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.book-row {
  display: flex;
  gap: 20px;
  align-items: center;
}
.book-row-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  max-width: 70px;
}
.book-name {
  font-size: 20px;
  font-weight: 500;
  max-width: 300px;
  min-width: 300px;
  width: 100%;
}
.book-author {
  max-width: 220px;
  width: 100%;
  text-align: center;
  min-width: 220px;
}
.book-img-wrapper {
  max-height: 120px;
  height: 110px;
  overflow: hidden;
  max-width: 70px;
  width: 100%;
  border-radius: 8px;
}
.delete-button {
  transition: all 0.3s ease;
  padding: 12px;
  border-radius: 100px;
  cursor: pointer;
  min-width: 50px;
}
.delete-button:hover {
  background-color: rgb(29, 30, 31, 0.1);
}
.book-description {
    font-size: 14px;
    color: var(--pale-color);
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    max-height: 4.2em; 
}
.book-year {
  min-width: 56px;
}
.loading, .error, .empty-list {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
}
.error {
  color: #ff4444;
}
.empty-list {
  color: var(--pale-color);
}
</style>
