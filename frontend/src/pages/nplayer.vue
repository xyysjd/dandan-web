<script setup lang="ts">
import type { CommentResult } from '~/typings/comment'

const playerStore = usePlayerStore()
const { video, comments } = storeToRefs(playerStore)

function handleResult(res: CommentResult) {
  if (res.count) {
    comments.value = res.comments.map(dandan2nPlayer).sort((a, b) => a.time - b.time)
    ElNotification.info(`弹幕匹配成功：共${res.count}条弹幕`)
  }
}

usePlayer(handleResult)
</script>

<template>
  <player-layout>
    <div class="video-player-container">
      <div class="mb-4 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
        <h3 class="text-lg font-semibold text-blue-800 dark:text-blue-200 mb-2">NPlayer 播放器</h3>
        <p class="text-blue-600 dark:text-blue-300">
          NPlayer 播放器需要额外的依赖包。当前使用基础HTML5播放器作为替代。
        </p>
      </div>

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
      <div v-if="comments.length > 0" class="mt-4">
        <h3 class="text-lg font-semibold mb-2">弹幕列表 ({{ comments.length }} 条)</h3>
        <div class="max-h-40 overflow-y-auto border rounded p-2">
          <div
            v-for="(comment, index) in comments.slice(0, 50)"
            :key="index"
            class="text-sm py-1 border-b last:border-b-0"
          >
            <span class="text-gray-500">{{ comment.time }}s</span>
            <span class="ml-2" :style="{ color: comment.color ? `#${comment.color}` : 'inherit' }">
              {{ comment.text }}
            </span>
          </div>
          <div v-if="comments.length > 50" class="text-center text-gray-500 py-2">
            还有 {{ comments.length - 50 }} 条弹幕...
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

.disabled {
  pointer-events: none;
}

@media screen and (max-width: 768px) {
  .player-container {
    width: 100vw;
  }
}
</style>
