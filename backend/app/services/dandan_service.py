import httpx
from typing import Dict, Any, Optional
from ..core.config import settings
from ..models.match import MatchRequest, MatchResult, Match
from ..models.comment import CommentResult, CommentRaw


class DanDanService:
    """弹弹play API服务"""
    
    def __init__(self):
        self.base_url = settings.dandan_proxy_url
        self.timeout = 30.0
    
    async def match_video(self, match_request: MatchRequest) -> MatchResult:
        """
        匹配视频信息
        
        Args:
            match_request: 匹配请求参数
            
        Returns:
            匹配结果
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/match",
                    json=match_request.dict()
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('success', True):
                    matches = [Match(**match) for match in data.get('matches', [])]
                    return MatchResult(
                        isMatched=data.get('isMatched', False),
                        matches=matches,
                        success=True
                    )
                else:
                    return MatchResult(
                        isMatched=False,
                        matches=[],
                        success=False,
                        errorMessage=data.get('errorMessage', '匹配失败')
                    )
                    
            except httpx.HTTPError as e:
                return MatchResult(
                    isMatched=False,
                    matches=[],
                    success=False,
                    errorMessage=f"网络请求失败: {str(e)}"
                )
            except Exception as e:
                return MatchResult(
                    isMatched=False,
                    matches=[],
                    success=False,
                    errorMessage=f"匹配失败: {str(e)}"
                )
    
    async def get_comments(self, episode_id: int, with_related: bool = True) -> CommentResult:
        """
        获取弹幕数据
        
        Args:
            episode_id: 剧集ID
            with_related: 是否包含相关弹幕
            
        Returns:
            弹幕数据
        """
        params = {}
        if with_related:
            params['withRelated'] = 'true'
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/comment/{episode_id}",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('success', True):
                    comments = [CommentRaw(**comment) for comment in data.get('comments', [])]
                    return CommentResult(
                        count=data.get('count', 0),
                        comments=comments,
                        success=True
                    )
                else:
                    return CommentResult(
                        count=0,
                        comments=[],
                        success=False,
                        errorMessage=data.get('errorMessage', '获取弹幕失败')
                    )
                    
            except httpx.HTTPError as e:
                return CommentResult(
                    count=0,
                    comments=[],
                    success=False,
                    errorMessage=f"网络请求失败: {str(e)}"
                )
            except Exception as e:
                return CommentResult(
                    count=0,
                    comments=[],
                    success=False,
                    errorMessage=f"获取弹幕失败: {str(e)}"
                )
    
    async def get_external_comments(self, url: str) -> CommentResult:
        """
        获取外部弹幕数据
        
        Args:
            url: 第三方弹幕站URL
            
        Returns:
            弹幕数据
        """
        params = {'url': url}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/extcomment/",
                    params=params
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('success', True):
                    comments = [CommentRaw(**comment) for comment in data.get('comments', [])]
                    return CommentResult(
                        count=data.get('count', 0),
                        comments=comments,
                        success=True
                    )
                else:
                    return CommentResult(
                        count=0,
                        comments=[],
                        success=False,
                        errorMessage=data.get('errorMessage', '获取外部弹幕失败')
                    )
                    
            except httpx.HTTPError as e:
                return CommentResult(
                    count=0,
                    comments=[],
                    success=False,
                    errorMessage=f"网络请求失败: {str(e)}"
                )
            except Exception as e:
                return CommentResult(
                    count=0,
                    comments=[],
                    success=False,
                    errorMessage=f"获取外部弹幕失败: {str(e)}"
                )


# 全局服务实例
dandan_service = DanDanService()
