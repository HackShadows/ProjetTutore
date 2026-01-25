import os

from fastapi import FastAPI, Request, Form, status, Cookie, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import unicodedata

from controllers.connexionController import registerUser, logIn
from controllers.puzzleController import registerImage, getAllPuzzleFromUser, deleteImage, getImageDept, getImageById, \
	getHashSolution, getMonumentNameById, clean_string
from models.connexionModel import verify_token, update_user_profile_pic
from models.mapModel import DepartementData
from models.puzzleModel import get_department_info

app = FastAPI()
app.mount("/static/css", StaticFiles(directory="view/css/"), name="static_css")
app.mount("/static/img", StaticFiles(directory="view/img/"), name="static_img")
app.mount("/static/js", StaticFiles(directory="view/js/"), name="static_js")

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
def get_root(request: Request, user_context: str = Depends(get_current_user)):
	return templates.TemplateResponse(name="index.tmpl", request=request, context=user_context)


@app.get("/map", response_class=HTMLResponse)
def get_root(request: Request, user_context: str = Depends(get_current_user)):
	return templates.TemplateResponse(name="map.tmpl", request=request, context=user_context)


@app.get("/personal-puzzles", response_class=HTMLResponse)
def get_root(request: Request, user_context: str = Depends(get_current_user)):
	if user_context['user_name'] is not None:
		listImages = getAllPuzzleFromUser(user_context['user_name'])
		return templates.TemplateResponse(name="personal-puzzles/index.tmpl", request=request,
										  context={"listImages": listImages} | user_context)
	else:
		return RedirectResponse(url="/connexion", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/connexion", response_class=HTMLResponse)
def get_root(request: Request, user_context: str = Depends(get_current_user)):
	return templates.TemplateResponse(name="connexion.tmpl", request=request, context={'data': False} | user_context)


@app.get("/inscription", response_class=HTMLResponse)
def get_root(request: Request, user_context: str = Depends(get_current_user)):
	return templates.TemplateResponse(name="inscription.tmpl", request=request, context={"data": False} | user_context)


@app.post("/traitementInscription", response_class=HTMLResponse)
def post_inscription(request: Request, username: str = Form(...), password: str = Form(...),
					 confirm_password: str = Form(...), user_context: str = Depends(get_current_user)):
	success, message = registerUser(username, password, confirm_password)
	if success:
		return RedirectResponse(url="/connexion", status_code=status.HTTP_303_SEE_OTHER)
	else:
		return templates.TemplateResponse(name="inscription.tmpl", request=request,
										  context={'data': {'username': username}, 'error': message} | user_context)


@app.post("/traitementConnexion", response_class=HTMLResponse)
def post_connexion(request: Request, username: str = Form(...), password: str = Form(...),
				   user_context: str = Depends(get_current_user)):
	success, result = logIn(username, password)  # result est soit le message d'erreur soit le token
	if success:
		token = result
		response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
		# key="access_token" : le nom du cookie
		# value=token : le JWT
		# httponly=True : empêche le JavaScript de lire le cookie (sécurité XSS)
		response.set_cookie(key="access_token", value=token, httponly=True)
		return response
	else:
		return templates.TemplateResponse(name="connexion.tmpl", request=request,
										  context={'data': {'username': username}, 'error': result} | user_context)


@app.get("/deconnexion")
def logout():
	response = RedirectResponse(url="/", status_code=303)
	response.delete_cookie("access_token")
	return response


@app.get("/personal-puzzles/create-puzzle", response_class=HTMLResponse)
def get_root(request: Request, user_context: str = Depends(get_current_user)):
	if user_context['user_name'] is not None:
		return templates.TemplateResponse(name="personal-puzzles/create-puzzle.tmpl", request=request,
										  context=user_context)
	else:
		return RedirectResponse(url="/connexion", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/play", response_class=HTMLResponse)
def get_root(request: Request, user_context: str = Depends(get_current_user)):
	return templates.TemplateResponse(name="play/index.tmpl", request=request, context=user_context)


@app.get("/play/official-puzzle", response_class=HTMLResponse)
def get_official_puzzle(request: Request, image_id: int = None, size: int = 4,
						user_context: dict = Depends(get_current_user)):
	if image_id is None:
		print("Accès direct au puzzle sans image : redirection vers la carte.")
		return RedirectResponse(url="/map", status_code=status.HTTP_303_SEE_OTHER)

	image = getImageById(image_id)

	tiles = []
	for i in range(size * size):
		tiles.append({
			"id": i,
			"x": i % size,
			"y": i // size,
			"rotation": 0
		})
	hashSolution = getHashSolution(tiles, size)
	context = {
		"image": image,
		"board_width": size,
		"board_height": size,
		"puzzle_tiles": tiles,
		"solution_hash": hashSolution
	}

	return templates.TemplateResponse(
		name="play/official-puzzle.tmpl",
		request=request,
		context=context | user_context
	)


@app.get("/play/personal-puzzle", response_class=HTMLResponse)
def get_personal_puzzle(request: Request, image_id: int = None, size: int = 4,
						user_context: dict = Depends(get_current_user)):
	if image_id is None:
		return RedirectResponse(url="/personal-puzzles", status_code=status.HTTP_303_SEE_OTHER)

	image = getImageById(image_id)

	tiles = []
	for i in range(size * size):
		tiles.append({
			"id": i,
			"x": i % size,
			"y": i // size,
			"rotation": 0
		})

	hashSolution = getHashSolution(tiles, size)
	context = {
		"image": image,
		"board_width": size,
		"board_height": size,
		"puzzle_tiles": tiles,
		"solution_hash": hashSolution
	}
	return templates.TemplateResponse(name="play/personal-puzzle.tmpl", request=request, context=context | user_context)


@app.post("/traitementCreationPuzzle", response_class=HTMLResponse)
def post_creation_puzzle(request: Request, nom_image: str = Form(...), url: str = Form(None),
						 file_image: UploadFile = File(None),
						 user_context: str = Depends(get_current_user)):
	if file_image.filename != '':
		upload_dir = "view/img/user_images"
		os.makedirs(upload_dir, exist_ok=True)
		file_path = f"{upload_dir}/{file_image.filename}"
		with open(file_path, "wb") as buffer:
			shutil.copyfileobj(file_image.file, buffer)
		generated_url = f"/static/img/user_images/{file_image.filename}"
		success, message = registerImage(nom_image, generated_url, user_context['user_name'])
	elif url:
		success, message = registerImage(nom_image, url, user_context['user_name'])
	else:
		return templates.TemplateResponse(name="personal-puzzles/create-puzzle.tmpl", request=request, context={
																												   'erreur': "Les champs url et file ne sont pas remplis"} | user_context)
	if success:
		return templates.TemplateResponse(name="personal-puzzles/create-puzzle.tmpl", request=request,
										  context={'message': "L'image a bien été crée"} | user_context)
	else:
		return templates.TemplateResponse(name="personal-puzzles/create-puzzle.tmpl", request=request,
										  context={'erreur': message} | user_context)


@app.post("/upload-profile-pic")
async def upload_profile_pic(request: Request, file_image: UploadFile = File(...),
							 user_context: dict = Depends(get_current_user)):
	username = user_context.get("user_name")
	if not username:
		return RedirectResponse(url="/connexion", status_code=status.HTTP_303_SEE_OTHER)

	file_location = f"view/img/{file_image.filename}"
	with open(file_location, "wb") as buffer:
		shutil.copyfileobj(file_image.file, buffer)

	url_image = f"/static/img/{file_image.filename}"

	success, result = registerImage(nom_image=f"Profil_{username}", url=url_image, username=username)

	if success:
		img_data = getImageById(result)
		update_user_profile_pic(username, result)

	return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/selectionDepartement")
def post_selection_departement(request: Request, data: DepartementData, user_context: str = Depends(get_current_user)):
	return {"redirect_url": f"/difficulte?number={data.number}"}


@app.get("/difficulte", response_class=HTMLResponse)
def get_difficulte(request: Request, number: str = None, user_context: dict = Depends(get_current_user)):
	if number is None:
		return RedirectResponse(url="/map", status_code=status.HTTP_303_SEE_OTHER)

	image = getImageDept(number)
	nom_dept = get_department_info(number)

	context = {
		"image": image,
		"departement_num": number,
		"departement_nom": nom_dept,
		"mode": "official"
	}
	return templates.TemplateResponse(name="difficulte.tmpl", request=request, context=context | user_context)


@app.post("/supprimerImage", response_class=HTMLResponse)
def post_supprimerImage(request: Request, id: str = Form(...), user_context: str = Depends(get_current_user)):
	deleteImage(id)
	return RedirectResponse(url="/personal-puzzles", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/choisirImage", response_class=HTMLResponse)
def post_choisirImage(request: Request, image_id: int = Form(...), user_context: str = Depends(get_current_user)):
	image = getImageById(image_id)
	return templates.TemplateResponse(name="difficulte.tmpl", request=request, context={
																						   "image": image,
																						   "departement_num": None,
																						   "departement_nom": None,
																						   "mode": "personal"
																					   } | user_context)


@app.get("/victoire", response_class=HTMLResponse)
def get_root(request: Request, image_id: str, user_context: str = Depends(get_current_user)):
	image = getImageById(image_id)
	return templates.TemplateResponse(name="play/victoire.tmpl", request=request,
									  context={'image': image} | user_context)


@app.post("/devinerMonument", response_class=HTMLResponse)
def post_devinerMonument(request: Request, monument: str = Form(...), id_image: str = Form(...),
						 user_context: str = Depends(get_current_user)):
	image = getImageById(id_image)
	name = image['nom_monument']
	name_no_accent = clean_string(name)
	monument_no_accent = clean_string(monument)
	if name_no_accent == monument_no_accent:
		return templates.TemplateResponse(name="play/victoire.tmpl", request=request, context={
																								  "image": image,
																								  "trouve": True,
																								  "monument": monument
																							  } | user_context)
	else:
		return templates.TemplateResponse(name="play/victoire.tmpl", request=request, context={
																								  "image": image,
																								  "essai": True,
																							  } | user_context)


@app.post("/revelerMonument", response_class=HTMLResponse)
def post_revelerMonument(request: Request, id_image: str = Form(...), user_context: str = Depends(get_current_user)):
	image = getImageById(id_image)
	name = image['nom_monument']
	return templates.TemplateResponse(name="play/victoire.tmpl", request=request, context={
																							  "image": image,
																							  "revele": True,
																							  "monument": name
																						  } | user_context)

