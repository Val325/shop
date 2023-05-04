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
from utils import send_all_goods, return_product_by_id, get_cart
from utils import auth_jwt, set_money_user, return_user

templates = Jinja2Templates(directory="public")
router = APIRouter()

@router.get('/shopcart', response_class=HTMLResponse)
async def main(response: Response,
				request: Request, 
				access_token_cookie: str | None = Cookie(default=None), 
				Authorize: AuthJWT = Depends()):

	user_money = None
	admin_right = None
	

	auth_jwt(Authorize, access_token_cookie)
	isAuth = json.loads(Authorize.get_jwt_subject())

	user = return_user(isAuth['user'])
	user_money = user.money

	if isAuth:
		auth = True

	if isAuth["admin_right"]:
		admin_right = True
	
	print('cart', get_cart(user.id))

	cart = get_cart(user.id)

	for item in cart:
		print('id:', item.id)
		print('header:', item.header)

	return templates.TemplateResponse("shopcart.html", {"request": request,
														"IsAuth": isAuth['user'],
														"auth": auth,
														"money":user_money,
														"admin_right":admin_right,
														"cart": cart})