from fastapi import FastAPI, Query, Body, status, Form
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse, Response
from fastapi.responses import JSONResponse, FileResponse
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, ForeignKey, ARRAY
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

engine = create_engine("postgresql://postgres:Hamachi2002@localhost/fastapiDB")
class Base(DeclarativeBase): pass

class products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    description = Column(String)
    name_image = Column(String)
    path_image = Column(String)
    path_url = Column(String)
    type_product = Column(String)
    price = Column(Integer)

class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    password = Column(String)
    admin = Column(Boolean, unique=False, default=False)
    money = Column(Integer)

class basketUsers(Base):
    __tablename__ = "baskets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(users.id))
    header = Column(ARRAY(String()), default=[])
    description = Column(ARRAY(String()), default=[])
    name_image = Column(ARRAY(String()), default=[])
    path_image = Column(ARRAY(String()), default=[])
    price = Column(ARRAY(String()), default=[])


Base.metadata.create_all(bind=engine)

