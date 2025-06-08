import axios from 'axios';

export default {
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  },
  getUsername() {
    return localStorage.getItem('username');
  },
  getToken() {
    return localStorage.getItem('authToken');
  },
  logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('username');
    delete axios.defaults.headers.common['Authorization'];
  },
  initializeAxios() {
    const token = this.getToken();
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;
    }
  }
}; 