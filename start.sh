#!/bin/bash

# 弹弹Play Web 启动脚本

set -e

echo "🎬 弹弹Play Web - 启动脚本"
echo "=================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，正在安装..."
    
    # 更新包管理器
    sudo apt update
    
    # 安装Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    
    # 将当前用户添加到docker组
    sudo usermod -aG docker $USER
    
    echo "✅ Docker安装完成"
    echo "⚠️  请重新登录或运行 'newgrp docker' 后再次运行此脚本"
    exit 0
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，正在安装..."
    
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    echo "✅ Docker Compose安装完成"
fi

# 修复依赖问题
echo "🔧 修复依赖问题..."
chmod +x fix-dependencies.sh
./fix-dependencies.sh

# 停止可能运行的旧容器
echo "🛑 停止旧容器..."
docker-compose down 2>/dev/null || true

# 清理Docker缓存
echo "🧹 清理Docker缓存..."
docker system prune -f

# 构建镜像（不使用缓存）
echo "🔨 构建Docker镜像..."
docker-compose build --no-cache

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 20

# 检查服务状态
echo "🔍 检查服务状态..."
BACKEND_STATUS="❌"
FRONTEND_STATUS="❌"

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    BACKEND_STATUS="✅"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    FRONTEND_STATUS="✅"
fi

# 获取服务器IP
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s ipinfo.io/ip 2>/dev/null || echo "YOUR_SERVER_IP")

echo ""
echo "🎉 启动完成！"
echo "=================================="
echo "服务状态:"
echo "  后端服务: $BACKEND_STATUS"
echo "  前端服务: $FRONTEND_STATUS"
echo ""
echo "📱 本地访问:"
echo "   前端: http://localhost:3000"
echo "   后端: http://localhost:8000"
echo ""
echo "🌐 外网访问:"
echo "   前端: http://$SERVER_IP:3000"
echo "   后端: http://$SERVER_IP:8000"
echo "   API文档: http://$SERVER_IP:8000/docs"
echo ""
echo "📋 常用命令:"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo ""

if [ "$BACKEND_STATUS" = "❌" ] || [ "$FRONTEND_STATUS" = "❌" ]; then
    echo "⚠️  部分服务启动失败，请检查日志:"
    echo "  docker-compose logs backend"
    echo "  docker-compose logs frontend"
    echo ""
fi

echo "🎬 弹弹Play Web已启动！"
