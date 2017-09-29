

import os

from flask import Flask, request, redirect, url_for, send_from_directory


StaticFolder = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__,static_folder=StaticFolder)
app.debug = True


@app.route('/', methods=['GET'])
def root():
  Response = redirect(url_for('staticProxy',path="swagger-ui/index.html"))
  Response.headers['Access-Control-Allow-Origin'] = "*"
  return Response

# Routes
@app.route('/<path:path>', methods=['GET'])
def staticProxy(path):

  print path

  Response = send_from_directory(StaticFolder,path)
  Response.headers['Access-Control-Allow-Origin'] = "*"
  return Response


if __name__ == '__main__':
  app.run(port=1108)
