from init import auth, MyResource
from flask import jsonify
from models import Producto, DetalleCompra, Familia
#from flask_sqlalchemy import exc
#exceptions = exc.sa_exc

class ProductosAll(MyResource):

	@auth.login_required
	def get(self, serie="", exacta="false"):
		try:
			if exacta=="true":
				productos = Producto.query.filter_by(serie=serie).all() #.first()
			else:
				productos = Producto.query.filter(Producto.serie.like("%"+serie+"%")).limit(20).all()

			if len(productos)==0:
				self.response["error"] = True
				self.response["message"] = "No se ha encontrado producto con el numero de serie."

			for row in productos:
				data = {
					"id": row.id,
					"serie": row.serie,
					"familia": row.familia.descripcion,
					"tipo": row.tipo.descripcion
				}

				self.response["data"].append(data)
		except:
			self.response["error"] = True
			self.response["message"] = "Error desconocido."
		
		return jsonify(self.response)

class Productos(MyResource):

	@auth.login_required
	def get(self, id=0):
		try:
			row = Producto.query.get(id)

			if row is None:
				self.response["error"] = True
				self.response["message"] = "No se ha encontrado producto con el numero de serie."

			print(row.serie)

			padreSerie = ""
			padre = Producto.query.get(row.producto_id)
			if not padre is None:
				padreSerie = padre.serie
			data = {
				"serie": row.serie,
				"familia": row.familia.descripcion,
				"marca": row.marca.descripcion,
				"modelo": "" if row.modelo is None else row.modelo.descripcion,
				"tipo": row.tipo.descripcion,
				"padre": padreSerie
			}
			data["guia"] = {}
			if not row.guia is None:
				data["guia"] = {
					"numero": row.guia.getNumero(),
					"tipo": row.guia.tipo.descripcion,
					"fecha": row.guia.getFecha(),
					"cliente": row.guia.contacto.getAlias()
				}

			data['componentes'] = []
			componentes = Producto.query.filter_by(producto_id=row.id).join(Familia, Producto.familia).order_by(Familia.orden2).all()
			for comp in componentes:
				data["componentes"].append({
					"serie": comp.serie,
					"familia": comp.familia.descripcion,
					"capacidad": comp.capacidad
				})
			data['compra'] = {}
			compra = DetalleCompra.query.filter_by(iins_id=row.id).all()
			for comp in compra:
				data["compra"] = {
					"fecha": comp.compra.fecha(),
					"numero": comp.compra.ccom_num,
					"guia": comp.compra.guia_compra,
					"proveedor": comp.compra.contacto.getAlias()
				}

			self.response["data"].append(data)
		except:
			self.response["error"] = True
			self.response["message"] = "Error desconocido."
		
		return jsonify(self.response)