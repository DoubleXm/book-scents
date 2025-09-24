<template>
  <header class="flex items-center justify-between whitespace-nowrap border-b border-solid border-b-[#f0f3f5] px-10 py-3">
    <div class="flex items-center gap-4 text-[#111518]" @click="$router.push({ name: 'HomePage' })">
      <div class="size-4">
        <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M4 42.4379C4 42.4379 14.0962 36.0744 24 41.1692C35.0664 46.8624 44 42.2078 44 42.2078L44 7.01134C44 7.01134 35.068 11.6577 24.0031 5.96913C14.0971 0.876274 4 7.27094 4 7.27094L4 42.4379Z"
            fill="currentColor"
          ></path>
        </svg>
      </div>
      <h2 class="text-[#111518] text-lg font-bold leading-tight tracking-[-0.015em]">书香</h2>
    </div>
    <div class="flex flex-1 justify-end gap-8">
      <div class="flex items-center gap-9">
        <a @click.prevent="$router.push({ name: 'HomePage' })" class="text-[#111518] text-sm font-medium leading-normal" href="#">首页</a>
        <a @click.prevent="$router.push({ name: 'BooksPage' })" class="text-[#111518] text-sm font-medium leading-normal" href="#">书籍列表</a>
        <a @click.prevent="$router.push({ name: 'BookUploadPage' })" class="text-[#111518] text-sm font-medium leading-normal" href="#">上传书籍</a>
      </div>
      <div
        @click="$router.push({ name: 'ProfilePage' })"
        class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
        :style="{ backgroundImage: `url(${user.profile.cover})` }"
      ></div>
    </div>
  </header>

  <slot />
</template>

<script lang="ts" setup>
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const { user } = storeToRefs(userStore);
</script>