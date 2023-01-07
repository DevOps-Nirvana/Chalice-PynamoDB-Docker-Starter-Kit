from importlib import import_module
from os.path import dirname, join
import glob

# This injects our chalicelib folder as a path to include so we can grab our own imports
import sys
sys.path.insert(0,'chalicelib')
import helpers

# This initializes our chalice app, must be done in this file first
app = helpers.get_chalice_app()

# Now, automatically add all routes from our various files inside the routes folder
modules = glob.glob(join(dirname(__file__), "chalicelib", "routes", "*.py"))
for item in modules:
    filename = item.split('/')[-1].split('.')[0]
    # print(f"Adding routes from {filename}...")
    mod = import_module(f".{filename}", "routes")

# Our validate API key logic must be present in this file for some reason otherwise chalice freaks out on AWS Lambda (only)
from routes.internal__routes import validate_api_key
