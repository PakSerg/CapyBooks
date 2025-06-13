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
      error: null,
      selectedGenre: null,
      currentPage: 1,
      totalPages: 1,
      pageSize: 15, 
    }
  },
  methods: {
    async fetchBooks() {
      this.loading = true;
      this.error = null;

      try {
        const params = {
          page: this.currentPage,
          page_size: this.pageSize
        };

        if (this.selectedGenre) {
          params.category = this.selectedGenre;
        }

        const response = await axios.get('http://localhost:8000/books', { params });

        this.books = response.data.books;
        this.userBooks = response.data.user_books || [];
        this.totalPages = response.data.pagination.total_pages;

      } catch (error) {
        this.error = 'Ошибка при загрузке книг';
        console.error('Ошибка при загрузке книг:', error);
      } finally {
        this.loading = false;
      }
    }, 
    async fetchGenres() {
      try {
        const response = await axios.get('http://localhost:8000/books/genres');
        this.genres = response.data.genres;
      } catch (error) {
        console.error('Ошибка при загрузке жанров');
      }
    },
    handleBookAdded(bookId) {
      if (!this.userBooks.includes(bookId)) {
        this.userBooks.push(bookId);
      }
    },
    handleBookRemoved(bookId) {
      const index = this.userBooks.indexOf(bookId);
      if (index > -1) {
        this.userBooks.splice(index, 1);
      }
    },
    selectGenre(genreId) {
      this.selectedGenre = genreId;
      this.currentPage = 1;
      this.fetchBooks();
    },
    goToPage(page) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
        this.fetchBooks();
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
            class="font-special category-filter"
            v-for="genre in genres"
            :key="genre.id"
            :class="{ active: selectedGenre === genre.id }"
            @click="selectGenre(genre.id)"
          >
            {{ genre.name }}
          </p>
          <p class="font-special category-filter dark-button" @click="selectGenre(null)">
            Сбросить фильтры
          </p>
        </div>

        <div class="main-container">
          <div v-if="error" class="error">
            {{ error }}
          </div>

          <div v-if="loading" class="loader"></div>

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

          <div class="pagination" v-if="totalPages > 1">
            <button class="dark-button" @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">Назад</button>
            <span>Страница {{ currentPage }} из {{ totalPages }}</span>
            <button class="dark-button" @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">Вперёд</button>
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
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
.category-filter {
  cursor: pointer;

  transition: all 0.3s ease;
}
.category-filter.active {
  text-decoration: underline;
}
.category-filter.dark-button {
  width: fit-content;
  margin-top: 20px;
}
</style>
