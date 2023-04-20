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
import main

templates = Jinja2Templates(directory="public")
router = APIRouter()

@router.get('/admin', response_class=HTMLResponse)
async def admin_get(request: Request,
					access_token_cookie: str | None = Cookie(default=None),
					Authorize: AuthJWT = Depends()):

	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())

		#If user had admin right?
		if isAuth['admin_right'] == False:
			return RedirectResponse(url="/")

		user_money = return_user(isAuth['user']).money

		#If user auth?
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	return templates.TemplateResponse("adminPanel.html", {"request": request, 
															"IsAuth": isAuth['user'],
															"auth": auth,
															"money":user_money})