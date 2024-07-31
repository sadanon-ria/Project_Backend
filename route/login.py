from fastapi import APIRouter, HTTPException, Cookie, Response
from pydantic import BaseModel
from passlib.context import CryptContext

import os
import jwt

from config.db import collection_userLogin
from models.models import userAccount
from schemas.schemas import loginUsers_serializer

login = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# add new user
@login.post("/singup", tags=["login"])
async def addUser(data: userAccount):
    checkUsername = collection_userLogin.find_one({"username": data.username})
    if (checkUsername):
        raise HTTPException(status_code=409, detail="Username already exists")
    else:
        hashed_password = pwd_context.hash(data.password)
        document = {"username":data.username, "password": hashed_password, "firstname": data.firstname,"lastname": data.lastname, "roles":data.roles}
        collection_userLogin.insert_one(document)
        return  {"status": "200 OK", "new_user": data.username}


def sign_token(username: str, firstname: str, lastname: str, roles: str) -> str:
    payload = {
        "UserInfo": {
            "username": username,
            "firstname": firstname,
            "lastname": lastname,
            "roles": roles
        },
        "exp": "1D"
    }
    token = jwt.encode(payload, "token secrets", algorithm="HS256")
    return token

class UserLogin(BaseModel):
    username: str
    password: str

# login
@login.post("/singin", tags=["login"])
async def handleLogin(data: UserLogin, response: Response):
    checkUsername = collection_userLogin.find_one({"username": data.username})
    if(not checkUsername):
        raise HTTPException(status_code=404, detail=f"User not found with username {data.username}")
    else:
        same = pwd_context.verify(data.password, checkUsername.get("password"))
        print(data)
        if (same):
            access_token = sign_token(data.username, checkUsername.get("firstname"), checkUsername.get("lastname"), checkUsername.get("roles"))
            response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="None", max_age=3600)
            return {"access_token": access_token, "username": data.username, "firstname":checkUsername.get("firstname"), "lastname":checkUsername.get("lastname"), "roles":checkUsername.get("roles")}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")
        

@login.post("/logout", tags=["login"])
async def handleLogout(response: Response):
    # Clear the access token cookie by setting its value to an empty string
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}
        
