<script>
import axios from 'axios'

export default {
  name: 'BookCard',
  props: {
    book: {
      type: Object,
      required: true
    },
    isInUserList: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    async handleAddToCart() {
      if (this.isInUserList) {
        await this.removeFromList();
        return;
      }
      
      this.isAdding = true;
      try {
        await axios.post('http://localhost:8000/reading-list/add-book/', {
          book_id: this.book.id
        });
        console.log('Книга добавлена в список для чтения:', this.book.name);
        this.$emit('book-added', this.book.id);
      } catch (error) {
        console.error('Ошибка при добавлении книги в список для чтения:', error);
      } finally {
        this.isAdding = false;
      }
    },
    async removeFromList() {
      try {
        await axios.post('http://localhost:8000/reading-list/delete-book/', {
          book_id: this.book.id
        });
        console.log('Книга удалена из списка для чтения:', this.book.name);
        this.$emit('book-removed', this.book.id);
      } catch (error) {
        console.error('Ошибка при удалении книги из списка для чтения:', error);
      } finally {
        this.isRemoving = false;
      }
    }
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
        <button 
          @click="handleAddToCart" 
          class="add-book"
          :class="{ 
            'in-list': isInUserList, 
          }"
          :disabled="isAdding || isRemoving"
        >
        {{ isInUserList ? 'В списке' : 'Добавить' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-card {
    width: 280px;
    width: calc((100% - 12px * 4) / 5);
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
    width: 100%;
}
.add-book:hover:not(:disabled) {
    background-color: var(--pale-color);
}
.add-book:disabled {
    cursor: default;
    opacity: 0.7;
}
.add-book.in-list {
  background-color: #686a6b;
}
.add-book.in-list:hover {
    background-color: var(--pale-color);
}
.add-book.adding,
.add-book.removing {
    background-color: var(--pale-color);
    cursor: wait;
}
.book-actions {
    display: flex;
}
</style>