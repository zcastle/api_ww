from init import auth, MyResource, db
from flask import jsonify
from models import Contacto
from util import getJsonFromUrl

class ContactosAll(MyResource):

	@auth.login_required
	def get(self, nombre="all"):
		if nombre=="all":
			contactos = Contacto.query.limit(20).all()
		else:
			contactos = Contacto.query.filter((Contacto.descripcion.like("%"+nombre+"%"))|(Contacto.coordinador.like("%"+nombre+"%"))).limit(20).all()

		if len(contactos)==0:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado informacion."

		for c in contactos:
			self.response["data"].append({
				"id": c.id,
				"alias": c.getAlias(),
				"razon": c.getRazon()
			})

		return jsonify(self.response)

class Contactos(MyResource):

	@auth.login_required
	def get(self, id=0):
		row = Contacto.query.get(id)

		if row is None:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado informacion."

		data = []
		data = {
			"alias": row.getAlias(),
			"ruc": row.ruc,
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

class ContactosFacturasPendientes(MyResource):

	@auth.login_required
	def get(self, id=0):

		sql = 'SELECT V.iven_id, V.dven_fee, CONCAT(V.cven_ser, \'-\', V.cven_num) AS numero, IFNULL(V.orden, \'\') AS orden, ROUND(V.nven_tot, 2) AS nven_tot, M.vmon_sim FROM venta V INNER JOIN moneda M ON M.imon_id = V.imon_id WHERE V.icli_id = '+str(id)+' AND V.vven_est = \'GENERADO\' AND V.temporal = \'N\' AND V.iven_id NOT IN (SELECT CD.venta_id FROM cobranza_d CD INNER JOIN cobranza C ON C.id=CD.cobranza_id) ORDER BY V.dven_fee, V.cven_num'
		rows = db.engine.execute(sql)
		for row in rows:
			self.response["data"].append({
				"id": row.iven_id,
				"fecha": row.dven_fee.strftime('%d-%m-%Y'),
				"numero": row.numero,
				"orden": row.orden,
				"monto": row.nven_tot,
				"moneda": row.vmon_sim
			})

		return jsonify(self.response)