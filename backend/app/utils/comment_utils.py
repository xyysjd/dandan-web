import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from ..models.comment import CommentRaw, CommentN, CommentArt, CommentCCL


def dandan_to_nplayer(comment: CommentRaw) -> CommentN:
    """
    将弹弹play格式弹幕转换为NPlayer格式
    
    Args:
        comment: 原始弹幕数据
        
    Returns:
        NPlayer格式弹幕
    """
    p_parts = comment.p.split(',')
    time = float(p_parts[0])
    comment_type = int(p_parts[1])
    color = int(p_parts[2])
    
    # 类型映射
    type_map = {
        1: 'scroll',
        4: 'bottom',
        5: 'top'
    }
    
    return CommentN(
        color=f"{color:06x}",
        text=comment.m,
        time=time,
        type=type_map.get(comment_type, 'scroll')
    )


def dandan_to_artplayer(comment: CommentRaw) -> CommentArt:
    """
    将弹弹play格式弹幕转换为ArtPlayer格式
    
    Args:
        comment: 原始弹幕数据
        
    Returns:
        ArtPlayer格式弹幕
    """
    p_parts = comment.p.split(',')
    time = float(p_parts[0])
    comment_type = int(p_parts[1])
    color = int(p_parts[2])
    
    # 模式映射
    mode_map = {
        1: 0,  # 滚动
        4: 1,  # 静止
        5: 1   # 静止
    }
    
    return CommentArt(
        color=f"{color:06x}",
        text=comment.m,
        time=time,
        mode=mode_map.get(comment_type, 0)
    )


def dandan_to_ccl(comment: CommentRaw) -> CommentCCL:
    """
    将弹弹play格式弹幕转换为CCL格式
    
    Args:
        comment: 原始弹幕数据
        
    Returns:
        CCL格式弹幕
    """
    p_parts = comment.p.split(',')
    stime = int(float(p_parts[0]) * 1000)  # 转换为毫秒
    comment_type = int(p_parts[1])
    color = int(p_parts[2])
    
    return CommentCCL(
        color=color,
        text=comment.m,
        stime=stime,
        mode=comment_type,
        size=25
    )


def parse_xml_comments(xml_content: str) -> List[CommentRaw]:
    """
    解析XML格式弹幕（B站格式）
    
    Args:
        xml_content: XML弹幕内容
        
    Returns:
        解析后的弹幕列表
    """
    try:
        root = ET.fromstring(xml_content)
        comments = []
        
        for i, d_elem in enumerate(root.findall('d')):
            p_attr = d_elem.get('p', '')
            text = d_elem.text or ''
            
            # 处理p属性，格式：时间,类型,大小,颜色,时间戳,池,用户ID,弹幕ID
            # 转换为弹弹play格式：时间,类型,颜色,0
            if p_attr and text:
                p_parts = p_attr.split(',')
                if len(p_parts) >= 4:
                    time = p_parts[0]
                    comment_type = p_parts[1]
                    color = p_parts[3]
                    
                    # 重新组装p属性
                    new_p = f"{time},{comment_type},{color},0"
                    
                    comments.append(CommentRaw(
                        cid=i,
                        p=new_p,
                        m=text.strip()
                    ))
        
        return comments
        
    except ET.ParseError as e:
        raise ValueError(f"XML解析错误: {str(e)}")
    except Exception as e:
        raise ValueError(f"弹幕解析失败: {str(e)}")
