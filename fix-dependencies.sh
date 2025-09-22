#!/bin/bash

# 修复依赖问题的脚本

echo "🔧 修复弹弹Play Web依赖问题..."

# 进入前端目录
cd frontend

# 删除可能有问题的文件
echo "🗑️  清理缓存文件..."
rm -rf node_modules
rm -rf pnpm-lock.yaml
rm -rf package-lock.json
rm -rf yarn.lock

# 创建简化的package.json
echo "📝 创建简化的package.json..."
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

# 创建简化的vite.config.ts
echo "📝 创建简化的vite.config.ts..."
cat > vite.config.ts << 'EOF'
/// <reference types="vitest" />

import path from 'node:path'
import Vue from '@vitejs/plugin-vue'
import Unocss from 'unocss/vite'
import AutoImport from 'unplugin-auto-import/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Components from 'unplugin-vue-components/vite'
import { defineConfig } from 'vite'
import Pages from 'vite-plugin-pages'

export default defineConfig({
  resolve: {
    alias: {
      '~/': `${path.resolve(__dirname, 'src')}/`,
      '@/': `${path.resolve(__dirname, 'libs')}/`,
    },
  },
  plugins: [
    Vue(),
    Pages(),
    AutoImport({
      imports: [
        'vue',
        'vue/macros',
        'vue-router',
        '@vueuse/core',
        'pinia',
        {
          tinycolor2: [['default', 'tinycolor']],
        },
      ],
      dts: true,
      dirs: [
        './src/composables',
        './src/store',
        './src/services',
        './src/utils',
      ],
      vueTemplate: true,
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      dts: true,
      resolvers: [
        ElementPlusResolver(),
      ],
    }),
    Unocss(),
  ],
  test: {
    environment: 'jsdom',
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  worker: {
    format: 'es',
  },
})
EOF

# 创建简化的tsconfig.json
echo "📝 创建简化的tsconfig.json..."
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "es2016",
    "jsx": "preserve",
    "lib": ["DOM", "ESNext"],
    "baseUrl": ".",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "paths": {
      "~/*": ["src/*"],
      "@/*": ["libs/*"]
    },
    "resolveJsonModule": true,
    "allowJs": true,
    "strict": true,
    "strictNullChecks": true,
    "noUnusedLocals": false,
    "outDir": "./dist",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": [
    "src/**/*.ts",
    "src/**/*.d.ts",
    "src/**/*.tsx",
    "src/**/*.vue",
    "auto-imports.d.ts",
    "components.d.ts"
  ],
  "exclude": ["dist", "node_modules", "libs"]
}
EOF

# 安装依赖
echo "📦 安装依赖..."
if command -v pnpm &> /dev/null; then
    pnpm install
elif command -v yarn &> /dev/null; then
    yarn install
else
    npm install
fi

echo "✅ 依赖修复完成！"
echo ""
echo "现在可以运行以下命令启动项目："
echo "  cd .."
echo "  docker-compose up -d"
echo ""
echo "或者手动启动："
echo "  cd frontend && pnpm dev"
echo "  cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
