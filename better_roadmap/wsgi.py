from flask import Flask

from .app import create_app

server: Flask = create_app().server
