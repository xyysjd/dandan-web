<script setup lang="ts">
import Worker from '~/workers/dandanMd5.ts?worker'

const worker = new Worker()
const router = useRouter()
const settingsStore = useSettingsStore()
const { player } = storeToRefs(settingsStore)
const playerStore = usePlayerStore()
const { video, videoInfo } = storeToRefs(playerStore)

watch(video, (val) => {
  if (val) {
    ElNotification.info(`读取文件：${videoInfo.value.name}`)
    videoInfo.value.md5 = ''
    worker.postMessage(videoInfo.value.raw)
    router.push(player.value)
    setTimeout(async () => {
      if (!videoInfo.value.md5) {
        ElNotification.warning('md5后台计算3s没有响应，开始在主线程计算')
        worker.terminate()
        videoInfo.value.md5 = await calcDandanMd5(videoInfo.value.raw!)
      }
    }, 3000)
  }
})

worker.onmessage = (e) => {
  videoInfo.value.md5 = e.data
}
</script>

<template>
  <div class="container mx-auto">
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold mb-4">弹弹Play Web</h1>
      <p class="text-lg text-gray-600 dark:text-gray-400">
        弹弹play web简易实现 - Python版本
      </p>
    </div>
    
    <div class="max-w-2xl mx-auto">
      <Uploader />
    </div>
    
    <div class="mt-12 text-center">
      <h2 class="text-2xl font-semibold mb-4">功能特性</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="p-4 border rounded-lg">
          <h3 class="font-semibold mb-2">多播放器支持</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            支持NPlayer、ArtPlayer、dan-player三种播放器
          </p>
        </div>
        <div class="p-4 border rounded-lg">
          <h3 class="font-semibold mb-2">弹幕匹配</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            自动匹配弹弹play弹幕库，支持手动匹配
          </p>
        </div>
        <div class="p-4 border rounded-lg">
          <h3 class="font-semibold mb-2">主题定制</h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            支持暗色模式和自定义主题色
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  padding: 2rem 1rem;
}
</style>
