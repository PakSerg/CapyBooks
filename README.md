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
- **Тело запроса**:
  ```json
  {
    "book_id": "integer"  // ID книги для добавления
  }
  ```

### Обновление информации о книге в списке
- **POST** `/reading-list/update-book/`
- **Тело запроса**:
  ```json
  {
    "book_id": "integer",     // ID книги (обязательный параметр)
    "status_id": "integer",   // ID статуса книги (опционально)
    "notes": "string",        // Заметки о книге (опционально)
    "start_date": "YYYY-MM-DD", // Дата начала чтения (опционально)
    "end_date": "YYYY-MM-DD",   // Дата окончания чтения (опционально)
    "rating": "number"        // Рейтинг книги от 0 до 10 (опционально)
  }
  ```

### Удаление книги из списка
- **POST** `/reading-list/delete-book/`
- **Тело запроса**:
  ```json
  {
    "book_id": "integer"  // ID книги для удаления
  }
  ```
