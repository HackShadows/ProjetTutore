from fastapi import FastAPI, Request, Form, status, Cookie, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from controllers.connexionController import registerUser, logIn
from models.connexionModel import verify_token

app = FastAPI()
app.mount("/static/css", StaticFiles(directory="view/css/"), name="static_css")
app.mount("/static/img", StaticFiles(directory="view/img/"), name="static_img")
app.mount("/static/js" , StaticFiles(directory="view/js/" ), name="static_js" )

templates = Jinja2Templates(directory="view/templates/", autoescape=True, auto_reload=True)


async def get_current_user(access_token: str = Cookie(default=None)):
	"""
	Récupère le cookie 'access_token' automatiquement.
	Si le cookie est absent ou invalide, retourne None.
	"""
	if not access_token:
		return None
	username = verify_token(access_token)
	return username

@app.get("/", response_class=HTMLResponse, )
def get_root(request :Request, username: str = Depends(get_current_user)) :
	user_is_connected = username is not None
	print(f"Username : {username}, connected : {user_is_connected}")
	return templates.TemplateResponse(name="index.tmpl", request=request, context={'user': username, 'connected': user_is_connected})


@app.get("/map", response_class=HTMLResponse)
def get_root(request :Request) :
	return templates.TemplateResponse(name="map.tmpl", request=request)


@app.get("/personal-puzzles", response_class=HTMLResponse)
def get_root(request :Request) :
	return templates.TemplateResponse(name="personal-puzzles.tmpl", request=request)

@app.get("/connexion", response_class=HTMLResponse)
def get_root(request :Request) :
	print(request)
	return templates.TemplateResponse(name="connexion.tmpl", request=request, context={'data': False})

@app.get("/inscription", response_class=HTMLResponse)
def get_root(request :Request) :
	return templates.TemplateResponse(name="inscription.tmpl", request=request, context={"data": False})

@app.post("/traitementInscription", response_class=HTMLResponse)
def post_inscription(request: Request, username: str = Form(...), password: str=Form(...), confirm_password: str=Form(...)):
	success, message = registerUser(username, password, confirm_password)
	print(f"succes : {success}, message : {message}")
	if success:
		return RedirectResponse(url="/connexion", status_code=status.HTTP_303_SEE_OTHER)
	else:
		return templates.TemplateResponse(name="inscription.tmpl", request=request, context={'data': {'username': username},
																							 'error': message})

@app.post("/traitementConnexion", response_class=HTMLResponse)
def post_connexion(request: Request, username: str = Form(...), password: str=Form(...)):
	print("entree dans post_connexion")
	success, result = logIn(username, password) # result est soit le message d'erreur soit le token
	print(f"succes : {success}, result : {result}")
	if success:
		token = result
		response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
		# key="access_token" : le nom du cookie
		# value=token : le JWT
		# httponly=True : empêche le JavaScript de lire le cookie (sécurité XSS)
		response.set_cookie(key="access_token", value=token, httponly=True)
		return response
	else:
		return templates.TemplateResponse(name="connexion.tmpl", request=request, context={'data': {'username': username},
																							 'error': result})

@app.get("/deconnexion")
def logout():
	response = RedirectResponse(url="/", status_code=303)
	response.delete_cookie("access_token")
	return response

