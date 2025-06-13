<script>
import axios from 'axios';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/thumbs';
import { Thumbs } from 'swiper/modules';
import { Fancybox } from "@fancyapps/ui";
import "@fancyapps/ui/dist/fancybox/fancybox.css";
import BookCard from '@/components/BookCard.vue';


export default {
  name: 'BookView',
  components: {
    Swiper,
    SwiperSlide,
    BookCard,
  },
  data() {
    return {
      book: null,
      recommended: [],
      isInUserList: null,
      loading: true,
      error: null,
      userBooks: [],
      mainSwiper: null, 
      thumbsSwiper: null,
      modules: [Thumbs]
    };
  },
  methods: {
    onSwiper(swiper) {
      console.log('Основной Swiper:', swiper);
      this.mainSwiper = swiper;
    },
    onSlideChange() {
      console.log('Слайд сменился');
    },
    setThumbsSwiper(swiper) {
      this.thumbsSwiper = swiper;
    },
    async handleAddToCart() {
      if (this.isInUserList) {
        await this.removeFromList();
        return;
      }

      this.isInUserList = true;
      try {
        await axios.post('http://localhost:8000/reading-list/add-book/', {
          book_id: this.book.id
        });
        console.log('Книга добавлена в список для чтения:', this.book.name);
        this.$emit('book-added', this.book.id);
      } catch (error) {
        console.error('Ошибка при добавлении книги:', error);
      }
    },
    async removeFromList() {
      try {
        await axios.post('http://localhost:8000/reading-list/delete-book/', {
          book_id: this.book.id
        });
        console.log('Книга удалена из списка для чтения:', this.book.name);
        this.$emit('book-removed', this.book.id);
        this.isInUserList = false;
      } catch (error) {
        console.error('Ошибка при удалении книги:', error);
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
  async created() {
    try {
      console.log('Загрузка книги со слагом:', this.$route.params.slug);
      const response = await axios.get(`http://localhost:8000/books/${this.$route.params.slug}/`);
      this.book = response.data.book;
      this.isInUserList = response.data.is_in_user_list;
      this.recommended = response.data.recommended || [];
      this.userBooks = response.data.user_books || [];
      console.log(this.recommended)
    } catch (error) {
      console.error('Ошибка загрузки:', error);
      this.error = 'Ошибка при загрузке книги';
    } finally {
      this.loading = false;
    }
  }, 
  mounted() {
    Fancybox.bind('[data-fancybox="gallery"]', {
    Thumbs: true,
    Toolbar: true, 
    on: {
      "Carousel.change": (fancybox, carousel, slideIndex) => {
        if (this.mainSwiper) {
          this.mainSwiper.slideTo(slideIndex);
        }
      }
    }
  });
  }
};
</script>


<template>
    <main>
        <div v-if="loading" class="loading">
            Загрузка...
        </div>
        <div v-else-if="error" class="error">
            {{ error }}
        </div>
        <div v-else class="book-content">
            <div class="book-details">
                <div class="book-left">
                    <!-- Основной слайдер -->
                    <swiper
                        :slides-per-view="1"
                        :space-between="0"
                        :centered-slides="1"
                        :thumbs="{ swiper: thumbsSwiper }"
                        :modules="modules"
                        class="main-slider"
                        @swiper="onSwiper"
                        @slideChange="onSlideChange"
                    >
                    <swiper-slide>
                        <a :href="book?.image || '/book-default.png'" data-fancybox="gallery">
                            <img :src="book?.image || '/book-default.png'" :alt="book?.slug" class="book-cover book-slide" />
                        </a>
                        </swiper-slide>

                        <swiper-slide v-for="(photo, index) in book.photos" :key="index">
                        <a :href="photo" data-fancybox="gallery">
                            <img :src="photo" :alt="book?.slug" class="book-cover book-slide" />
                        </a>
                        </swiper-slide>
                    </swiper>

                    <!-- Миниатюры -->
                    <swiper
                        @swiper="setThumbsSwiper"
                        :spaceBetween="10"
                        :slidesPerView="4.5"
                        :freeMode="true"
                        :watchSlidesProgress="true"
                        :modules="modules"
                        class="mini-slider"
                    >
                        <swiper-slide>
                            <img :src="book?.image || '/book-default.png'" :alt="book?.slug" class="book-cover book-slide">
                        </swiper-slide>
                        <swiper-slide v-for="photo in book.photos">
                            <img :src="photo" :alt="book?.slug" class="book-cover book-slide">
                        </swiper-slide>
                    </swiper>
                </div>
                <div class="book-info">
                    <h1>{{ book.name }}</h1>
                    <p class="author">Автор: {{ book?.author?.name }}</p>
                    <p class="year">Год: {{ book?.year }}</p>
                    <p class="pages">Страниц: {{ book?.pages_count }}</p>
                    <p class="description font-usual">Описание: {{ book?.description }}</p>
                    <div class="genres">
                        <span>Жанры: </span>
                        <span v-for="(genre, index) in book?.genres" :key="genre.id" class="genre-tag">
                            {{ genre.name }}{{ index < book.genres.length - 1 ? ',' : '' }} </span>
                    </div>
                    <div class="buttons-row">
                        <button 
                            class="dark-button"
                            @click="handleAddToCart" 
                            :class="{ 
                                'passive': isInUserList, 
                            }"
                        >
                        {{ isInUserList ? 'В списке' : 'Добавить' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <section class="recommended-section" v-if="recommended.length > 0">
            <h2 class="font-usual">Похожие книги</h2>
            
            <div class="books-cards">
                <BookCard
                v-for="book in recommended.slice(0, 6)"
                :key="book.id"
                :book="book"
                :is-in-user-list="userBooks.includes(book.id)"
                @book-added="handleBookAdded"
                @book-removed="handleBookRemoved"
                />
          </div>
        </section>

    </main>
</template>

<style scoped>

.loading,
.error {
    text-align: center;
    padding: 20px;
}

.error {
    color: red;
}

.book-content {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.book-details {
    display: flex;
    gap: 40px;
}

.book-cover {
    width: 300px;
    height: 450px;
    object-fit: cover;
    border-radius: 8px;
}

.book-info {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.genres {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}

.book-content * {
    font-family: var(--font-usual), sans-serif;
}
h2 {
    font-size: 28px;
}
.buttons-row {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}
.book-left {
    min-width: 300px;
    display: flex;
    flex-direction: column;
    gap: 16px;

    width: 100%;
}

.main-slider,
.mini-slider {
    width: 100%;
}

.mini-slider .swiper-slide{
    height: 72px;
    object-fit: cover;
}
.mini-slider .swiper-slide img {
    max-height: 100%;
    object-fit: cover;
}
.main-slider .swiper-slide,
.mini-slider .swiper-slide {
    cursor: pointer;
    transition: all 0.3s ease;
}
.mini-slider .swiper-slide {
    border: 1px solid rgb(0, 30, 34, 0.1);
    border-radius: 6px;
}
.mini-slider .swiper-slide:hover {
    border: 1px solid var(--dark-color);
}
.mini-slider .swiper-slide-thumb-active {
    border: 1px solid var(--dark-color);
}

.books-cards .book-card {
    width: calc((100% - 12px * 5) / 6);
}
main {
    gap: 50px
}
h2 {
    font-size: 32px;
}
.recommended-section {
    gap: 20px;
}
</style>