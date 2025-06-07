# CapyBooks
Трекер прочитанных книг на Django + Vue.js

# CapyBooks API

## Аутентификация

### Регистрация
- **POST** `/users/auth/register/`
- **Тело запроса**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### Вход
- **POST** `/users/auth/login/`
- **Тело запроса**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

## Книги

### Получение каталога книг
- **GET** `/books/`

### Получение информации о книге
- **GET** `/books/<slug>/`

## Списки для чтения

### Получение списка книг пользователя
- **GET** `/reading-list/`

### Добавление книги в список
- **POST** `/reading-list/add-book`

### Обновление информации о книге в списке
- **POST** `/reading-list/update-book/`

### Удаление книги из списка
- **POST** `/reading-list/delete-book/`
