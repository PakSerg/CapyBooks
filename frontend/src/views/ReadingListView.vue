<script>
import axios from 'axios'

export default {
	data() {
		return {
			userBooks: [],
			loading: false,
			error: null,
			statuses: [],

			lastWeekBooks: [],
			lastMonthBooks: [],
			lastYearBooks: [],
			olderBooks: [],
			userBooksSections: [],
		}
	},
	methods: {
		async fetchUserBooks() {
			this.loading = true
			try {
				const response = await axios.get('http://5.129.207.86/api/reading-list/');
				this.userBooks = response.data.all_books;
				console.log(response.data);

				this.lastWeekBooks = response.data.last_week;
				this.lastMonthBooks = response.data.last_month;
				this.lastYearBooks = response.data.last_year;
				this.olderBooks = response.data.older;
				this.userBooksSections = [
					this.lastWeekBooks, 
					this.lastMonthBooks, 
					this.lastYearBooks, 
					this.olderBooks
				].filter(books => books && books.length > 0);
				console.log(this.userBooksSections)

			} catch (error) {
				this.error = 'Ошибка при загрузке книг'
				console.error('Ошибка при загрузке книг:', error)
			} finally {
				this.loading = false
			}
		},
		async fetchStatuses() {
			try {
				const response = await axios.get('http://5.129.207.86/api/reading-list/statuses/');
				this.statuses = response.data.statuses;
				console.log('Полученные статусы:', this.statuses);
			} catch (error) {
				console.error('Ошибка при загрузке статусов:', error);
			}
		},
		async handleDelete(bookId) {
			try {
				await axios.post('http://5.129.207.86/api/reading-list/delete-book/', {
					book_id: bookId
				});
				this.userBooks = this.userBooks.filter(book => book.id !== bookId);

				this.userBooksSections = this.userBooksSections.map(section =>
					section.filter(book => book.id !== bookId)
				).filter(section => section.length > 0);

				console.log('Книга удалена из списка чтения');
			} catch (error) {
				console.error('Ошибка при удалении книги:', error);
			}
		},
		async updateBookStatus(bookId, statusId) {
			try {
				await axios.post('http://5.129.207.86/api/reading-list/update-book/', {
					book_id: bookId,
					status_id: statusId
				});
				let book = null;

				this.userBooksSections.forEach((section) => {
					section.forEach((b) => {
						if (b.id == bookId) {
							book = b;
						}
					});
				});

				book.isDropdownOpen = false;
				if (book) {
					const foundStatus = this.statuses.find(s => s.id === statusId);
					book.status.id = statusId;
					book.status.name = foundStatus.name;
				}
			} catch (error) {
				console.error('Ошибка при обновлении статуса:', error);
			}
		},
		toggleDropdown(bookId) {
			console.log(`нажатие на дропдаун ${bookId}`)
			const book = this.userBooks.find(b => b.id === bookId);
			console.log(book)
			if (book) {
				book.isDropdownOpen = !book.isDropdownOpen;
			}
			this.userBooksSections.forEach((section) => {
				section.forEach((book) => {
					if (book.id == bookId) {
						book.isDropdownOpen = !book.isDropdownOpen;
					}
				});
			});
		},
		closeDropdowns() {
			this.userBooksSections.forEach((section) => {
				section.forEach((book) => {
					if (book.id == bookId) {
						book.isDropdownOpen = false;
					}
				});
			});
		}
	},
	async mounted() {
		await Promise.all([
			this.fetchUserBooks(),
			this.fetchStatuses()
		]);
		document.addEventListener('click', this.closeDropdowns);
	},
	beforeUnmount() {
		document.removeEventListener('click', this.closeDropdowns);
	}
}
</script>

<template>
	<main>
		<section class="container">
			<h1 class="font-special">Ваш список чтения</h1>
			<div class="reading-list-container">
				<div v-if="loading" class="loader"></div>
				<div v-else-if="error" class="error">
					{{ error }}
				</div>
				<div v-else-if="userBooks.length === 0" class="empty-list">
					Список чтения пуст
				</div>
				<div v-else>
					<div class="userbooks-section" v-for="section in userBooksSections">
						<h2>За последнюю неделю</h2>
						<div v-for="book in section" :key="book.id" class="book-row">
							<div class="book-img-wrapper">
								<img :src="book.image || '/book-default.png'" :alt="book.name" class="book-row-cover">
							</div>
							<p class="book-name">{{ book.name }}</p>
							<p class="book-description">{{ book.description }}</p>
							<p class="book-author">{{ book.author.name }}</p>
							<p class="book-year">{{ book.year }} г.</p>
							<div class="status-dropdown" @click.stop>
								<button class="status-button" @click="toggleDropdown(book.id)" :class="book.status">
									{{statuses.find(s => s.id === book.status.id)?.name || 'Выбрать статус'}}
								</button>
								<div v-if="book.isDropdownOpen" class="dropdown-menu">
									<button v-for="status in statuses" :key="status.id"
										@click="updateBookStatus(book.id, status.id)"
										:class="{ active: book.status.id === status.id }">
										{{ status.name }}
									</button>
								</div>
							</div>
							<button class="delete-button" @click="handleDelete(book.id)">
								<img src="/delete-icon.svg" alt="">
							</button>
						</div>
					</div>
				</div>
			</div>
		</section>
	</main>
</template>

<style scoped>
.reading-list-container {
	display: flex;
	flex-direction: column;
	gap: 20px;
}

.book-row {
	display: flex;
	gap: 20px;
	align-items: center;
}

.book-row-cover {
	width: 100%;
	height: 100%;
	object-fit: cover;
	max-width: 70px;
}

.book-name {
	font-size: 20px;
	font-weight: 500;
	max-width: 300px;
	min-width: 300px;
	width: 100%;
}

.book-author {
	max-width: 220px;
	width: 100%;
	text-align: center;
	min-width: 220px;
}

.book-img-wrapper {
	max-height: 120px;
	height: 110px;
	overflow: hidden;
	max-width: 70px;
	width: 100%;
	border-radius: 8px;
}

.delete-button {
	transition: all 0.3s ease;
	padding: 12px;
	border-radius: 100px;
	cursor: pointer;
	min-width: 50px;
}

.delete-button:hover {
	background-color: rgb(29, 30, 31, 0.1);
}

.book-description {
	font-size: 14px;
	color: var(--pale-color);
	line-height: 1.4;
	display: -webkit-box;
	-webkit-line-clamp: 3;
	-webkit-box-orient: vertical;
	overflow: hidden;
	text-overflow: ellipsis;
	max-height: 4.2em;
}

.book-year {
	min-width: 56px;
}

.loading,
.error,
.empty-list {
	text-align: center;
	padding: 20px;
	font-size: 1.2em;
}

.error {
	color: #ff4444;
}

.empty-list {
	padding: 0;
	color: var(--pale-color);
	text-align: start;
}

/* Стили для дропдауна */
.status-dropdown {
	position: relative;
	min-width: 160px;
}

.status-button {
	width: 100%;
	padding: 8px 16px;
	border: 1px solid var(--pale-color);
	border-radius: 8px;
	background: white;
	text-align: center;
	cursor: pointer;
	transition: all 0.3s ease;
	font-size: 14px;
}

.status-button:hover {
	border-color: var(--dark-color);
}

.status-button.reading {
	border-color: #4CAF50;
	color: #4CAF50;
}

.status-button.completed {
	border-color: #2196F3;
	color: #2196F3;
}

.status-button.planned {
	border-color: #FFC107;
	color: #FFC107;
}

.dropdown-menu {
	position: absolute;
	top: 100%;
	left: 0;
	right: 0;
	background: white;
	border: 1px solid var(--pale-color);
	border-radius: 8px;
	margin-top: 4px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	z-index: 1000;
}

.dropdown-menu button {
	width: 100%;
	padding: 8px 16px;
	border: none;
	background: none;
	cursor: pointer;
	text-align: left;
	font-size: 14px;
	transition: all 0.3s ease;
}

.dropdown-menu button:hover {
	background-color: rgba(0, 0, 0, 0.05);
}

.dropdown-menu button.active {
	background-color: rgba(0, 0, 0, 0.05);
	font-weight: 600;
}

.status-button {
	transition: all 0.3s ease;
}

.status-button:hover {
	opacity: 0.8;
	/* background-color: #e7e7e7; */
	color: var(--dark-color)
}
h2 {
	font-size: 28px;
}
.userbooks-section {
	display: flex;
	flex-direction: column;
	gap: 20px;
}
</style>
