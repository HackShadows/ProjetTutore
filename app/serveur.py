from fastapi import FastAPI, Request, Form, status, Cookie, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from controllers.connexionController import registerUser, logIn
from controllers.puzzleController import registerImage, getAllPuzzleFromUser, deleteImage, getImageDept
from models.connexionModel import verify_token
from models.mapModel import DepartementData

app = FastAPI()
app.mount("/static/css", StaticFiles(directory="view/css/"), name="static_css")
app.mount("/static/img", StaticFiles(directory="view/img/"), name="static_img")
app.mount("/static/js" , StaticFiles(directory="view/js/" ), name="static_js" )

templates = Jinja2Templates(directory="view/templates/", autoescape=True, auto_reload=True)


board_size = 4
puzzle_tiles = [
	{"id": 0, "img": "/static/img/test_tile1.png", "rotation": 0},
	{"id": 1, "img": "/static/img/test_tile2.png", "rotation": 0}]

puzzle_context = {"board_size": board_size, "puzzle_tiles": puzzle_tiles}

async def get_current_user(access_token: str = Cookie(default=None)):
	"""
	Récupère le cookie 'access_token' automatiquement.
	Si le cookie est absent ou invalide, name sera None.
	"""
	if not access_token:
		name = None
	else:
		name = verify_token(access_token)
	connected = name is not None
	return {"user_name": name, "user_connected": connected}

@app.get("/", response_class=HTMLResponse, )
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	return templates.TemplateResponse(name="index.tmpl", request=request, context=user_context)

@app.get("/map", response_class=HTMLResponse)
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	return templates.TemplateResponse(name="map.tmpl", request=request, context=user_context)

@app.get("/personal-puzzles", response_class=HTMLResponse)
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	if user_context['user_name'] is not None:
		listImages = getAllPuzzleFromUser(user_context['user_name'])
		return templates.TemplateResponse(name="personal-puzzles/index.tmpl", request=request, context={"listImages": listImages} | user_context)
	else:
		return RedirectResponse(url="/connexion", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/connexion", response_class=HTMLResponse)
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	print(request)
	return templates.TemplateResponse(name="connexion.tmpl", request=request, context={'data': False} | user_context)

@app.get("/inscription", response_class=HTMLResponse)
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	return templates.TemplateResponse(name="inscription.tmpl", request=request, context={"data": False} | user_context)

@app.post("/traitementInscription", response_class=HTMLResponse)
def post_inscription(request: Request, username: str = Form(...), password: str=Form(...), confirm_password: str=Form(...), user_context: str = Depends(get_current_user)):
	success, message = registerUser(username, password, confirm_password)
	print(f"succes : {success}, message : {message}")
	if success:
		return RedirectResponse(url="/connexion", status_code=status.HTTP_303_SEE_OTHER)
	else:
		return templates.TemplateResponse(name="inscription.tmpl", request=request, context={'data': {'username': username}, 'error': message} | user_context)

@app.post("/traitementConnexion", response_class=HTMLResponse)
def post_connexion(request: Request, username: str = Form(...), password: str=Form(...), user_context: str = Depends(get_current_user)):
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
		return templates.TemplateResponse(name="connexion.tmpl", request=request, context={'data': {'username': username}, 'error': result} | user_context)

@app.get("/deconnexion")
def logout():
	response = RedirectResponse(url="/", status_code=303)
	response.delete_cookie("access_token")
	return response

@app.get("/personal-puzzles/create-puzzle", response_class=HTMLResponse)
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	if user_context['user_name'] is not None:
		return templates.TemplateResponse(name="personal-puzzles/create-puzzle.tmpl", request=request, context=user_context)
	else:
		return RedirectResponse(url="/connexion", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/play", response_class=HTMLResponse)
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	return templates.TemplateResponse(name="play/index.tmpl", request=request, context=user_context)

@app.get("/play/official-puzzle", response_class=HTMLResponse)
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	return templates.TemplateResponse(name="play/official-puzzle.tmpl", request=request, context=user_context | puzzle_context)

@app.get("/play/personal-puzzle", response_class=HTMLResponse)
def get_root(request :Request, user_context: str = Depends(get_current_user)) :
	return templates.TemplateResponse(name="play/personal-puzzle.tmpl", request=request, context=user_context | puzzle_context)

@app.post("/traitementCreationPuzzle", response_class=HTMLResponse)
def post_creation_puzzle(request: Request, nom_image: str = Form(...), url: str = Form(...), user_context: str = Depends(get_current_user)):
	print("entree dans traitementCreationPuzzle")
	success, message = registerImage(nom_image, url, user_context['user_name'])
	if success:
		return templates.TemplateResponse(name="personal-puzzles/create-puzzle.tmpl", request=request, context=user_context)
	else:
		return templates.TemplateResponse(name="personal-puzzles/create-puzzle.tmpl", request=request, context={'error': message} | user_context)

@app.post("/selectionDepartement")
def post_selection_departement(request: Request, data: DepartementData, user_context: str = Depends(get_current_user)):
	print("entree dans traitementCreationPuzzle")
	print(f"Numéro du departement {data.number}")
	allImages = getImageDept(data.number)
	return {"redirect_url": "/difficulte"}

@app.get("/difficulte", response_class=HTMLResponse)
def get_difficulte(request: Request, user_context: str = Depends(get_current_user)):
	return templates.TemplateResponse(name="difficulte.tmpl", request=request, context=user_context)

@app.post("/supprimerImage", response_class=HTMLResponse)
def post_supprimerImage(request: Request, id: str = Form(...), user_context: str = Depends(get_current_user)):
	print("entree dans traitementCreationPuzzle")
	print(f"id de l'image : {id}")
	deleteImage(id)
	return RedirectResponse(url="/personal-puzzles", status_code=status.HTTP_303_SEE_OTHER)
