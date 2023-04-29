from fastapi import FastAPI,HTTPException,status,APIRouter,Depends
from sqlalchemy.orm import Session
from ..import database,schemas,models,utils,oauth2

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(tags=['Authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user= db.query(models.User).filter(models.User.email==user_credential.username).first()
    if not user:
      return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")

    if not utils.verify(user_credential.password,user.password):
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")

    # create a token, return a token

    access_token=oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token": access_token,"token_type":"bearer"} 
