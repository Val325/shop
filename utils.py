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
from DB import engine, products, users, basketUsers

def send_all_goods():
	texts = None

	with Session(autoflush=False, bind=engine) as db:
		texts = db.query(products).all()

	return texts

def send_all_users():
	total_users = []
	users_array = []
	users_id = []

	with Session(autoflush=False, bind=engine) as db:
		users_all = db.query(users).all()
		for data_user in users_all:
			users_array.append(data_user.user)
			users_id.append(data_user.id)

			total_users.append({"id": int(data_user.id),
							"user": str(data_user.user)})

	
	return total_users


def return_user_by_id(id):
	with Session(autoflush=False, bind=engine) as db:
		try:
			user = db.query(users).filter(users.id==id).one_or_none()
			return {'id':user.id,'user': user.user}
		except AttributeError:
		    return {'error': 'user not found'}

def return_user_by_user(user):
	with Session(autoflush=False, bind=engine) as db:
		
		try:
		
			user = db.query(users).filter(users.user==user).one_or_none()
			return {'id':user.id,'user': user.user}
		
		except AttributeError:
		    return {'error': 'user not found'}
		

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
		print("Password bigger then 7 symbols")
		return True
	else:
		print("Password correct")
		return False

def is_user_exists(user):
	pass


def add_to_cart(user, data):
	with Session(autoflush=False, bind=engine) as db:
		
		data_user = basketUsers(user_id=user,
    							header=header.append(data.header),
    							description=description.append(data.description),
    							name_image=name_image.append(data.name_image),
    							path_image=path_image.append(data.path_image),
    							price=price.append(data.price))
		db.add(data_user)     
		db.commit()


def get_cart(id_user):
	with Session(autoflush=False, bind=engine) as db:
		try:
			basket = db.query(basketUsers).filter(basketUsers.user_id==id_user).one_or_none()

		except AttributeError:
		    print("basket not finded")
	return basket