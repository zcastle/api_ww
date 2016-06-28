from init import MyResource
from flask import jsonify
from models import Guia, Contacto
from util import getJsonFromUrl
from sqlalchemy import desc

class GuiasAll(MyResource):

	def get(self, ciaId, contactoId=0, numero="all"):
		if numero=="all":
			numero = ""
		if contactoId==0 and numero=="":
			rows = Guia.query.filter(Guia.cia_id==ciaId).order_by(desc(Guia.igui_id)).limit(20).all()
		else:
			if contactoId>0:
				rows = Guia.query.filter(Guia.cia_id == ciaId, Guia.icli_id == contactoId, Guia.cgui_num.like("%"+numero+"%")).order_by(desc(Guia.igui_id)).limit(20).all()
			else:
				rows = Guia.query.filter(Guia.cia_id == ciaId, Guia.cgui_num.like("%"+numero+"%")).order_by(desc(Guia.igui_id)).limit(20).all()

		if len(rows)==0:
			self.response["error"] = True
			self.response["message"] = "No se ha encontrado contactos."

		for row in rows:
			self.response["data"].append({
				"id": row.igui_id,
				"fecha": row.getFecha(),
				"numero": row.getNumero(),
				"contacto": row.contacto.getAlias()
			})

		return jsonify(self.response)