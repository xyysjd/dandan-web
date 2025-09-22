import hashlib
import os
import aiofiles
from typing import BinaryIO, Union
from pathlib import Path


async def calculate_md5(file_path: Union[str, Path], chunk_size: int = 16 * 1024 * 1024) -> str:
    """
    异步计算文件MD5值
    
    Args:
        file_path: 文件路径
        chunk_size: 读取块大小，默认16MB
        
    Returns:
        文件的MD5值
    """
    md5_hash = hashlib.md5()
    
    async with aiofiles.open(file_path, 'rb') as f:
        # 只读取前16MB用于计算MD5（与原项目保持一致）
        chunk = await f.read(chunk_size)
        if chunk:
            md5_hash.update(chunk)
    
    return md5_hash.hexdigest()


def calculate_md5_sync(file_obj: BinaryIO, chunk_size: int = 16 * 1024 * 1024) -> str:
    """
    同步计算文件MD5值（用于上传时的实时计算）
    
    Args:
        file_obj: 文件对象
        chunk_size: 读取块大小，默认16MB
        
    Returns:
        文件的MD5值
    """
    md5_hash = hashlib.md5()
    
    # 保存当前位置
    current_pos = file_obj.tell()
    file_obj.seek(0)
    
    # 只读取前16MB用于计算MD5
    chunk = file_obj.read(chunk_size)
    if chunk:
        md5_hash.update(chunk)
    
    # 恢复文件位置
    file_obj.seek(current_pos)
    
    return md5_hash.hexdigest()


def is_video_file(filename: str, allowed_extensions: list) -> bool:
    """
    检查文件是否为支持的视频格式
    
    Args:
        filename: 文件名
        allowed_extensions: 允许的扩展名列表
        
    Returns:
        是否为支持的视频文件
    """
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_extensions


def ensure_upload_dir(upload_dir: str) -> Path:
    """
    确保上传目录存在
    
    Args:
        upload_dir: 上传目录路径
        
    Returns:
        上传目录的Path对象
    """
    upload_path = Path(upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    获取文件大小
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件大小（字节）
    """
    return os.path.getsize(file_path)
