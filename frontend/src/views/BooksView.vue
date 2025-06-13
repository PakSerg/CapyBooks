<script>
import BookCard from '@/components/BookCard.vue'
import axios from 'axios'

export default {
  name: 'BooksView',
  components: {
    BookCard
  },
  data() {
    return {
      books: [],
      userBooks: [],
      genres: [],
      loading: false,
      error: null
    }
  },
  methods: {
    async fetchBooks() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:8000/books')
        this.books = response.data.books;
        this.userBooks = response.data.user_books || [];
        console.log(response.data)
      } catch (error) {
        this.error = 'Ошибка при загрузке книг'
        console.error('Ошибка при загрузке книг:', error)
      } finally {
        this.loading = false
      }
    }, 
    async fetchGenres() {
      try {
        const response = await axios.get('http://localhost:8000/books/genres')
        this.genres = response.data.genres;
      } catch (error) {
        console.error('Ошибка при загрузке жанров')
      }
    },
    handleBookAdded(bookId) {
      this.userBooks.push(bookId);
    },
    handleBookRemoved(bookId) {
      const index = this.userBooks.indexOf(bookId);
      if (index > -1) {
        this.userBooks.splice(index, 1);
      }
    }
  },
  mounted() {
    this.fetchBooks();
    this.fetchGenres();
  }
}
</script>

<template>
  

  <main>
    <section class="container catalog">
      <h1 class="font-special">Каталог</h1>
      <div class="catalog-content">
        <div class="sidebar">
          <p 
            class="font-special"
            v-for="genre in genres" 
            :key="genre.id"
          >
            {{ genre.name }}
          </p>
        </div>
        <div class="main-container">
          <div v-if="error" class="error">
            {{ error }}
          </div>
          <div v-if="loading" class="loader">
          </div>
          <div v-else class="books-cards">
            <BookCard
              v-for="book in books"
              :key="book.id"
              :book="book"
              :is-in-user-list="userBooks.includes(book.id)"
              @book-added="handleBookAdded"
              @book-removed="handleBookRemoved"
            />
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
.catalog {
    display: flex;
    flex-direction: column;
    gap: 40px;
}
.catalog-content {
    display: flex;
    gap: 16px;
    justify-content: space-between;
}
.sidebar {
    display: flex;
    flex-direction: column;
    gap: 20px;
    min-width: 200px;
    width: 240px;
    position: sticky;
    top: 140px; 
    height: fit-content;
    align-self: flex-start;
}
.main-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    flex: 1
}
.books-cards {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}
.loading, .error {
    text-align: center;
    padding: 20px;
    font-size: 1.2em;
}
.error {
    color: #ff4444;
}
</style>
