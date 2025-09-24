<template>
  <div class="relative flex h-auto min-h-screen w-full flex-col bg-white group/design-root overflow-x-hidden" style='font-family: "Work Sans", "Noto Sans", sans-serif;'>
      <div class="layout-container flex h-full grow flex-col">
        <div class="px-40 flex flex-1 justify-center py-5">
          <div class="layout-content-container flex flex-col w-[512px] max-w-[512px] py-5 max-w-[960px] flex-1 items-center w-full">
            <div class="flex flex-wrap justify-between align-center gap-3 p-4"><p class="text-[#111518] tracking-light text-[32px] font-bold leading-tight min-w-72 text-center">个人信息</p></div>
            <div class="flex p-4 @container">
              <div class="flex w-full flex-col gap-4 items-center">
                <div class="flex gap-4 flex-col items-center">
                  <div
                    class="bg-center bg-no-repeat aspect-square bg-cover rounded-full min-h-32 w-32"
                    :style="{ backgroundImage: `url(${userStore.user.value.profile.cover})` }"
                  ></div>
                  <div class="flex flex-col items-center justify-center justify-center">
                    <p class="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] text-center">{{ userStore.user.value.profile.name }}</p>
                    <p class="text-[#607a8a] text-base font-normal leading-normal text-center">用户名: {{ userStore.user.value.profile.name }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
              <label class="flex flex-col min-w-40 flex-1">
                <p class="text-[#111518] text-base font-medium leading-normal pb-2">用户名</p>
                <input
                  class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111518] focus:outline-0 focus:ring-0 border-none bg-[#f0f3f5] focus:border-none h-14 placeholder:text-[#607a8a] p-4 text-base font-normal leading-normal"
                  :value="userStore.user.value.profile.name"
                />
              </label>
            </div>
            <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
              <label class="flex flex-col min-w-40 flex-1">
                <p class="text-[#111518] text-base font-medium leading-normal pb-2">手机号码</p>
                <input
                  class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111518] focus:outline-0 focus:ring-0 border-none bg-[#f0f3f5] focus:border-none h-14 placeholder:text-[#607a8a] p-4 text-base font-normal leading-normal"
                  :value="userStore.user.value.profile.mobile"
                />
              </label>
            </div>
            <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
              <button
                @click="handleLogout"
                class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 flex-1 bg-[#0a54c2] text-white text-sm font-bold leading-normal tracking-[0.015em]"
              >
                <span class="truncate">退出登录</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

const router = useRouter()
const userStore = storeToRefs(useUserStore());
const { clearUser } = useUserStore();

const handleLogout = () => {
  clearUser();
  router.push({ name: 'LoginPage' })
}
</script>