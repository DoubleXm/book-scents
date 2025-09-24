<template>
  <div class="relative flex h-auto min-h-screen w-full flex-col bg-white group/design-root overflow-x-hidden" style='font-family: "Work Sans", "Noto Sans", sans-serif;'>
    <div class="layout-container flex h-full grow flex-col">
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col w-[512px] max-w-[512px] py-5 max-w-[960px] flex-1 items-center w-full">
          <h2 class="text-[#111418] tracking-light text-[28px] font-bold leading-tight px-4 text-center pb-3 pt-5">注册</h2>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <label class="flex flex-col min-w-40 flex-1">
              <input
                placeholder="请输入用户名"
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111418] focus:outline-0 focus:ring-0 border-none bg-[#f0f2f5] focus:border-none h-14 placeholder:text-[#5f718c] p-4 text-base font-normal leading-normal"
                v-model="formData.username"
                />
            </label>
          </div>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <label class="flex flex-col min-w-40 flex-1">
              <input
                placeholder="请输入密码"
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111418] focus:outline-0 focus:ring-0 border-none bg-[#f0f2f5] focus:border-none h-14 placeholder:text-[#5f718c] p-4 text-base font-normal leading-normal"
                v-model="formData.password"
              />
            </label>
          </div>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <label class="flex flex-col min-w-40 flex-1">
              <input
                placeholder="请输入手机号"
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111418] focus:outline-0 focus:ring-0 border-none bg-[#f0f2f5] focus:border-none h-14 placeholder:text-[#5f718c] p-4 text-base font-normal leading-normal"
                v-model="formData.mobile"
              />
            </label>
          </div>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <button
              @click="handleRegister"
              class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 flex-1 bg-[#0553c7] text-white text-sm font-bold leading-normal tracking-[0.015em]"
            >
              <span class="truncate">注册</span>
            </button>
          </div>
          <p
            @click="$router.push({ name: 'LoginPage' })"
            class="text-[#5f718c] text-sm font-normal leading-normal pb-3 pt-1 px-4 text-center underline">已有账号？直接登录</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { register } from '@/apis';

const router = useRouter();
const userStore = useUserStore();

const formData = reactive<User.UserRegisterReq>({
  username: '',
  password: '',
  mobile: '',
})

const handleRegister = async () => {
  const { data } = await register(formData);
  if (data.token) {
    userStore.setUser(data);
    router.push({ name: 'HomePage' });
  }
}
</script>