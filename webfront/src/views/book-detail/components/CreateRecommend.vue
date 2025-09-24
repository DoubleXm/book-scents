<template>
  <ElDialog 
    title="发布评论"
    :model-value="modelValue"
    :before-close="() => $emit('update:modelValue', false)"
    :destroy-on-close="true"
    width="50%"
  >
    <ElForm label-position="top">
      <ElFormItem label="内容">
        <ElInput v-model="form.content" />
      </ElFormItem>
      <ElFormItem label="评分">
        <ElRate v-model="form.rating" allow-half />
      </ElFormItem>
    </ElForm>

    <template #footer>
      <ElButton @click="() => $emit('update:modelValue', false)">取消</ElButton>
      <ElButton type="primary" @click="onCreate">发布</ElButton>
    </template>
  </ElDialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { ElDialog, ElButton, ElInput, ElRate, ElForm, ElFormItem } from 'element-plus';
import { createRecommend } from '@/apis';

const props = defineProps<{
  id: string;
  modelValue: boolean;
}>()
const emits = defineEmits<{
  (e: 'update:modelValue', value: boolean): void;
}>()

const form = ref({
  content: '',
  rating: 0
})

const onCreate = async () => {
  await createRecommend(props.id, form.value);
  emits('update:modelValue', false);
}
</script>