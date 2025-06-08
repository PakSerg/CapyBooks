<script>
import BookCard from '@/components/BookCard.vue'

export default {
  name: 'BooksView',
  components: {
    BookCard
  },
  data() {
    return {
      books: [
        {
          id: 1,
          name: "Евгений Онегин",
          author: {
            id: 1,
            name: "Пушкин Александр Сергеевич"
          },
          image: null,
          pages_count: 200,
          year: 1831,
          description: "Роман в стихах \"Евгений Онегин\" - самое известное и самое значительное произведение А. С. Пушкина...",
          genres: [
            {
              id: 1,
              name: "Роман в стихах"
            }
          ],
          slug: "evgenij-onegin"
        }
      ]
    }
  }
}
</script>

<template>
  <main>
    <section class="container catalog">
      <h1 class="font-special">Каталог</h1>
      <div class="catalog-content">
        <div class="sidebar">
          <!-- Здесь будет фильтр -->
        </div>
        <div class="main-container">
          <div class="books-cards">
            <BookCard
              v-for="book in books"
              :key="book.id"
              :book="book"
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
    gap: 20px;
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
    width: 200px;
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
</style>
