from importlib import import_module
from os.path import dirname, join
from chalice import Chalice
import glob

# This injects our chalicelib folder as a path to include so we can grab our own imports
import sys
sys.path.insert(0,'chalicelib')
from models.APIKey import APIKey
from models.User import User
import helpers

# Our chalice app definition
app = Chalice(app_name='chalice-pynamodb-starter-kit')

# Automatically add all routes from our various files inside the routes folder
modules = glob.glob(join(dirname(__file__), "chalicelib", "routes", "*.py"))
for item in modules:
    filename = item.split('/')[-1].split('.')[0]
    print(f"Adding routes from {filename}")
    mod = import_module(f".{filename}", "routes")
    met = getattr(mod, "addRoutes")
    met(app)


