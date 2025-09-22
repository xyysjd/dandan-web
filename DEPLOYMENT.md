# 部署指南

## 快速开始

### 使用启动脚本（推荐）

```bash
chmod +x start.sh
./start.sh
```

### 手动启动

1. **克隆项目**
```bash
git clone <repository-url>
cd dandan-web
```

2. **配置环境变量**
```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env 文件，修改必要的配置
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **访问应用**
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 本地开发

### 后端开发

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端开发

```bash
cd frontend
pnpm install
pnpm dev
```

## 生产部署

### 使用Docker Compose

```bash
# 构建生产镜像
make build-prod

# 启动生产服务
make deploy-prod
```

### 使用Nginx反向代理

1. **配置Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

2. **配置HTTPS（可选）**
```bash
# 使用Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

## 环境变量配置

### 后端环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `CORS_ORIGINS` | 允许的跨域源 | `http://localhost:3000,http://localhost:5173` |
| `DANDAN_PROXY_URL` | 弹弹play代理URL | `https://dandan-proxy.wiidede.space/api/v2` |
| `UPLOAD_DIR` | 文件上传目录 | `uploads` |
| `MAX_FILE_SIZE` | 最大文件大小（字节） | `10737418240` (10GB) |
| `SECRET_KEY` | JWT密钥 | `your-secret-key-here-change-in-production` |

### 前端环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `VITE_API_BASE_URL` | 后端API地址 | `http://localhost:8000` |

## 故障排除

### 常见问题

1. **端口冲突**
   - 修改 `docker-compose.yml` 中的端口映射
   - 或停止占用端口的其他服务

2. **文件上传失败**
   - 检查 `uploads` 目录权限
   - 确认文件大小未超过限制

3. **弹幕匹配失败**
   - 检查网络连接
   - 确认弹弹play API可访问

4. **前端无法访问后端**
   - 检查CORS配置
   - 确认代理配置正确

### 日志查看

```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 服务管理

```bash
# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 重新构建并启动
docker-compose up -d --build

# 清理所有容器和镜像
docker-compose down -v --rmi all --remove-orphans
```

## 性能优化

### 后端优化

1. **使用Gunicorn**
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **启用缓存**
```python
# 在FastAPI中添加缓存中间件
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
```

### 前端优化

1. **启用Gzip压缩**（已在nginx.conf中配置）

2. **CDN加速**
```javascript
// 在vite.config.ts中配置CDN
export default defineConfig({
  build: {
    rollupOptions: {
      external: ['vue', 'element-plus'],
      output: {
        globals: {
          vue: 'Vue',
          'element-plus': 'ElementPlus'
        }
      }
    }
  }
})
```

## 监控和日志

### 使用Docker日志驱动

```yaml
# 在docker-compose.yml中添加
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 健康检查

```yaml
# 在docker-compose.yml中添加
services:
  backend:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## 安全建议

1. **更改默认密钥**
   - 修改 `SECRET_KEY` 为强密码

2. **限制文件上传**
   - 设置合理的文件大小限制
   - 验证文件类型

3. **使用HTTPS**
   - 在生产环境中启用SSL/TLS

4. **定期更新依赖**
   - 定期更新Python和Node.js依赖
   - 关注安全漏洞公告
