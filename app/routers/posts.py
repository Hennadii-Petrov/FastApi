from typing import List
from fastapi import  status, HTTPException,APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends
from .. import schema, models
from ..database import get_db
from ..oauth2 import get_current_user


router = APIRouter(prefix="/posts", tags=["Posts"], redirect_slashes=False)

@router.get('', response_model=List[schema.PostWithVotes])
async def get_posts(db:Session = Depends(get_db), current_user: int = Depends(get_current_user), limit: int = 10, skip: int = 0, search: str = ""):

    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).limit(limit).offset(skip).all()
    
    return result

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
async def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
   
    new_post = models.Post(
       owner_id=current_user.id,  # Set the owner_id to current user
       **post.model_dump()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=schema.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:    
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    if post:
        db.delete(post)
        db.commit()
        return {"message": "Post deleted successfully"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.put('/{id}', response_model=schema.PostResponse)
def update_post(id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    
    # Fetch the updated post from database
    updated_post_obj = post_query.first()
    return updated_post_obj


