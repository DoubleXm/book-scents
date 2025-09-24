<template>
  <div class="relative flex h-auto min-h-screen w-full flex-col bg-white group/design-root overflow-x-hidden" style='font-family: "Work Sans", "Noto Sans", sans-serif;'>
    <div class="layout-container flex h-full grow flex-col" v-if="bookDetail && recommends.list">
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div class="flex flex-wrap gap-2 p-4">
            <a class="text-[#607a8a] text-base font-medium leading-normal" href="#" @click.prevent="$router.go(-1)">书籍列表</a>
            <span class="text-[#607a8a] text-base font-medium leading-normal">/</span>
            <span class="text-[#111518] text-base font-medium leading-normal">书籍详情</span>
          </div>
          <div class="p-4">
            <div class="flex items-stretch justify-between gap-4 rounded-lg">
              <div class="flex flex-[2_2_0px] flex-col gap-4">
                <div class="flex flex-col gap-1">
                  <p class="text-[#111518] text-base font-bold leading-tight">{{ bookDetail?.name }}</p>
                  <p class="text-[#607a8a] text-sm font-normal leading-normal">{{ bookDetail?.author }}</p>
                </div>
                <button
                  @click="handleReadClick"
                  class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-8 px-4 flex-row-reverse bg-[#f0f3f5] text-[#111518] text-sm font-medium leading-normal w-fit"
                >
                  <span class="truncate">阅读</span>
                </button>
              </div>
              <div
                class="w-full bg-center bg-no-repeat aspect-video bg-cover rounded-lg flex-1"
                :style="{ backgroundImage: `url(${bookDetail?.cover})` }"
              ></div>
            </div>
          </div>
          <h2 class="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">书籍介绍</h2>
          <p class="text-[#111518] text-base font-normal leading-normal pb-3 pt-1 px-4">{{ bookDetail?.description }}</p>
          <h2 class="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">评分</h2>
          <div class="flex flex-wrap gap-x-8 gap-y-6 p-4">
            <div class="flex flex-col gap-2">
              <p class="text-[#111518] text-4xl font-black leading-tight tracking-[-0.033em]">{{ bookDetail?.rating }}</p>
              <div class="flex gap-0.5">
                <ElRate 
                  :model-value="bookDetail?.rating > 5 ? 5 : bookDetail?.rating"
                  disabled
                  allow-half
                />
              </div>
              <div class="flex">
                <p class="text-[#111518] text-base font-normal leading-normal">{{ recommends.total }} 条评论</p>
                <p
                  @click="visible = true"
                  style="margin-left: 10px; cursor: pointer; color: var(--el-color-primary);"
                  class="text-[#111518] text-base font-normal leading-normal"
                >发布评论</p>
              </div>
            </div>
            <div class="min-w-[200px] max-w-[400px] flex-1 grid-cols-[20px_1fr_40px] items-center gap-y-3">
              <div
                class="flex"
                v-for="(item, index) in bookDetail.statement.reverse()" 
                :key="index"
              >
                <p class="text-[#111518] text-sm font-normal leading-normal mr-2">{{ bookDetail.statement.length - index }}</p>
                <ElProgress
                  class="flex-1"
                  :percentage="item > 100 ? 100 : item"
                  :show-text="false"
                  :stroke-width="8"
                />
              </div>
            </div>
          </div>
          <div class="flex flex-col gap-8 overflow-x-hidden bg-white p-4">
            <div class="flex flex-col gap-3 bg-white" v-for="recommend in recommends.list" :key="recommend.id">
              <div class="flex items-center gap-3">
                <div
                  class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-10"
                  :style="{
                    backgroundImage: `url(${recommend.user.cover})`
                  }"
                ></div>
                <div class="flex-1">
                  <p class="text-[#111518] text-base font-medium leading-normal">{{ recommend.user.name }}</p>
                  <p class="text-[#607a8a] text-sm font-normal leading-normal">{{ recommend.createdTime }}</p>
                </div>
              </div>
              <div class="flex gap-0.5">
                <ElRate 
                  :model-value="recommend.rating > 5 ? 5 : recommend.rating"
                  disabled
                  allow-half
                />
              </div>
              <p class="text-[#111518] text-base font-normal leading-normal">{{ recommend.content }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <CreateRecommend v-if="bookDetail?.id" v-model="visible" :id="(bookDetail?.id as string)" />
  </div>
</template>

<script lang="ts" setup>
import { fetchBookById, fetchRecommends, createBookRead } from '@/apis'
import { ElProgress } from 'element-plus';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import CreateRecommend from '@/views/book-detail/components/CreateRecommend.vue';

const route = useRoute();
const bookDetail = ref<Book.BookDetailRes>()
const recommends = ref<ListResult<Recommend.RecommendRes>>({
  list: [],
  total: 0,
})
const visible = ref(false);

onMounted(async () => {
  const id = route.params.id as string;
  const { data } = await fetchBookById(id);
  bookDetail.value = data;

  const { data: recommendsData } = await fetchRecommends(id)
  recommends.value = recommendsData;
})

const handleReadClick = async () => {
  await createBookRead(bookDetail.value?.id as string);
  window.open(bookDetail.value?.url, '_blank');
}
</script>