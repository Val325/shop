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
from utils import send_all_goods, return_product_by_id, add_to_cart
from utils import auth_jwt, set_money_user, return_user, get_cart, delete_cart
import main

templates = Jinja2Templates(directory="public")
router = APIRouter()

@router.get("/product/{id}")
def product_id_get(request: Request,
					id: int,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):

	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
		
		user = return_user(isAuth["user"])
		print("are user had money?", user.money)
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	data_product = return_product_by_id(id)
	print("product", data_product)
	return templates.TemplateResponse("showProduct.html", {"request": request,
															"id":data_product["id"],
															"header":data_product["header"],
															"description":data_product["description"],
															"name_image":data_product["name_image"],
															"path_image":data_product["path_image"],
															"price":data_product["price"],
															"IsAuth": isAuth['user'],
															"auth": auth,
															"money": user.money})

@router.post("/product/{id}")
def product_id_post(request: Request,
					id: int,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):

	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())

		user = return_user(isAuth["user"])
		print("are user had money?", user.money)
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	data_product = return_product_by_id(id)
	print("product", data_product)
	return templates.TemplateResponse("showProduct.html", {"request": request,
															"id":data_product["id"],
															"header":data_product["header"],
															"description":data_product["description"],
															"name_image":data_product["name_image"],
															"path_image":data_product["path_image"],
															"price":data_product["price"],
															"IsAuth": isAuth['user'],
															"auth": auth,
															"money": user.money})

#
# bying product
#

@router.get("/bying/{id}")
def bying_id_get(request: Request,
					id: int,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):
	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())

		user = return_user(isAuth["user"])
		print("are user had money?", user.money)

		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	data_product = return_product_by_id(id)
	print("product", data_product)

	

	return templates.TemplateResponse("showProduct.html", {"request": request,
															"id":data_product["id"],
															"header":data_product["header"],
															"description":data_product["description"],
															"name_image":data_product["name_image"],
															"path_image":data_product["path_image"],
															"price":data_product["price"],
															"IsAuth": isAuth['user'],
															"auth": auth,
															"money": user.money})

@router.post("/bying/{id}")
def bying_id_post(request: Request,
					id: int,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):
	data_product = return_product_by_id(id)
	print("product", data_product)
	
	#try:

	texts = send_all_goods()
	auth_jwt(Authorize, access_token_cookie)
	isAuth = json.loads(Authorize.get_jwt_subject())
		
	user = return_user(isAuth["user"])
	user_id = user.id
	print("userid:", user_id)

	data_cart = {
				"header":data_product['header'],
    			"description":data_product["description"],
    			"name_image":data_product["name_image"],
    			"path_image":data_product["path_image"],
    			"price":data_product["price"]
	}

	add_to_cart(user_id, data_cart)
	moneyAfterBying = user.money - data_product["price"]
	#set_money_user(user.user, moneyAfterBying)

	if moneyAfterBying < 0:
		moneyAfterBying = 0
		set_money_user(user.user, moneyAfterBying)
		return templates.TemplateResponse("fail.html", {"request": request,
													"id":data_product["id"],
													"header":data_product["header"],
													"description":data_product["description"],
													"name_image":data_product["name_image"],
													"path_image":data_product["path_image"],
													"price":data_product["price"],
													"money": user.money})

	if isAuth:
		auth = True
	#except:
	#	return RedirectResponse(url="/login")

	

	


	return templates.TemplateResponse("bying.html", {"request": request,
													"id":data_product["id"],
													"header":data_product["header"],
													"description":data_product["description"],
													"name_image":data_product["name_image"],
													"path_image":data_product["path_image"],
													"price":data_product["price"],
													"IsAuth": isAuth['user'],
													"auth": auth,
													"money": user.money})


@router.get("/byingcart")
def bying_id_post(request: Request,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):
	total_price = 0

	#try:

	auth_jwt(Authorize, access_token_cookie)
	isAuth = json.loads(Authorize.get_jwt_subject())
		
	user = return_user(isAuth["user"])
	user_id = user.id
	print("userid:", user_id)

	
	"""
	moneyAfterBying = user.money - data_product["price"]
	set_money_user(user.user, moneyAfterBying)
	"""


	cart = get_cart(user_id)

	for item in cart:
		total_price += item.price

	moneyAfterBying = user.money - total_price

	if moneyAfterBying < 0:
		moneyAfterBying = 0
		set_money_user(user.user, moneyAfterBying)
		return templates.TemplateResponse("fail.html", {"request": request,
														"money": user.money})
	set_money_user(user.user, moneyAfterBying)

	

	

	delete_cart(user_id)	

	if isAuth:
		auth = True
	#except:
	#	return RedirectResponse(url="/login")

	

	


	return templates.TemplateResponse("bying.html", {"request": request,
													"IsAuth": isAuth['user'],
													"auth": auth,
													"money": user.money})