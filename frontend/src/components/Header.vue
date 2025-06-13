<script>
import { RouterLink } from 'vue-router'
import AuthService from '@/services/AuthService'

export default {
  data() {
    return {
      isAuthenticated: false,
      username: '',
      scrollIntervalId: null,
      lastScrollTop: 0,
      didScroll: false,
      SCROLL_DELTA: 5,
      SCROLL_CHECK_INTERVAL: 150
    }
  },
  methods: {
    async logout() {
      await AuthService.logout()
      this.updateAuthState()
      console.log('Вышел')
    },
    updateAuthState() {
      this.isAuthenticated = AuthService.isAuthenticated()
      this.username = AuthService.getUsername()
    },
    handleScroll() {
      const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop
      const header = document.querySelector('header')
      const filtersSectionVisible = document.querySelector('.filtersSection.visible')
      const navbarNav = document.getElementById('navbarNav')
      const mobileMenu = document.querySelector('.mobile-menu')
      const dropdown = document.querySelector('.header-dropdown-choices')
      const burger = document.querySelector('.burger-container img')
      const navbarHeight = header?.offsetHeight || 96

      if (filtersSectionVisible) {
        header.classList.remove('nav-up')
        header.classList.add('nav-down')
        return
      }

      if (Math.abs(this.lastScrollTop - currentScrollTop) <= this.SCROLL_DELTA) {
        return
      }

      if (this.lastScrollTop < currentScrollTop && currentScrollTop > navbarHeight) {
        header.classList.remove('nav-down')
        header.classList.add('nav-up')

        dropdown?.classList.remove('visible')
        if (mobileMenu?.classList.contains('active')) {
          mobileMenu.classList.remove('active')
          if (burger) burger.src = '/static/images/burger.svg'
        }

        navbarNav?.classList.remove('show')
      } else if (currentScrollTop + window.innerHeight < document.body.scrollHeight) {
        header.classList.remove('nav-up')
        header.classList.add('nav-down')
      }

      this.lastScrollTop = currentScrollTop
    }
  },
  mounted() {
    this.updateAuthState()
    window.addEventListener('auth-state-changed', this.updateAuthState)

    window.addEventListener('scroll', () => {
      this.didScroll = true
    })

    this.scrollIntervalId = setInterval(() => {
      if (this.didScroll) {
        this.handleScroll()
        this.didScroll = false
      }
    }, this.SCROLL_CHECK_INTERVAL)
  },
  beforeUnmount() {
    window.removeEventListener('auth-state-changed', this.updateAuthState)
    clearInterval(this.scrollIntervalId)
  }
}
</script>

<template>
<header class="header">
    <div class="container">
        <div class="left-part">
            <div class="header-logo">
                <div class="header-logo-wrapper">
                    <RouterLink to="/">
                        <img src="/logo.png" alt="Логотип">
                    </RouterLink>
                </div>
                <RouterLink to="/" class="header-logo-label font-special">CapyBooks</RouterLink>
            </div>
        </div>
        <div class="right-part">
            <nav>
                <RouterLink class="font-special" to="/">Главная</RouterLink>
                <RouterLink class="font-special" to="/books">Книги</RouterLink>
                <RouterLink v-if="isAuthenticated" class="font-special" to="/reading-list">Список чтения</RouterLink>
                <RouterLink v-if="isAuthenticated" class="font-special" to="/about">Статистика</RouterLink>
                <RouterLink v-if="!isAuthenticated" class="font-special" to="/auth/register">Регистрация</RouterLink>
                <RouterLink v-if="!isAuthenticated" class="font-special" to="/auth/login">Вход</RouterLink>
                <div v-if="isAuthenticated" class="logout-button" @click="logout">
                    <img src="/logout-icon.svg" alt="">
                </div>
            </nav>
        </div>
    </div>
</header>
</template>

<style scoped>
header {
    height: 96px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000; 
    background-color: white;

    transition: transform 0.3s ease;
}
header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    gap: 40px;
    background-color: white;
    padding: 12px 0px;
}

header.nav-up {
    transform: translateY(-100%);
}
header.nav-down {
    transform: translateY(0);
}

header .left-part {
    display: flex;
    align-items: center;
    gap: 20px;
}
header .right-part nav {
    display: flex;
    align-items: center;
    gap: 26px;
}
header .right-part nav a {
    color: var(--dark-color);
    font-size: 18px;
    font-weight: 500;
    position: relative;
    transition: all 0.3s ease;
}

header .right-part nav a.router-link-active {
    color: var(--accent-color);
}

header .right-part nav a.router-link-active::after {
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--dark-color);
    border-radius: 2px;
    animation: underline 0.3s ease forwards;
}

@keyframes underline {
    from {
        transform: scaleX(0);
        transform-origin: left;
    }
    to {
        transform: scaleX(1);
        transform-origin: left;
    }
}

.header-logo-wrapper {
    overflow: hidden;
    width: 64px;
    border-radius: 30px;

    transition: all 0.3s ease;
}
.header-logo-wrapper a {
    display: flex;
    gap: 10px;
}
.header-logo {
    display: flex;
    gap: 14px;
    align-items: center;
}
.header-logo-label {
    font-size: 28px;
}
.header-logo-wrapper:hover {
    opacity: 0.9;
}
.header-logo-wrapper
.header-logo-wrapper img {
    object-fit: cover;
}
.logout-button {
    transition: all 0.3s ease;
    padding: 12px;
    border-radius: 100px;
    cursor: pointer;
}
.logout-button:hover {
    background-color: rgb(29, 30, 31, 0.1);
}
</style>