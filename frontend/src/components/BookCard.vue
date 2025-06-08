<script>
import axios from 'axios'

export default {
  name: 'BookCard',
  props: {
    book: {
      type: Object,
      required: true
    }
  },
  methods: {
    async handleAddToCart() {
      try {
        await axios.post('http://localhost:8000/reading-list/add-book/', {
          book_id: this.book.id
        });
        console.log('Книга добавлена в список для чтения:', this.book.name);
      } catch (error) {
        console.error('Ошибка при добавлении книги в список для чтения:', error);
      }
    },
  }
}
</script>

<template>
  <div class="book-card">
    <a class="book-image">
      <img 
        :src="book.image || '/book-default.png'" 
        :alt="book.name"
        class="book-cover"
      >
    </a>
    <div class="book-info">
      <div class="book-upper">
        <div class="book-header">
          <h3 class="book-title font-special">{{ book.name }}</h3>
          <p class="book-author font-special">{{ book.author.name }}</p>
        </div>

        <div class="book-meta">
          <span class="book-year">{{ book.year }}</span>
          <span>•</span>
          <span class="book-pages">{{ book.pages_count }} стр.</span>
          <span>•</span>
          <span 
            v-for="genre in book.genres" 
            :key="genre.id" 
            class="genre-tag"
          >
            {{ genre.name }}
          </span>
        </div>
      </div>
      <div class="book-actions">
        <button @click="handleAddToCart" class="add-book">
          Добавить
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-card {
    width: 280px;
    width: calc((100% - 20px * 3) / 4);
    background: #fff;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s ease;
    display: flex;
    flex-direction: column;
}

.book-image {
    display: block;
    width: 100%;
    height: 320px;
    overflow: hidden;
}

.book-cover {
    width: 100%;
    height: 100%;
    object-fit: cover;
}


.book-info {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    font-family: var(--font-special), sans-serif;
    flex: 1;
    justify-content: space-between;
}
.book-upper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.book-meta {
    display: flex;
    flex-wrap: wrap;
    column-gap: 4px;
    row-gap: 6px;
    font-size: 13px;
}
.book-header {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.book-title {
    font-size: 16px;
    font-weight: 600;
}
.book-author {
    font-size: 14px;
    color: var(--pale-color)
}
.add-book {
    background-color: var(--dark-color);
    border-radius: 12px;
    padding: 10px 28px;
    font-size: 14px;
    color: white;
    transition: all 0.3s ease;
}
.add-book:hover {
    background-color: var(--pale-color);
}
.book-actions {
    display: flex;
}
</style>