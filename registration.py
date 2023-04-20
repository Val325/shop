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
from utils import auth_jwt, set_money_user, return_user, validation_registration
import main

templates = Jinja2Templates(directory="public")
router = APIRouter()

@router.get('/registration', response_class=HTMLResponse)
async def main(request: Request):
	return templates.TemplateResponse("registration.html", {"request": request})

@router.post('/registration', response_class=HTMLResponse)
async def login_post(request: Request, 
						Password = Form(), 
						Username = Form()):
	print("Password")
	print("Username:", Username)
	print("Password:", Password)

	isNotValidated = validation_registration(Password)


	#If password is less then 6 symbols and if return_user return use you get a error
	if isNotValidated or (return_user(Username) != None):
		return templates.TemplateResponse("registration.html", {"request": request,
																"isNotValidated":isNotValidated})

	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(Password.encode('utf-8'), salt).decode('utf8')

	print("salt", salt)
	print("Hashed:", hashed)
	with Session(autoflush=False, bind=engine) as db:
		
		data_user = users(user=Username, password=hashed,money=100)
		db.add(data_user)     
		db.commit()     
		
	return RedirectResponse(url="/login")
	#