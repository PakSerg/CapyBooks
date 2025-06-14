<script>
import Header from './components/Header.vue'
import { RouterView } from 'vue-router'

export default {
  components: {
    Header
  }
}
</script>

<template>
  <Header />
  <RouterView v-slot="{ Component, route }" >
    <transition name="page" mode="out-in" :key="route.path">
      <component :is="Component" />
    </transition>
  </RouterView>

  <footer>
    <div class="footer-left">
      <img class="footer-logo" src="/logo.png" alt="">
      <p>CapyBooks</p>
    </div>
    <span>Все права защищены</span>
  </footer>
</template>

<style>
@import './assets/main.css';

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0;
  font-weight: normal;
}

.page-enter-active,
.page-leave-active {
  transition: all 0.1s;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
}

footer {
  display: flex;
  justify-content: space-between;
  height: 100px;
}
.footer-logo {
  border-radius: 100px;
  width: 40px;
  height: 40px;
  object-fit: contain;
}
.footer-left {
  display: flex;
  gap: 12px;
  height: 20px;
  align-items: center;
}
</style>
