#!/bin/bash

# 修复前端问题的脚本

echo "🔧 修复前端问题..."

cd frontend

# 重新创建main.ts
echo "📝 修复main.ts..."
cat > src/main.ts << 'EOF'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ElementPlus from 'element-plus'
import NProgress from 'nprogress'
import routes from 'virtual:generated-pages'

import App from './App.vue'

// 样式导入
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import '@unocss/reset/tailwind-compat.css'
import 'uno.css'
import './styles/main.css'
import 'nprogress/nprogress.css'

const app = createApp(App)

// 路由
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

router.beforeEach((to, from, next) => {
  NProgress.start()
  next()
})

router.afterEach(() => {
  NProgress.done()
})

app.use(router)

// 状态管理
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// Element Plus
app.use(ElementPlus)

app.mount('#app')
EOF

# 确保UnoCSS配置正确
echo "📝 修复UnoCSS配置..."
cat > unocss.config.ts << 'EOF'
import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetTypography,
  presetUno,
  presetWebFonts,
  transformerDirectives,
  transformerVariantGroup,
} from 'unocss'

export default defineConfig({
  shortcuts: [
    ['btn', 'px-4 py-1 rounded inline-block bg-teal-600 text-white cursor-pointer hover:bg-teal-700 disabled:cursor-default disabled:bg-gray-600 disabled:opacity-50'],
    ['icon-btn', 'inline-block cursor-pointer select-none opacity-75 transition duration-200 ease-in-out hover:opacity-100 hover:text-teal-600'],
  ],
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
      collections: {
        ep: () => import('@iconify-json/ep/icons.json').then(i => i.default),
      },
    }),
    presetTypography(),
    presetWebFonts({
      fonts: {
        sans: 'DM Sans',
        serif: 'DM Serif Display',
        mono: 'DM Mono',
      },
    }),
  ],
  transformers: [
    transformerDirectives(),
    transformerVariantGroup(),
  ],
})
EOF

# 更新package.json添加缺少的依赖
echo "📝 更新package.json..."
cat > package.json << 'EOF'
{
  "name": "dandan-web-frontend",
  "type": "module",
  "version": "1.0.0",
  "private": true,
  "packageManager": "pnpm@8.15.0",
  "scripts": {
    "build": "vite build",
    "dev": "vite --host 0.0.0.0 --port 3000",
    "lint": "eslint .",
    "typecheck": "vue-tsc --noEmit",
    "preview": "vite preview",
    "test": "vitest"
  },
  "dependencies": {
    "@element-plus/icons-vue": "^2.1.0",
    "@iconify/utils": "^2.1.0",
    "@vueuse/core": "^10.9.0",
    "axios": "^1.6.2",
    "element-plus": "^2.4.4",
    "nprogress": "^0.2.0",
    "pinia": "^2.1.7",
    "pinia-plugin-persistedstate": "^3.2.1",
    "spark-md5": "^3.0.2",
    "tinycolor2": "^1.6.0",
    "vue": "^3.4.0",
    "vue-router": "^4.2.5"
  },
  "devDependencies": {
    "@antfu/eslint-config": "^2.6.4",
    "@iconify-json/ep": "^1.1.15",
    "@iconify/json": "^2.2.150",
    "@types/node": "^20.10.0",
    "@types/nprogress": "^0.2.3",
    "@types/spark-md5": "^3.0.4",
    "@types/tinycolor2": "^1.4.6",
    "@unocss/reset": "^0.58.0",
    "@vitejs/plugin-vue": "^4.5.2",
    "@vue/test-utils": "^2.4.3",
    "eslint": "^8.56.0",
    "jsdom": "^23.2.0",
    "typescript": "^5.3.3",
    "unocss": "^0.58.0",
    "unplugin-auto-import": "^0.17.2",
    "unplugin-vue-components": "^0.26.0",
    "vite": "^5.0.10",
    "vite-plugin-pages": "^0.32.0",
    "vitest": "^1.1.0",
    "vue-tsc": "^1.8.25"
  }
}
EOF

# 重新安装依赖
echo "📦 重新安装依赖..."
rm -rf node_modules pnpm-lock.yaml package-lock.json yarn.lock

if command -v pnpm &> /dev/null; then
    pnpm install
elif command -v yarn &> /dev/null; then
    yarn install
else
    npm install
fi

echo "✅ 前端修复完成！"
echo ""
echo "现在可以重新启动服务："
echo "  cd .."
echo "  docker-compose restart frontend"
