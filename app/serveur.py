from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from controllers.connexionController import registerUser

app = FastAPI()
app.mount("/static/css", StaticFiles(directory="view/css/"), name="static_css")
app.mount("/static/img", StaticFiles(directory="view/img/"), name="static_img")
app.mount("/static/js" , StaticFiles(directory="view/js/" ), name="static_js" )

templates = Jinja2Templates(directory="view/templates/", autoescape=True, auto_reload=True)



@app.get("/", response_class=HTMLResponse)
def get_root(request :Request) :
	return templates.TemplateResponse(name="index.tmpl", request=request)


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




