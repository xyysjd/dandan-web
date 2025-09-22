## 项目特性

- [x] 基础功能：弹幕播放器&匹配弹幕
- [x] 支持多种播放器（NPlayer、ArtPlayer、dan-player）
- [x] 主题色切换支持
- [x] 用户自定义主题色
- [x] 暗色模式支持
- [x] 手动匹配弹幕库
- [x] 手动添加XML弹幕
- [x] 响应式设计，适配移动端

## 技术栈

### 后端
- **FastAPI**: 现代、快速的Python Web框架
- **Uvicorn**: ASGI服务器
- **Pydantic**: 数据验证和设置管理
- **httpx**: 异步HTTP客户端
- **python-multipart**: 文件上传支持

### 前端
- **Vue 3**: 渐进式JavaScript框架
- **TypeScript**: 类型安全的JavaScript
- **Vite**: 现代前端构建工具
- **Element Plus**: Vue 3组件库
- **UnoCSS**: 原子化CSS引擎
- **Pinia**: Vue状态管理
- **Vue Router**: 路由管理

### 播放器
- **NPlayer**: 现代HTML5视频播放器
- **ArtPlayer**: 简洁的HTML5播放器
- **dan-player**: 支持弹幕的播放器



## 快速开始

### 一键启动（推荐）

```bash
chmod +x start.sh
./start.sh
```

这个脚本会自动：
- 检测并安装Docker和Docker Compose
- 修复依赖问题
- 构建并启动服务
- 显示访问地址

### 手动启动

```bash
# 确保Docker已安装
docker --version
docker-compose --version

# 启动服务
docker-compose up -d

# 访问应用
# 前端: http://localhost:3000
# 后端API: http://localhost:8000
# API文档: http://localhost:8000/docs
```

### 手动启动

#### 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 前端启动

```bash
cd frontend
npm install
npm run dev
```

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看自动生成的API文档。

## 主要功能

1. **视频上传和播放**: 支持本地视频文件上传和播放
2. **弹幕匹配**: 自动根据视频文件MD5匹配弹弹play弹幕库
3. **手动匹配**: 支持手动输入第三方弹幕站URL匹配弹幕
4. **XML弹幕导入**: 支持导入B站XML格式弹幕
5. **多播放器支持**: 可切换不同的播放器引擎
6. **主题定制**: 支持暗色模式和自定义主题色
7. **弹幕样式**: 可调整弹幕阴影、字重等样式

## 致谢

- [弹弹play](https://www.dandanplay.com/) - 原始项目和API支持
- [dandanplay-vi](https://github.com/wiidede/dandanplay-vi) - 原始Vue.js实现
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Python Web框架
- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架

## 许可证

MIT License
