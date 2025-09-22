from pydantic import BaseModel
from typing import List, Optional, Union


class CommentRaw(BaseModel):
    """原始弹幕数据模型"""
    cid: int
    p: str  # 时间,类型,颜色,用户ID等信息，逗号分隔
    m: str  # 弹幕内容


class CommentN(BaseModel):
    """NPlayer弹幕格式"""
    color: Optional[str] = None  # 弹幕颜色
    text: str  # 弹幕文字
    time: float  # 弹幕出现时间
    type: Optional[str] = "scroll"  # 弹幕类型：top, bottom, scroll
    isMe: Optional[bool] = False  # 是否是当前用户发送的
    force: Optional[bool] = False  # 是否强制展示该弹幕


class CommentArt(BaseModel):
    """ArtPlayer弹幕格式"""
    text: str  # 弹幕文本
    time: float  # 发送时间，单位秒
    color: Optional[str] = None  # 弹幕局部颜色
    border: Optional[bool] = False  # 是否显示描边
    mode: int  # 弹幕模式: 0表示滚动、1静止


class CommentCCL(BaseModel):
    """CCL弹幕格式"""
    text: str
    stime: int  # 时间，毫秒
    color: int
    mode: int
    size: int


class CommentResult(BaseModel):
    """弹幕查询结果"""
    count: int
    comments: List[CommentRaw]
    errorCode: Optional[int] = None
    success: Optional[bool] = True
    errorMessage: Optional[str] = None


class ExtCommentRequest(BaseModel):
    """外部弹幕请求"""
    url: str


class XMLCommentRequest(BaseModel):
    """XML弹幕请求"""
    xml_content: str
