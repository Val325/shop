from fastapi import FastAPI, Query, Body, status, Form, APIRouter
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.responses import JSONResponse, FileResponse
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy import  Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi import Request, File, UploadFile, Cookie
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
import uuid
import shutil
import jwt
import bcrypt
from datetime import datetime, timedelta
import json
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
import time
from typing import Optional
import uuid
from DB import engine, products, users
from utils import send_all_goods, return_product_by_id
from utils import auth_jwt, set_money_user, return_user

templates = Jinja2Templates(directory="public")
router = APIRouter()

@router.get('/login', response_class=HTMLResponse)
async def login_get(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})



@router.post('/login')
async def login_post(request: Request, 
					response: Response, 
					Password = Form(), 
					Username = Form(), 
					Authorize: AuthJWT = Depends()):
	print("login")
	print("Username:", Username)
	print("Password:", Password)

	expires = timedelta(days=7)
	response = None

	with Session(autoflush=False, bind=engine) as db:
		try:
			userDB = db.query(users).filter(users.user==Username).one_or_none()
			print(f"{userDB.id}.{userDB.user} ({userDB.password})")

			

			print("money user", userDB.money)

			data_jwt_save = json.dumps({"user":userDB.user, "admin_right":userDB.admin})
			
			IsAuthBool = bcrypt.checkpw(Password.encode('utf-8'), userDB.password.encode('utf8'))
			print("Is password correct?", IsAuthBool)

			if IsAuthBool:
				# Create the tokens and passing to set_access_cookies or set_refresh_cookies
				access_token = Authorize.create_access_token(subject=data_jwt_save,expires_time=expires)
				refresh_token = Authorize.create_refresh_token(subject=data_jwt_save,expires_time=expires)
				# Set the JWT cookies in the response
		
		
				response = RedirectResponse(url="/")
				Authorize.set_access_cookies(access_token, response) 
				Authorize.set_refresh_cookies(refresh_token, response)
				
				return response
				
			
			
		except AttributeError:
		    print("User not finded")

	

	return templates.TemplateResponse("login.html", {"request": request})