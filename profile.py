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
from utils import send_all_goods, return_product_by_id, count_cart
from utils import auth_jwt, set_money_user, return_user
import main

templates = Jinja2Templates(directory="public")
router = APIRouter()

@router.get("/profile")
def profile(request: Request, 
			access_token_cookie: str | None = Cookie(default=None), 
			Authorize: AuthJWT = Depends()):

	try:
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
		print("userdata", isAuth["user"])
		user = return_user(isAuth["user"])
		print("are user had money?", user.money)

		amount_court = count_cart(user.id)
		print("user:", user.user)
		print("money:", user.money)
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")


	return templates.TemplateResponse("profile.html", {"request": request, 
														"IsAuth": isAuth['user'],
														"auth": auth,
														"user": user.user,
														"money": user.money,
														"admin_right":isAuth['admin_right'],
														"count_cart":amount_court})



@router.post("/profile")
def profile(request: Request, 
			access_token_cookie: str | None = Cookie(default=None), 
			Authorize: AuthJWT = Depends(), 
			money = Form()):

	try:
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
		print("userdata", isAuth["user"])
		user = return_user(isAuth["user"])
		print("are user had money?", user.money)

		amount_court = count_cart(user.id)
		print("user:", user.user)
		print("money:", user.money)
		print("money_set:", money)

		moneyAfterGetMoney = int(user.money) + int(money)
		set_money_user(user.user, moneyAfterGetMoney)


		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")


	return templates.TemplateResponse("profile.html", {"request": request, 
														"IsAuth": isAuth['user'],
														"auth": auth,
														"user": user.user,
														"money": user.money,
														"IsAuth": isAuth['user'],
														"auth": auth,
														"count_cart":amount_court})