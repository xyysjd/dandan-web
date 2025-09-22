from pydantic import BaseModel
from typing import Optional


class FileInfo(BaseModel):
    """文件信息模型"""
    filename: str
    size: int
    content_type: str
    md5: Optional[str] = None


class UploadResponse(BaseModel):
    """上传响应模型"""
    success: bool
    message: str
    file_info: Optional[FileInfo] = None
    file_url: Optional[str] = None


class MD5Request(BaseModel):
    """MD5计算请求"""
    filename: str


class MD5Response(BaseModel):
    """MD5计算响应"""
    success: bool
    md5: Optional[str] = None
    message: str
