from jose import JWTError,jwt
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from .import schemas,database,models
from sqlalchemy.orm import session
from .config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')



# secret_key
# Algorithm
# Expriation Time

Secret_key=settings.secret_key
Algorith=settings.algorithm
Access_token_expiry_minutes=settings.access_token_expiry_minutes

def create_access_token(data:dict):
    to_encode=data.copy()
    expiry=datetime.utcnow()+timedelta(minutes=Access_token_expiry_minutes)
    to_encode.update({"exp":expiry})
    encoded_jwt=jwt.encode(to_encode,Secret_key,algorithm=Algorith)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        payload= jwt.decode(token,Secret_key,algorithms=[Algorith])
        id:str=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:session=Depends(database.get_db)):
    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"couldnot validate credentials",headers={"www-Authenticate":"Bearer"})
    
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
  
    return user


