from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db
router = APIRouter(
    prefix = "/votes",
    tags = ["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteReturn)
def addVote(vote: schemas.VoteCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    try:
        newVote = models.Vote(user_id=current_user.id, **vote.model_dump())
        db.add(newVote)
        db.commit()
        db.refresh(newVote)
        return newVote
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Either post with ID {vote.post_id} doesn't exist or user has already voted on it before")

    
@router.put("/", response_model=schemas.VoteReturn)
def editVote(vote: schemas.VoteCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    current_vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    current_vote = current_vote_query.first()
    
    if not current_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote of user {current_user.id} and post {vote.post_id} you are trying to edit does not exist")
    
    newVoteAsDict = vote.model_dump()
    newVoteAsDict['user_id'] = current_user.id
    current_vote_query.update(newVoteAsDict, synchronize_session=False)
    db.commit()

    return current_vote_query.first()