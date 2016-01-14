# -*- coding: utf-8 -*-
from lab4_5_6.project import app
from bottle import static_file


@app.route('/:file#(favicon.ico)#')
def favicon(file):
    return static_file(file, root='project/static/misc')


@app.route('/:path#(images|css|js|fonts)\/.+#')
def server_static(path):
    return static_file(path, root='project/static')

@app.route('/')
def index():
    return static_file('index.html', root='project/static')