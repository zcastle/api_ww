from init import auth, MyResource, db
from flask import jsonify
from models import Guia, GuiaTipo, GuiaSalidaDetalle, Producto, Familia
from sqlalchemy import desc, func, text

class GuiasAll(MyResource):

	@auth.login_required
	def get(self, ciaId, contactoId=0, numero="all", pagina=0):
		if numero=="all":
			numero = ""

		rows = Guia.query.filter(Guia.cia_id==ciaId)

		if contactoId>0:
			rows = rows.filter(Guia.icli_id == contactoId)

		rows = rows.filter(Guia.cgui_num.like("%"+numero+"%")).order_by(desc(Guia.dgui_fee)).order_by(desc(Guia.cgui_num)).limit(20).offset(pagina*20).all()

		if len(rows)==0:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado informacion."

		for row in rows:
			contacto = ""
			if not row.contacto is None:
				contacto = row.contacto.getAlias()

			self.response["data"].append({
				"id": row.igui_id,
				"fecha": row.getFecha(),
				"numero": row.getNumero(),
				"contacto": contacto,
				"tipo": row.tipo.descripcion,
				"anulado": row.isAnulado()
			})

		return jsonify(self.response)

class GuiasTipo(MyResource):

	@auth.login_required
	def get(self):
		rows = GuiaTipo.query.all()

		if len(rows)==0:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado informacion."

		for row in rows:
			self.response["data"].append({
				"id": row.id,
				"descripcion": row.descrpicion
			})

		return jsonify(self.response)

class GuiasDetalle(MyResource):

	@auth.login_required
	def get(self, id=0):
		row = Guia.query.get(id)

		#if contactoId>0:
		#	rows = rows.filter(Guia.icli_id == contactoId)

		#rows = rows.filter(Guia.cgui_num.like("%"+numero+"%")).order_by(desc(Guia.dgui_fee)).order_by(desc(Guia.cgui_num)).limit(20).offset(pagina*20).all()

		if row is None:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado informacion."

		rows = row.guia_salida_detalle.join(Producto, GuiaSalidaDetalle.producto).join(Familia, Producto.familia).order_by(Familia.orden).order_by(Producto.serie)

		for row in rows:
			#print(.producto_id)
			self.response["data"].append({
				"producto_id": row.producto_id,
				"serie": row.producto.serie,
				"familia": row.producto.familia.descripcion,
				"tipo": row.producto.tipo.descripcion
			})

		return jsonify(self.response)

class GuiasDetalleResumen(MyResource):

	@auth.login_required
	def get(self, id=0):
		row = Guia.query.get(id)

		if row is None:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado informacion."

		#rows = row.guia_salida_detalle #.join(Producto) #.join(Familia, Producto.familia).order_by(Familia.orden).order_by(Producto.serie)
		#rows = db.session.query(func.count(Familia.descripcion), Familia.descripcion).join(Producto).join(row.guia_salida_detalle).group_by(Familia.descripcion).all()
		#rows = db.session.query(func.count(Familia.descripcion), Familia.descripcion).join(Producto).join(GuiaSalidaDetalle).filter(row.guia_salida_detalle).group_by(Familia.descripcion).all()

		#productos = []
		#for row in rows:
			#print(row.producto_id)
			#productos.append(row.producto_id)
			#self.response["data"].append({
			#	"producto_id": row.producto_id,
			#	"serie": row.producto.serie,
			#	"familia": row.producto.familia.descripcion,
			#	"tipo": row.producto.tipo.descripcion
			#})
		#resumen = db.session.query(func.sum(GuiaSalidaDetalle.cantidad), Familia.descripcion).join(Producto).filter(Producto.id.in_(productos)).filter_by(GuiaSalidaDetalle.guia_id=1).group_by(Familia.descripcion).all()
		#resumen = db.session.query(func.sum(GuiaSalidaDetalle.cantidad), Familia.descripcion).join(Producto).join(GuiaSalidaDetalle).filter(Producto.id.in_(productos)).group_by(Familia.descripcion).all()
		#q = db.QueryDebugger(resumen)
		#print(q.query)
		#GuiaSalidaDetalle.query.with_entities(func.sum(GuiaSalidaDetalle.cantidad)).filter(GuiaSalidaDetalle.guia_id=id)
		#rows = db.session.query(Familia.descripcion, func.sum(GuiaSalidaDetalle.cantidad)).filter_by(GuiaSalidaDetalle.guia_id=id).group_by(Familia.descripcion).all()
		#rows = rows.with_entities(Producto).filter(GuiaSalidaDetalle.guia_id=id)
		#resumen = []
		sql = 'SELECT F.descripcion AS familia, SUM(GSD.cantidad) AS cantidad FROM guia_salida_detalle GSD INNER JOIN producto P ON P.id=GSD.producto_id INNER JOIN familia F ON F.id =P.familia_id WHERE GSD.guia_id = '+str(id)+' GROUP BY F.descripcion ORDER BY F.orden'
		#connection = db.engine.connect()
		#print(connection)
		#rows = connection.execute(sql)
		rows = db.engine.execute(sql)
		for row in rows:
			#print(row)
			#print(row.familia)
			#print(row.cantidad)
			#print(row.producto.familia.descripcion)

			self.response["data"].append({
				"cantidad": int(row.cantidad),
				"familia": row.familia
			})

		return jsonify(self.response)