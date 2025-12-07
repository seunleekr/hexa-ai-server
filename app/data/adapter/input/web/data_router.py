from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.data.adapter.input.web.request.create_data_request import (
    CrawlingIngestRequest,
)
from app.data.adapter.input.web.response.data_response import DataResponse
from config.database import get_db

data_router = APIRouter()


@data_router.post(
    "/",
    response_model=List[DataResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_data_from_crawling(
    request: CrawlingIngestRequest, db: Session = Depends(get_db)
):
    """
    크롤링/분석 API 결과에 포함된 analysis 내용을 DB에 저장
    """
    items_to_save: List[dict] = []
    for article in request.articles:
        analysis = article.analysis
        title = analysis.title.strip()
        content = analysis.content.strip()
        keywords = [
            keyword.strip()
            for keyword in analysis.keywords
            if isinstance(keyword, str) and keyword.strip()
        ]

        if not title or not content:
            continue

        # published_at이 필수 필드이므로, 없으면 빈 문자열로 처리
        published_at = ""
        if hasattr(analysis, 'published_at') and analysis.published_at:
            published_at = analysis.published_at
        
        items_to_save.append(
            {
                "title": title,
                "content": content,
                "keywords": keywords,
                "published_at": published_at,
            }
        )

    if not items_to_save:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="저장 가능한 분석 데이터가 없습니다.",
        )

    return _create_data_items(items_to_save, db)

