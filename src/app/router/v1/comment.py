from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.common.utils.dependency import get_current_user, get_session
from src.app.v1.comment.schema.requestDto import CommentCreateRequest
from src.app.v1.comment.schema.responseDto import (
    CommentCreateResponse,
    CommentListResponse,
)
from src.app.v1.comment.service.comment_service import CommentService

router = APIRouter(prefix="/comments", tags=["Comments"])
comment_service = CommentService()


@router.post("/write/{post_id}", response_model=CommentCreateResponse)
async def create_comment(
    post_id: str,
    payload: CommentCreateRequest,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    try:
        actual_post_id = await comment_service.get_post_id_from_external_id(session, post_id)
        return await comment_service.create_comment_with_tags(
            session=session,
            post_id=actual_post_id,
            author_id=current_user["user_id"],            
            payload=payload,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{post_id}", response_model=CommentListResponse)
async def get_comments(
    post_id: str,
    session: AsyncSession = Depends(get_session),
):
    try:
        actual_post_id = await comment_service.get_post_id_from_external_id(session, post_id)
        comments = await comment_service.get_comments_with_tags(session, actual_post_id)
        return {"comments": comments, "total_count": len(comments)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    try:
        await comment_service.delete_comment(session, comment_id, current_user["user_id"])
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
