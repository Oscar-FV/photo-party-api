import os
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List

from app.core.db import get_db
from app.core.security import get_current_user
from app.services.posts.models import Post
from app.services.posts.repository import (
    create_post,
    get_all_event_posts,
    get_posts_by_quest,
    get_posts_by_user,
)
from app.services.posts.schemas import PostCreate, PostLK, PostLKWithPagination, PostRespone, PostUserInfo, PostUserInfoWithPagination
from app.services.users.schemas import CurrentUser


router = APIRouter()


@router.post("", response_model=PostRespone)
async def create_post_route(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return create_post(db, post.dict(), current_user.user.id)


@router.post("/image", response_model=str)
async def save_image(
    file: UploadFile = File(...), current_user: CurrentUser = Depends(get_current_user)
):
    try:
        file_extension = file.filename.split(".")[-1]
        if file_extension not in ("png", "jpg", "jpeg", "JPEG", "jfif", "gif", "heic", "heif", "webp"):
            raise HTTPException(status_code=400, detail="Invalid file format")

        image_filename = f"{uuid.uuid4()}.{file_extension}"
        image_path = os.path.join("uploads/", image_filename)

        with open(image_path, "wb") as image:
            content = await file.read()
            image.write(content)
        image_url = f"/uploads/{image_filename}"

        return image_url

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error uploading file")


@router.get("", response_model=PostUserInfoWithPagination)
async def get_event_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return get_all_event_posts(db, current_user.event_id, skip, limit)


@router.get("/user-posts", response_model=PostLKWithPagination)
async def get_user_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return get_posts_by_user(db, current_user.user.id, skip, limit)


@router.get("/quest-posts/{quest_id}", response_model=PostUserInfoWithPagination)
async def get_quest_posts(
    quest_id: uuid.UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return get_posts_by_quest(db, quest_id, skip, limit)
