from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from ..models.match import MatchRequest, MatchResult
from ..models.comment import CommentResult, ExtCommentRequest, XMLCommentRequest
from ..services.dandan_service import dandan_service
from ..utils.comment_utils import parse_xml_comments

router = APIRouter()


@router.post("/match", response_model=MatchResult)
async def match_video(request: MatchRequest):
    """
    匹配视频信息
    """
    try:
        result = await dandan_service.match_video(request)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"匹配失败: {str(e)}"
        )


@router.get("/comment/{episode_id}", response_model=CommentResult)
async def get_comments(
    episode_id: int,
    with_related: Optional[str] = Query(None, alias="withRelated"),
    ch_convert: Optional[str] = Query(None, alias="chConvert"),
    from_source: Optional[str] = Query(None, alias="from")
):
    """
    获取弹幕数据
    """
    try:
        with_related_bool = with_related == "true" if with_related else True
        result = await dandan_service.get_comments(episode_id, with_related_bool)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取弹幕失败: {str(e)}"
        )


@router.get("/extcomment/", response_model=CommentResult)
async def get_external_comments(url: str = Query(...)):
    """
    获取外部弹幕数据
    """
    try:
        result = await dandan_service.get_external_comments(url)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取外部弹幕失败: {str(e)}"
        )


@router.post("/xml-comment", response_model=CommentResult)
async def parse_xml_comment(request: XMLCommentRequest):
    """
    解析XML格式弹幕
    """
    try:
        comments = parse_xml_comments(request.xml_content)
        return CommentResult(
            count=len(comments),
            comments=comments,
            success=True
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"XML弹幕解析失败: {str(e)}"
        )
