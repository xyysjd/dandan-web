from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Settings
    api_v1_str: str = "/api/v1"
    project_name: str = "弹弹Play Web API"
    version: str = "1.0.0"
    description: str = "弹弹Play Web版本的后端API服务"
    
    # CORS Settings
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # DanDan Play API
    dandan_api_base_url: str = "https://api.dandanplay.net/api/v2"
    dandan_proxy_url: str = "https://dandan-proxy.wiidede.space/api/v2"
    
    # File Upload Settings
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024 * 1024  # 10GB
    allowed_video_extensions: List[str] = [
        ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", 
        ".webm", ".m4v", ".3gp", ".ogv", ".ts", ".m2ts"
    ]
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
