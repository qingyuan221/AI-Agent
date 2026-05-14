from pydantic import BaseModel, Field
from typing import List

class MovieInfo(BaseModel):
    title: str = Field(..., description="电影名称")
    director: str = Field(..., description="导演姓名")
    rating: float = Field(..., ge=0, le=10, description="评分(0-10)")
    tags: List[str] = Field(default_factory=list, description="电影风格标签")
    summary: str = Field(..., min_length=10, description="不少于10个字的剧情简介")