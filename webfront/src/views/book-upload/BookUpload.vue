<template>
  <div class="relative flex h-auto min-h-screen w-full flex-col bg-white group/design-root overflow-x-hidden" style='font-family: "Work Sans", "Noto Sans", sans-serif;'>
    <div class="layout-container flex h-full grow flex-col">
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col w-[512px] max-w-[512px] py-5 max-w-[960px] flex-1 items-center w-full">
          <div class="flex flex-wrap justify-between gap-3 p-4"><p class="text-[#111518] tracking-light text-[32px] font-bold leading-tight min-w-72 text-center">上传书籍</p></div>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <label class="flex flex-col min-w-40 flex-1">
              <p class="text-[#111518] text-base font-medium leading-normal pb-2">书籍名称</p>
              <input
                placeholder="请输入书籍名称"
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111518] focus:outline-0 focus:ring-0 border-none bg-[#f0f3f5] focus:border-none h-14 placeholder:text-[#607a8a] p-4 text-base font-normal leading-normal"
                v-model="bookForm.name"
              />
            </label>
          </div>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <label class="flex flex-col min-w-40 flex-1">
              <p class="text-[#111518] text-base font-medium leading-normal pb-2">作者</p>
              <input
                placeholder="请输入作者"
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111518] focus:outline-0 focus:ring-0 border-none bg-[#f0f3f5] focus:border-none h-14 placeholder:text-[#607a8a] p-4 text-base font-normal leading-normal"
                v-model="bookForm.author"
              />
            </label>
          </div>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <label class="flex flex-col min-w-40 flex-1">
              <p class="text-[#111518] text-base font-medium leading-normal pb-2">书籍描述</p>
              <textarea
                placeholder="请输入书籍描述"
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111518] focus:outline-0 focus:ring-0 border-none bg-[#f0f3f5] focus:border-none min-h-36 placeholder:text-[#607a8a] p-4 text-base font-normal leading-normal"
                v-model="bookForm.description"
              ></textarea>
            </label>
          </div>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <label class="flex flex-col min-w-40 flex-1">
              <p class="text-[#111518] text-base font-medium leading-normal pb-2">书籍封面</p>
              <input
                placeholder="请上传书籍封面"
                type="file"
                class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111518] focus:outline-0 focus:ring-0 border-none bg-[#f0f3f5] focus:border-none h-14 placeholder:text-[#607a8a] p-4 text-base font-normal leading-normal"
                @change="handleUpload"
              />
            </label>
          </div>
          <div class="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3 w-full">
            <button
              @click="handleSubmit"
              class="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-10 px-4 flex-1 bg-[#0a54c2] text-white text-sm font-bold leading-normal tracking-[0.015em]"
            >
              <span class="truncate">上传</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue';
import { createBook } from '@/apis';
import { ElMessage } from 'element-plus';

const bookForm = reactive<Book.CreateBookReq>({
  name: '',
  author: '',
  description: '',
  cover: null as File | null,
})

const handleUpload = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    bookForm.cover = file;
  }
}

const handleSubmit = async () => {
  if (!bookForm.cover) {
    ElMessage.warning('请上传书籍封面');
  }
  const formData = new FormData();
  formData.append('name', bookForm.name);
  formData.append('author', bookForm.author);
  formData.append('description', bookForm.description);
  formData.append('cover', bookForm.cover as File);
  await createBook(formData as unknown as Book.CreateBookReq);
}
</script>