<template>
  <div class="relative flex h-auto min-h-screen w-full flex-col bg-white group/design-root overflow-x-hidden" style='font-family: "Work Sans", "Noto Sans", sans-serif;'>
    <div class="layout-container flex h-full grow flex-col">
      <div class="px-40 flex flex-1 justify-center py-5">
        <div class="layout-content-container flex flex-col max-w-[960px] flex-1">
          <div class="px-4 py-3">
            <label class="flex flex-col min-w-40 h-12 w-full">
              <div class="flex w-full flex-1 items-stretch rounded-lg h-full">
                <div
                  class="text-[#607a8a] flex border-none bg-[#f0f3f5] items-center justify-center pl-4 rounded-l-lg border-r-0"
                  data-icon="MagnifyingGlass"
                  data-size="24px"
                  data-weight="regular"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                    <path
                      d="M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z"
                    ></path>
                  </svg>
                </div>
                <input
                  placeholder="搜索书籍..."
                  class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111518] focus:outline-0 focus:ring-0 border-none bg-[#f0f3f5] focus:border-none h-full placeholder:text-[#607a8a] px-4 rounded-l-none border-l-0 pl-2 text-base font-normal leading-normal"
                  v-model="queryParams.name"
                  @keyup.enter="handlerSearch"
                />
              </div>
            </label>
          </div>
          <h2 class="text-[#111518] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">书籍列表</h2>
          <div class="px-4 py-3 @container">
            <div class="flex overflow-hidden rounded-lg border border-[#dbe2e6] bg-white">
              <ElTable :data="result.list" size="large">
                <ElTableColumn prop="name" label="书籍名称" show-overflow-tooltip></ElTableColumn>
                <ElTableColumn prop="author" label="作者" show-overflow-tooltip></ElTableColumn>
                <ElTableColumn prop="publisher" label="出版社" show-overflow-tooltip></ElTableColumn>
                <ElTableColumn prop="publisherDate" label="出版日期" show-overflow-tooltip></ElTableColumn>
                <ElTableColumn label="查看" width="80">
                  <template #default="{ row }">
                    <a href="#" @click.prevent="$router.push({ name: 'BookDetailPage', params: { id: row.id }})">查看</a>
                  </template>
                </ElTableColumn>
              </ElTable>
            </div>
          </div>
          <div class="flex items-end justify-end p-4">
            <ElPagination
              v-model:current-page="queryParams.pageNum"
              background
              layout="prev, pager, next" 
              :total="result.total"
              :page-size="queryParams.pageSize"
              @current-change="onCurrentChange"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { fetchBooks } from '@/apis';
import { ElTableColumn, ElTable, ElPagination } from 'element-plus';

const queryParams = ref<Partial<Book.BooksReq>>({
  pageSize: 20,
  pageNum: 1,
  name: ''
});

const result = ref<ListResult<Book.BooksRes>>({
  list: [],
  total: 0
});

onMounted(() => {
  handlerSearch();
})

const handlerSearch = () => {
  fetchBooks(queryParams.value).then(res => {
    result.value = res.data;
  });
}

const onCurrentChange = (val: number) => {
  queryParams.value.pageNum = val;
  handlerSearch();
}
</script>