############################################################################################################
############################################################################################################
##                                                                                                        ##
## Quart Vuetify Template  (c)2024 Dieter Chvatal                                                         ##
##                                                                                                        ##
############################################################################################################
############################################################################################################

import uvicorn
import asyncio
import json
import os
from pprint import pformat as pf
from pprint import pprint as pp
from quart import Quart, jsonify, render_template, request, redirect, url_for, send_file
from quart_cors import cors
import subprocess
import time


# overwrite jinja2 delimiters to avoid conflict with vue delimiters, was previosly used by me (Dieter Chvatal)
# in order to transfer information from the backend to the frontend, while the frontend does not know its host ip address.
# window.location.host and winndow.location.protocol is now used to get the host ip address. The code is left here for reference.
# https://stackoverflow.com/questions/37039835/how-to-change-jinja2-delimiters
class CustomQuart(Quart):
    jinja_options = Quart.jinja_options.copy()
    jinja_options.update(dict( block_start_string='<%', block_end_string='%>', variable_start_string='%%', 
                              variable_end_string='%%',comment_start_string='<#',comment_end_string='#>',))


# instantiate the app
# the frontend is built with vuetify.js and is located in the dist folder
# you have to set the static folder to the dist folder and the template folder to the dist folder in the backend like below
# and edit vite.config.js to output to the dist folder within the frontend. in adddition you have to
# run 'npm run build' after each modification of the frontend. Once you run this once, the included watch mode will
# take care of the rest.
app = CustomQuart(__name__, static_folder = "dist/static", template_folder = "dist", static_url_path = "/static")
app = cors(app, allow_origin="*")
app.config.from_object(__name__)


# uncomment to disable caching, which is useful for development when you are actively changing the frontend
@app.after_request
async def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for x minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# test route
@app.route("/api")
async def json():
    return {"hello": "world"}

# deliver the vuetify frontend
@app.route("/")
async def index():
    return await render_template('index.html')

if __name__ == '__main__':
    print('''
\033[H\033[J
********************************************************
* Vuetify Quart Template V0.01  (c)2024 Dieter Chvatal *
* Async Backend                                        *
********************************************************
''')
    try:
        if 'PRODUCTION' in os.environ:
            uvicorn.run('app:app', host='0.0.0.0', port=6000, log_level="info")
        else:
            asyncio.run(app.run_task(host='0.0.0.0', port=6000, debug=True))
    except Exception as e:
        print(str(e))
    print('Bye!')