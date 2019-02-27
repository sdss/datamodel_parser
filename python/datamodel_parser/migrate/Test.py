from flask import render_template
from datamodel_parser import app, logger
from datamodel_parser.models.datamodel import Tree
trees = Tree.query.all()
template0 = "null.txt"
x=1
result0 = render_template(template0)
template1 = "example.txt"
result1 = render_template(template1, trees = trees, ...)

