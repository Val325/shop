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
from utils import send_all_goods, return_product_by_id
from utils import auth_jwt, set_money_user, return_user

import main
import adminPanel
import productsShop
import profile
import registration
import logout 
import categories
import login
import choice
import api
import shopcart

app = FastAPI()
secret_jwt = "4d398bd652db815963be16eb60638b9cc3c70096"

app.include_router(main.router)
app.include_router(adminPanel.router)
app.include_router(productsShop.router)
app.include_router(profile.router)
app.include_router(registration.router)
app.include_router(logout.router)
app.include_router(categories.router)
app.include_router(login.router)
app.include_router(choice.router)
app.include_router(api.router)
app.include_router(shopcart.router)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)


# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = secret_jwt
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, 
							exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )



templates = Jinja2Templates(directory="public")
