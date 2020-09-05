import werkzeug
# flask-restplus has bug. target miss matched.
werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask

from model import db
from endpoint import api
from config import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{}:{}@{}:{}/{}'.format(ID, PW, HOST, PORT, DB)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
api.init_app(app)

if __name__ == '__main__':
    app.run(threaded=True)