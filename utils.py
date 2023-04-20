from fastapi import FastAPI, Query, Body, status, Form
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

def send_all_goods():
	texts = None

	with Session(autoflush=False, bind=engine) as db:
		texts = db.query(products).all()

	return texts	

#Return product by id
def return_product_by_id(id):
	product = None

	with Session(autoflush=False, bind=engine) as db:
		try:
			product = db.query(products).filter(products.id==id).one_or_none()
		except AttributeError:
		    print("product not finded")

	return {"id":product.id, 
			"header":product.header, 
			"description":product.description,
			"name_image":product.name_image,
			"path_image":product.path_image,
			"price":product.price}

def auth_jwt(Authorize, access_token_cookie):

	
	Authorize.jwt_required()
	

	return None

def return_user(user):
	with Session(autoflush=False, bind=engine) as db:
		try:
			user = db.query(users).filter(users.user==user).one_or_none()

		except AttributeError:
		    print("user not finded")
	print(user)
	return user

def set_money_user(user, num_money):
	with Session(autoflush=False, bind=engine) as db:
		try:
			userDB = db.query(users).filter(users.user==user).one_or_none()
			userDB.money = num_money
			db.commit()
		except AttributeError:
		    print("user not finded")
	print(user)
	return user

def send_filter_goods_type_product(type_product):
	texts = None

	with Session(autoflush=False, bind=engine) as db:
		texts = db.query(products).filter(products.type_product == type_product)

	return texts

def validation_registration(symbols):
	if len(symbols) < 7:
		print("Пароль должен быть больше 6ти символов")
		return True
	else:
		print("Пароль правильный")
		return False