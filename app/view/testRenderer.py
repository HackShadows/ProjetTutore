from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys
import webbrowser

source = "templates/"
destination = "renders/"

environment = Environment(loader=FileSystemLoader(source), autoescape=select_autoescape(), trim_blocks=True)

template = environment.get_template(sys.argv[1])

with open(destination + sys.argv[2], 'w') as file :
    file.write(template.render())

if len(sys.argv) > 3 and sys.argv[3]:
    webbrowser.open("file:///home/cauch/Documents/School/ProjetPuzzle/projet-tutore/app/view/" + destination + sys.argv[2])
