from fastapi import FastAPI, HTTPException, status, Response, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags=["Posts"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostReturn)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    newPost = models.Post(**post.model_dump(), owner_id= current_user.id)
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    return newPost

@router.get("/", response_model=List[schemas.PostReturn])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/{id}", response_model=schemas.PostReturn)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with ID {id} was not found.")

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"post with ID {id} was not found so it was not deleted.") 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Post with ID {id} doesn't belong to the current user to delete it.")
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostReturn)
def update_post(newPost: schemas.PostCreate, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"post with ID {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Post with ID {id} doesn't belong to the current user to edit it.")
    post_query.update(newPost.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()  

# while True:
#     try:
#         DBconnection = psycopg.connect(host='localhost', dbname='postgres', user='postgres', password='password', row_factory=dict_row)
#         cursor = DBconnection.cursor()
#         break
#     except Exception as DBconnectionError:
#         print("Connection to the db has failed")
#         time.sleep(2)


# def findPostByID(ID):
#     cursor.execute("""SELECT * FROM "fastAPI"."socialMediaApp" WHERE id = %s""", (ID,))
#     return cursor.fetchone()
# 
# def editPostByID(ID, newPost):
#     newTitle = newPost.title
#     newContent = newPost.content
#     cursor.execute("""UPDATE "fastAPI"."socialMediaApp" SET title = %s, content = %s WHERE id = %s RETURNING *""", (newTitle, newContent, ID))
#     DBconnection.commit()
#     return cursor.fetchone()
# 
# def deletePostByID(ID):
#     cursor.execute("""DELETE FROM "fastAPI"."socialMediaApp" WHERE id = %s RETURNING *""", (ID,))
#     DBconnection.commit()
#     return cursor.fetchone()
# 
# @socialMediaApp.get("/orm")
# def test_orm(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"posts": posts}

    
# @socialMediaApp.post("/posts", status_code=status.HTTP_201_CREATED)
# def createPost(post: Post):
#     cursor.execute("""INSERT INTO "fastAPI"."socialMediaApp" (title, content) VALUES (%s, %s) RETURNING *""",
#                    (post.title, post.contenct))
#     newPost = cursor.fetchone()
#     DBconnection.commit()
#     return newPost

# @socialMediaApp.post("/posts", status_code=status.HTTP_201_CREATED)
# def createPost(post: Post, db: Session = Depends(get_db)):
#     newPost = models.Post(title=post.title, content=post.content)
#     return newPost
# 



# @socialMediaApp.get("/posts")
# def getPosts():
#     posts = cursor.execute("""SELECT * FROM "fastAPI"."socialMediaApp" ORDER BY id ASC""").fetchall()
#     return {"data": posts}


    

# @socialMediaApp.get("/posts/{id}")
# def getPostByID(id: int):
#     post = findPostByID(id)
#     if post:
#         return post
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with ID {id} was not found.")



       
# @socialMediaApp.delete("/posts/{id}")
# def deletePost(id: int):
#     post = deletePostByID(id)
#     if post:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f"post with ID {id} was not found so it was not deleted.")


   
# @socialMediaApp.put("/posts/{id}")
# def updatePost(newPost: Post,id: int):
#     editedPost = editPostByID(id, newPost)
#     if editedPost:
#         return editedPost
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f"post with ID {id} was not found")

