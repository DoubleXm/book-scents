import { defineStore } from "pinia"
import { onMounted, reactive } from "vue"

export const useUserStore = defineStore('user', () => {
  const user = reactive({
    profile: {} as User.UserRes,
    token: '',
  })

  const setUser = (data: User.UserLoginOfRegisterRes) => {
    user.profile = data.profile;
    user.token = data.token;
    window.localStorage.setItem('user', JSON.stringify(user));
  }

  const clearUser = () => {
    user.profile = {} as User.UserRes;
    user.token = '';
    window.localStorage.setItem('user', JSON.stringify(user));
  }

  const getUser = () => {
    return JSON.parse(window.localStorage.getItem('user') || '{}');
  }

  onMounted(() => {
    const data = getUser();
    if (data.token) {
      setUser(data);
    }
  })

  return {
    user,
    setUser,
    clearUser
  }
})