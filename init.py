from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'aquideboponerunaclavesecreta'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://sistema:275718@192.168.2.10/ww"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class MyResource(Resource):

	def __init__(self):
		self.response = {
			"success": True,
			"error": False,
			"message": "",
			"data": []
		}