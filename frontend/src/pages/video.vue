<script setup lang="ts">
import type { CommentResult, ICommentCCL } from '~/typings/comment'

const playerStore = usePlayerStore()
const { video, videoInfo, comments } = storeToRefs(playerStore)
const commentsCCL = computed<ICommentCCL[]>(() => comments.value as ICommentCCL[])

function handleResult(res: CommentResult) {
  if (res.count) {
    comments.value = res.comments.map(dandan2CCL)
    ElNotification.info(`弹幕匹配成功：共${res.count}条弹幕`)
  }
}

usePlayer(handleResult)
</script>

<template>
  <player-layout>
    <div class="video-player-container">
      <video
        v-if="video"
        :src="video"
        controls
        class="w-full h-96 bg-black rounded-lg"
        @loadedmetadata="ElNotification.success('视频加载完成')"
      >
        您的浏览器不支持视频播放
      </video>
      <div v-else class="w-full h-96 bg-gray-200 dark:bg-gray-800 rounded-lg flex items-center justify-center">
        <p class="text-gray-500">请先上传视频文件</p>
      </div>

      <!-- 弹幕显示区域 -->
      <div v-if="commentsCCL.length > 0" class="mt-4">
        <h3 class="text-lg font-semibold mb-2">弹幕列表 ({{ commentsCCL.length }} 条)</h3>
        <div class="max-h-40 overflow-y-auto border rounded p-2">
          <div
            v-for="(comment, index) in commentsCCL.slice(0, 50)"
            :key="index"
            class="text-sm py-1 border-b last:border-b-0"
          >
            <span class="text-gray-500">{{ Math.floor(comment.stime / 1000) }}s</span>
            <span class="ml-2">{{ comment.text }}</span>
          </div>
          <div v-if="commentsCCL.length > 50" class="text-center text-gray-500 py-2">
            还有 {{ commentsCCL.length - 50 }} 条弹幕...
          </div>
        </div>
      </div>
    </div>
    <template #action>
      <ActionLayout @manual-match="manualMatchComment(handleResult)" @manual-match-xml="manualMatchCommentXML(handleResult)" />
    </template>
  </player-layout>
</template>

<style scoped>
.video-player-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}
</style>
