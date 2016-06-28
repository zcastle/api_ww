from init import MyResource
from flask import jsonify
from models import Contacto
from util import getJsonFromUrl

class ContactosAll(MyResource):

	def get(self, nombre="all"):
		if nombre=="all":
			contactos = Contacto.query.limit(20).all()
		else:
			contactos = Contacto.query.filter((Contacto.descripcion.like("%"+nombre+"%"))|(Contacto.coordinador.like("%"+nombre+"%"))).limit(20).all()

		if len(contactos)==0:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado contactos."

		for c in contactos:
			self.response["data"].append({
				"id": c.id,
				"alias": c.getAlias(),
				"razon": c.getRazon()
			})

		return jsonify(self.response)

class Contactos(MyResource):

	def get(self, id=0):
		row = Contacto.query.get(id)

		if row is None:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado coincidencia."

		data = []
		data = {
			"alias": row.getAlias(),
			"razon": row.getRazon(),
			"direccion": row.direccion,
			"departamento": row.getDepartamento(),
			"provincia": row.getProvincia(),
			"distrito": row.getDistrito()
		}

		data["personas"] = []
		for persona in row.getPersonas():
			data["personas"].append({
				"nombre": persona.nombre,
				"telefono": persona.telefono,
				"correo": persona.correo
			})

		if row.direccion:
			direccion = data['direccion'].replace(" ", "+")+"+"+data['distrito'].replace(" ", "+")+"+"+data['provincia'].replace(" ", "+")+"+"+data['departamento'].replace(" ", "+")
			google_maps_key = "AIzaSyCKAP5TL-tLyhRqtUC1rLYg_kReI5cnz6M"
			url = "https://maps.googleapis.com/maps/api/geocode/json?address="+direccion+"+PE&key="+google_maps_key
			p = getJsonFromUrl(url)
			if not p is None:
				if p.status=='OK':
					lat = p.results[0].geometry.location.lat
					lng = p.results[0].geometry.location.lng
					data["location"] = {
						"lat": lat,
						"lng": lng
					}

		self.response["data"] = data

		return jsonify(self.response)