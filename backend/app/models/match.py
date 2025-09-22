from pydantic import BaseModel
from typing import List, Optional


class Match(BaseModel):
    """匹配结果模型"""
    episodeId: int
    animeId: int
    animeTitle: str
    episodeTitle: str
    type: str
    typeDescription: str
    shift: int


class MatchRequest(BaseModel):
    """匹配请求模型"""
    fileName: str
    fileHash: str
    fileSize: int
    videoDuration: Optional[int] = None
    matchMode: Optional[str] = None


class MatchResult(BaseModel):
    """匹配结果响应"""
    isMatched: bool
    matches: List[Match]
    errorCode: Optional[int] = None
    success: Optional[bool] = True
    errorMessage: Optional[str] = None
