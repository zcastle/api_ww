from init import app, api, MyResource
from flask import jsonify, make_response
from models import Producto
#, Familia

response = {
	"success": True,
	"error": False,
	"message": "",
	"data": []
}

@app.errorhandler(404)
def not_found(error):
	response["error"] = True
	response["message"] = "No encontrado"
	return make_response(jsonify(response), 404)

@app.route("/")
def index():
	return "HW"

class Productos(MyResource):

	def get(self, serie, exacta="false"):
		if exacta=="true":
			res = Producto.query.filter_by(serie=serie).limit(10).all() #.first()
		else:
			res = Producto.query.filter(Producto.serie.like("%"+serie+"%")).limit(10).all()

		if len(res)==0:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado producto con el numero de serie."

		for row in res:
			print row.detalle_compra.compra
			data = {
				"serie": row.serie,
				"familia": row.familia.descripcion,
				"marca": row.marca.descripcion,
				"modelo": row.modelo.descripcion,
				"tipo": row.tipo.descripcion
			}
			data["guia"] = {}
			if not row.guia is None:
				data["guia"] = {
					"numero": row.guia.numero(),
					"fecha": row.guia.fecha(),
					"cliente": row.guia.contacto.alias()
				}
			data['componentes'] = []
			#join(Familia, Producto.familia).order_by(Familia.orden2).
			componentes = Producto.query.filter_by(producto_id=row.id).all()
			for comp in componentes:
				data["componentes"].append({
					"serie": comp.serie,
					"familia": comp.familia.descripcion,
					"capacidad": comp.capacidad,
					#"orden": comp.familia.orden2
				})

			self.response["data"].append(data)
		
		return jsonify(self.response)

api.add_resource(Productos, '/api/producto/<string:serie>/<string:exacta>')

if __name__ == "__main__":
	app.run(debug=True)