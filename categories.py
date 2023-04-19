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
from DB import engine, products, users, return_user
from utils import send_all_goods, return_product_by_id
from utils import auth_jwt, set_money_user

templates = Jinja2Templates(directory="public")
router = APIRouter()

@router.get("/Categories/{category}")
def get_data(request: Request,
				category: str, 
				post: Optional[str] = Form(None), 
				file: Optional[UploadFile] = File(None),
				price: Optional[str] = Form(None), 
				headerProduct: Optional[str] = Form(None),
				access_token_cookie: str | None = Cookie(default=None),
				Authorize: AuthJWT = Depends()):


	try:
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	name_image = uuid.uuid1()
	texts = send_all_goods()
	
	#для отправки header auth
	if (post and price and headerProduct) == None:
		return templates.TemplateResponse("category.html", {"request": request, 
															"texts": texts, 
															"IsAuth": isAuth['user'],
															"auth": auth,
															"category":category})

	with Session(autoflush=False, bind=engine) as db:
		product = products(description=post,
							header=headerProduct, 
							name_image=name_image,
							path_image="/",
							price=price)
		db.add(product)     
		db.commit()     
    
	with open(str(Path(__file__).parent.absolute()) +"/static" + "/uploads/" + str(name_image) +".png", "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)

	return templates.TemplateResponse("category.html", {"request": request, 
													"filename": file.filename, 
													"IsAuth": isAuth['user'],
													"auth": auth,
													"category":category})

@router.get("/Categories/{category}")
def get_data(request: Request,
				category: str, 
				post: Optional[str] = Form(None), 
				file: Optional[UploadFile] = File(None),
				price: Optional[str] = Form(None), 
				headerProduct: Optional[str] = Form(None),
				access_token_cookie: str | None = Cookie(default=None),
				Authorize: AuthJWT = Depends()):


	try:
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	name_image = uuid.uuid1()
	texts = send_all_goods()
	
	#для отправки header auth
	if (post and price and headerProduct) == None:
		return templates.TemplateResponse("index.html", {"request": request, 
															"texts": texts, 
															"IsAuth": isAuth['user'],
															"auth": auth})

	with Session(autoflush=False, bind=engine) as db:
		product = products(description=post,
							header=headerProduct, 
							name_image=name_image,
							path_image="/",
							price=price)
		db.add(product)     
		db.commit()     
    
	with open(str(Path(__file__).parent.absolute()) +"/static" + "/uploads/" + str(name_image) +".png", "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)

	return templates.TemplateResponse("category.html", {"request": request, 
													"filename": file.filename, 
													"IsAuth": isAuth['user'],
													"auth": auth,
													"category":category})