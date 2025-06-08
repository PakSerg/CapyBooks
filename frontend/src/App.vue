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
  <RouterView v-slot="{ Component }">
    <transition name="page" mode="out-in">
      <component :is="Component" />
    </transition>
  </RouterView>
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
</style>
