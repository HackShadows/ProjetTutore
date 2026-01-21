from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates



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



