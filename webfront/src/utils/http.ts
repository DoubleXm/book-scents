import axios from 'axios';
import router from '@/router';
import { ElMessage } from 'element-plus';

axios.defaults.timeout = 10000;
axios.defaults.baseURL = '/api/v1';

axios.interceptors.request.use((config) => {
  const user = localStorage.getItem('user');
  if (user) {
    const token = JSON.parse(user).token;
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

axios.interceptors.response.use((response) => {
  return response;
}, (error) => {
  if (error.response.data.code !== 200) {
    ElMessage.error(error.response.data.message);
     if (error.response.status === 401) {
      router.push({ name: 'LoginPage' });
    }
  }
  return Promise.reject(error);
});

export {
  axios
};