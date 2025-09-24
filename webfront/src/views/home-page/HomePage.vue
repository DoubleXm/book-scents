<template>
  <div class="relative flex h-auto min-h-screen w-full flex-col bg-white group/design-root overflow-x-hidden" style='font-family: "Work Sans", "Noto Sans", sans-serif;'>
    <div class="layout-container flex h-full grow flex-col">
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div class="@container">
            <div class="@[480px]:px-4 @[480px]:py-3">
              <div
                class="bg-cover bg-center flex flex-col justify-end overflow-hidden bg-white @[480px]:rounded-lg min-h-[218px]"
                style='background-image: linear-gradient(0deg, rgba(0, 0, 0, 0.4) 0%, rgba(0, 0, 0, 0) 25%), url("https://lh3.googleusercontent.com/aida-public/AB6AXuB4Jw1eLjJpLry2EIIxPsIg0047VW02tAz1MEeEK8Geb5JZext0VCSwKmCUr2rtGAavI64lnmlwg9zaqeFFm6qRDZN2BYf0SZDEK77PFzhxX8ijAaPxGEcZEEv5hIrt5mi-V3uxoNJeZ59p6oBiCjwLq1o6IzFTRVqNdJDd7milUwZPybiO7xPAG4KPP1jiKekitJ5wpYTHhn1iW-bHgrkH4WYwWrJgdAmeUH-P6ME3xbhB6QBB1Ykg0gVAc4fO-I2_9WmdcIuQrzY7");'
              >
                <div class="flex p-4"><p class="text-white tracking-light text-[28px] font-bold leading-tight">欢迎来到我们的图书系统</p></div>
              </div>
            </div>
          </div>
          <h2 class="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">热门书籍</h2>
          <div class="flex overflow-y-auto [-ms-scrollbar-style:none] [scrollbar-width:none] [&amp;::-webkit-scrollbar]:hidden">
            <div class="flex items-stretch p-4 gap-3">
              <div
                v-for="book in hotBooks"
                :key="book.id"
                class="flex h-full flex-1 flex-col gap-4 rounded-lg min-w-60"
                @click="$router.push({ name: 'BookDetailPage', params: { id: book.id }})"
              >
                <div
                  class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg flex flex-col"
                  :style='{
                    backgroundImage: `url(${book.cover})`
                  }'
                ></div>
                <div>
                  <p class="text-[#111518] text-base font-medium leading-normal">{{ book.name }}</p>
                  <p class="text-[#607a8a] text-sm font-normal leading-normal">创作者：{{ book.author }}</p>
                </div>
              </div>
            </div>
          </div>
          <h2 class="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">推荐书籍</h2>
          <div class="grid grid-cols-[repeat(auto-fit,minmax(158px,1fr))] gap-3 p-4">
            <div
              v-for="book in recommendBooks"
              :key="book.id"
              class="flex flex-col gap-3 pb-3"
              @click="$router.push({ name: 'BookDetailPage', params: { id: book.id }})"
            >
              <div
                class="w-full bg-center bg-no-repeat aspect-[3/4] bg-cover rounded-lg"
                :style='{
                  backgroundImage: `url(${book.cover})`
                }'
              ></div>
              <div>
                <p class="text-[#111518] text-base font-medium leading-normal">{{ book.name }}</p>
                <p class="text-[#607a8a] text-sm font-normal leading-normal">创作者：{{ book.author }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { fetchBooks } from '@/apis';

const payload = ref<Book.BooksReq>({
  pageNum: 1,
  pageSize: 4,
  name: '',
  order: 'DESC',
  filed: 'RECOMMEND',
})

const recommendBooks = ref<Book.BooksRes[]>([]);
const hotBooks = ref<Book.BooksRes[]>([]);

onMounted(async () => {
  try {
    const [recommendRes, hotRes] = await Promise.all([fetchBooks(payload.value), fetchBooks({ ...payload.value, filed: 'HOT' })]);
    recommendBooks.value = recommendRes.data.list || [];
    hotBooks.value = hotRes.data.list || [];
  } catch (error) {
    console.error('获取推荐书籍失败', error);
  }
});
</script>