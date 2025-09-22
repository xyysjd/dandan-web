from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .core.config import settings
from .api import upload, dandan

# 创建FastAPI应用
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description=settings.description,
    openapi_url=f"{settings.api_v1_str}/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(upload.router, prefix=f"{settings.api_v1_str}", tags=["文件上传"])
app.include_router(dandan.router, prefix=f"{settings.api_v1_str}", tags=["弹弹play"])

# 静态文件服务（用于提供上传的视频文件）
upload_dir = Path(settings.upload_dir)
upload_dir.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "弹弹Play Web API",
        "version": settings.version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
