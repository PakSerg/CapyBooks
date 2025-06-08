<script>
import { RouterLink, RouterView } from 'vue-router'


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
                <RouterLink class="font-special" to="/reading-list">Список чтения</RouterLink>
                <RouterLink class="font-special" to="/about">Статистика</RouterLink>
                <RouterLink class="font-special" to="/about">Вход</RouterLink>
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
}
header .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    gap: 40px;
    padding: 12px 0px;
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
</style>