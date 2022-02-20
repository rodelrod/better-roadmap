from flask import Flask

from .app import app

server: Flask = app.server
