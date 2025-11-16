from typing import List
from fastapi import HTTPException,APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from .. import schema, models
from ..database import get_db
from ..oauth2 import get_current_user


router = APIRouter(prefix="/votes", tags=["Votes"], redirect_slashes=False)

@router.post('/', status_code=201)
def vote(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=409, detail="You have already voted on this post")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully"}
    
@router.get('/', response_model=List[schema.VoteResponse])
def get_votes(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    votes = db.query(models.Vote).filter(models.Vote.user_id == current_user.id).all()
    return votes