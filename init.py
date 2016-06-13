from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://sistema:275718@192.168.2.10/miningbd"
db = SQLAlchemy(app)

class MyResource(Resource):

	def __init__(self):
		self.response = {
			"success": True,
			"error": False,
			"message": "",
			"data": []
		}