from typing import List,Optional
from ..import models,schemas,oauth2
from sqlalchemy.orm import session
from fastapi import Depends,HTTPException,status,Response,APIRouter
from ..database import get_db
from sqlalchemy import func



router=APIRouter(
    prefix="/post",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
              Limit:int=10,skip:int=0,search:Optional[str]=""):
    


    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id). label("votes")).join(models.Vote, 
                    models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    
    print(current_user.email)
    return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.Postcreate,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
   
   new_post=models.Post(owner_id=current_user.id,**post.dict())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
  
  # post= db.query(models.Post).filter(models.Post.id==id).first()
    
     
  post  = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()

  if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
  return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    delete_post=db.query(models.Post).filter(models.Post.id==id)
    post=delete_post.first()
   
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} doenot exist")
    
    if post.owner_id != current_user.id :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorize to perform requested action")
    
    delete_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.Postcreate,db:session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    print("updated post entry")
    post_query= db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} doesnot exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorize to perform requested action")    
        
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
