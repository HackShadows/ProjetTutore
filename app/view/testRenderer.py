from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys
import webbrowser

with open("app_path.txt", "r") as path_file:
	app_path = path_file.readline() # chemin de l'application

source = "templates/" # le répertoire contenant les fichiers jinja
template_extension = ".tmpl"
destination = "renders/" # le répertoire destination

environment = Environment(loader=FileSystemLoader(source), autoescape=select_autoescape(), trim_blocks=True)

template = environment.get_template(sys.argv[1] + template_extension)

with open(destination + sys.argv[1] + ".html", 'w+') as file :
	file.write(template.render(app_path = app_path))

# ouvre le navigateur si 2eme argument
if len(sys.argv) > 2:
	webbrowser.open(destination + sys.argv[1] + ".html")
