import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional

from ..core.config import settings
from ..models.upload import UploadResponse, FileInfo, MD5Request, MD5Response
from ..utils.file_utils import (
    calculate_md5_sync, 
    calculate_md5, 
    is_video_file, 
    ensure_upload_dir,
    get_file_size
)

router = APIRouter()

# 确保上传目录存在
upload_dir = ensure_upload_dir(settings.upload_dir)


@router.post("/upload", response_model=UploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    上传视频文件
    """
    # 检查文件类型
    if not is_video_file(file.filename, settings.allowed_video_extensions):
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式。支持的格式: {', '.join(settings.allowed_video_extensions)}"
        )
    
    # 检查文件大小
    if file.size and file.size > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制 ({settings.max_file_size / (1024**3):.1f}GB)"
        )
    
    try:
        # 生成文件路径
        file_path = upload_dir / file.filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 获取文件信息
        file_size = get_file_size(file_path)
        
        # 计算MD5（异步）
        md5_hash = await calculate_md5(file_path)
        
        file_info = FileInfo(
            filename=file.filename,
            size=file_size,
            content_type=file.content_type or "video/mp4",
            md5=md5_hash
        )
        
        return UploadResponse(
            success=True,
            message="文件上传成功",
            file_info=file_info,
            file_url=f"/api/v1/files/{file.filename}"
        )
        
    except Exception as e:
        # 清理可能创建的文件
        if file_path.exists():
            file_path.unlink()
        
        raise HTTPException(
            status_code=500,
            detail=f"文件上传失败: {str(e)}"
        )


@router.post("/calculate-md5", response_model=MD5Response)
async def calculate_file_md5(request: MD5Request):
    """
    计算已上传文件的MD5值
    """
    file_path = upload_dir / request.filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="文件不存在"
        )
    
    try:
        md5_hash = await calculate_md5(file_path)
        return MD5Response(
            success=True,
            md5=md5_hash,
            message="MD5计算完成"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"MD5计算失败: {str(e)}"
        )


@router.get("/files/{filename}")
async def get_file(filename: str):
    """
    获取上传的文件
    """
    file_path = upload_dir / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="文件不存在"
        )
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    """
    删除上传的文件
    """
    file_path = upload_dir / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="文件不存在"
        )
    
    try:
        file_path.unlink()
        return {"success": True, "message": "文件删除成功"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件删除失败: {str(e)}"
        )
