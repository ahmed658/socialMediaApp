from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db
router = APIRouter(
    prefix = "/votes",
    tags = ["Votes"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteReturn)
def submitVote(vote: schemas.VoteCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    current_vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    current_vote = current_vote_query.first()
    try:
        if not current_vote:
            newVote = models.Vote(user_id=current_user.id, **vote.model_dump())
            db.add(newVote)
            db.commit()
            db.refresh(newVote)
            return newVote
        if current_vote.vote_dir == vote.vote_dir:
            return current_vote
        newVoteAsDict = vote.model_dump()
        newVoteAsDict['user_id'] = current_user.id
        current_vote_query.update(newVoteAsDict, synchronize_session=False)
        db.commit()
        return current_vote_query.first()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {vote.post_id} doesn't exist")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def deleteVote(vote: schemas.Vote, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    current_vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    current_vote = current_vote_query.first()
    if not current_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote of post with ID {vote.post_id} doesn't exist")
    current_vote_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
#@router.put("/", response_model=schemas.VoteReturn)
#def editVote(vote: schemas.VoteCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
#    current_vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
#    current_vote = current_vote_query.first()
#    
#    if not current_vote:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote of user {current_user.id} and post {vote.post_id} you are trying to edit does not exist")
#    
#    newVoteAsDict = vote.model_dump()
#    newVoteAsDict['user_id'] = current_user.id
#    current_vote_query.update(newVoteAsDict, synchronize_session=False)
#    db.commit()
#
#    return current_vote_query.first()