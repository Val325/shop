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

app = FastAPI()

secret_jwt = "4d398bd652db815963be16eb60638b9cc3c70096"

engine = create_engine("postgresql://postgres:Hamachi2002@localhost/fastapiDB")
class Base(DeclarativeBase): pass

class products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    header = Column(String)
    description = Column(String)
    name_image = Column(String)
    path_image = Column(String)
    price = Column(Integer)

class users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    password = Column(String)
    admin = Column(Boolean, unique=False, default=False)
    money = Column(Integer)

Base.metadata.create_all(bind=engine)
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

templates = Jinja2Templates(directory="public")

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


@app.get('/', response_class=HTMLResponse)
async def main(response: Response,
				request: Request, 
				access_token_cookie: str | None = Cookie(default=None), 
				Authorize: AuthJWT = Depends()):
	

	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	return templates.TemplateResponse("index.html", {"request": request, 
														"texts": texts, 
														"IsAuth": isAuth['user'],
														"auth": auth})

@app.post('/', response_class=HTMLResponse)
def get_data(request: Request, 
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

	return templates.TemplateResponse("index.html", {"request": request, 
													"filename": file.filename, 
													"IsAuth": isAuth['user'],
													"auth": auth})

@app.get('/login', response_class=HTMLResponse)
async def login_get(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})

@app.get('/admin', response_class=HTMLResponse)
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

		#If user auth?
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	return templates.TemplateResponse("adminPanel.html", {"request": request, 
															"IsAuth": isAuth['user'],
															"auth": auth})

@app.post('/login')
async def login_post(request: Request, 
					response: Response, 
					Password = Form(), 
					Username = Form(), 
					Authorize: AuthJWT = Depends()):
	print("login")
	print("Username:", Username)
	print("Password:", Password)

	expires = timedelta(days=7)
	response = None

	with Session(autoflush=False, bind=engine) as db:
		try:
			userDB = db.query(users).filter(users.user==Username).one_or_none()
			print(f"{userDB.id}.{userDB.user} ({userDB.password})")

			data_jwt_save = json.dumps({"user":userDB.user, "admin_right":userDB.admin})
			
			IsAuthBool = bcrypt.checkpw(Password.encode('utf-8'), userDB.password.encode('utf8'))
			print("Is password correct?", IsAuthBool)

			if IsAuthBool:
				# Create the tokens and passing to set_access_cookies or set_refresh_cookies
				access_token = Authorize.create_access_token(subject=data_jwt_save,expires_time=expires)
				refresh_token = Authorize.create_refresh_token(subject=data_jwt_save,expires_time=expires)
				# Set the JWT cookies in the response
		
		
				response = RedirectResponse(url="/")
				Authorize.set_access_cookies(access_token, response) 
				Authorize.set_refresh_cookies(refresh_token, response)
				
				return response
				
			
			
		except AttributeError:
		    print("User not finded")

	

	return templates.TemplateResponse("login.html", {"request": request})

@app.get('/registration', response_class=HTMLResponse)
async def main(request: Request):
	return templates.TemplateResponse("registration.html", {"request": request})

@app.post('/registration', response_class=HTMLResponse)
async def login_post(request: Request, 
						Password = Form(), 
						Username = Form()):
	print("Password")
	print("Username:", Username)
	print("Password:", Password)

	salt = bcrypt.gensalt()
	hashed = bcrypt.hashpw(Password.encode('utf-8'), salt).decode('utf8')

	print("salt", salt)
	print("Hashed:", hashed)
	with Session(autoflush=False, bind=engine) as db:
		
		data_user = users(user=Username, password=hashed,money=100)
		db.add(data_user)     
		db.commit()     
		
	return templates.TemplateResponse("registration.html", {"request": request})

@app.get('/logout')
async def logout(response: Response,
				Authorize: AuthJWT = Depends()):
	response = RedirectResponse(url="/")
	Authorize.unset_jwt_cookies(response)
	return response

#
# show product
#

@app.get("/product/{id}")
def product_id_get(request: Request,
					id: int,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):

	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
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
															"auth": auth})

@app.post("/product/{id}")
def product_id_post(request: Request,
					id: int,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):

	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
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
															"auth": auth})

#
# bying product
#

@app.get("/bying/{id}")
def bying_id_get(request: Request,
					id: int,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):
	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
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
															"auth": auth})

@app.post("/bying/{id}")
def bying_id_post(request: Request,
					id: int,
					access_token_cookie: str | None = Cookie(default=None), 
					Authorize: AuthJWT = Depends()):
	data_product = return_product_by_id(id)
	print("product", data_product)
	
	try:
		texts = send_all_goods()
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
		user = return_user(isAuth["user"])
		
		
		print("money:", user.money)
		print("product money:", data_product["price"])
		moneyAfterBying = user.money - data_product["price"]
		print("after bying money:", moneyAfterBying)
		set_money_user(user.user, moneyAfterBying)
		if isAuth:
			auth = True
	except:
		return RedirectResponse(url="/login")

	

	


	return templates.TemplateResponse("bying.html", {"request": request,
													"id":data_product["id"],
													"header":data_product["header"],
													"description":data_product["description"],
													"name_image":data_product["name_image"],
													"path_image":data_product["path_image"],
													"price":data_product["price"],
													"IsAuth": isAuth['user'],
													"auth": auth})

@app.get("/profile")
def profile(request: Request, 
			access_token_cookie: str | None = Cookie(default=None), 
			Authorize: AuthJWT = Depends()):

	try:
		auth_jwt(Authorize, access_token_cookie)
		isAuth = json.loads(Authorize.get_jwt_subject())
		print("userdata", isAuth["user"])
		user = return_user(isAuth["user"])
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
														"IsAuth": isAuth['user'],
														"auth": auth})