from jinja2 import Environment, FileSystemLoader, select_autoescape
import sys

environment = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape(), trim_blocks=True)

template = environment.get_template(sys.argv[1])

with open(sys.argv[2], 'w') as file :
    file.write(template.render())
