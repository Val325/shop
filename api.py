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
from utils import send_all_goods, return_product_by_id, send_all_users, return_user_by_user
from utils import auth_jwt, set_money_user, return_user, return_user_by_id

templates = Jinja2Templates(directory="public")
router = APIRouter()

@router.get('/api/users')
async def get_all_users(response: Response):
	users = send_all_users()
	print('users', users)
	return {"users":users}

@router.get('/api/users/{id}')
async def get_id_users(response: Response, id: int):
	try:
		user = return_user_by_id(id)
		return user
	except IndexError:
		return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "error": "Out from range" }
        )

@router.get('/api/users/name/{user}')
async def get_id_users(response: Response, user: str):
	try:
		user = return_user_by_user(user)
		return user
	except IndexError:
		return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "error": "Out from range" }
        )

@router.get('/api/products')
async def get_all_products(response: Response):
	products = send_all_goods()
	return {"products":products}

@router.get('/api/products/{id}')
async def get_id_products(response: Response, id: int):
	try:
		products = send_all_goods()
		return products[id]
	except IndexError:
		return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={ "error": "Out from range" }
        )

