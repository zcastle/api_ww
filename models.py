from init import db, app
from util import md5
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class Cia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ruc = db.Column(db.String(11), unique=True)
	razon = db.Column(db.String(255), unique=True)
	comercial = db.Column(db.String(255), unique=True)

	def __repr__(self):
		return '<Cia %r>' % self.comercial

class Familia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(255), unique=True)
	#producto = db.relationship('Producto', backref='familia', lazy='dynamic')
	orden = db.Column(db.Integer)
	orden2 = db.Column(db.Integer)

	def __repr__(self):
		return '<Familia %r>' % self.descripcion

class Marca(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(255), unique=True)

	def __repr__(self):
		return '<Marca %r>' % self.descripcion

class Modelo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(255), unique=True)

	def __repr__(self):
		return '<Modelo %r>' % self.descripcion

class TipoProducto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(255), unique=True)

	def __repr__(self):
		return '<TipoProducto %r>' % self.descripcion

class Departamento(db.Model):
	cdep_id = db.Column(db.String(2), primary_key=True, unique=True)
	vdep_nom = db.Column(db.String(255))

class Provincia(db.Model):
	cdep_id = db.Column(db.String(2))
	cpvi_id = db.Column(db.String(2), primary_key=True, unique=True)
	vpvi_nom = db.Column(db.String(255))

class Distrito(db.Model):
	cdep_id = db.Column(db.String(2))
	cpvi_id = db.Column(db.String(2))
	cdis_id = db.Column(db.String(2), primary_key=True, unique=True)
	vdis_nom = db.Column(db.String(255))

class Contacto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ruc = db.Column(db.String(11), unique=True)
	descripcion = db.Column(db.String(255), unique=True)
	coordinador = db.Column(db.String(255), unique=True)
	direccion = db.Column(db.String(255))
	cdep_id = db.Column(db.String(2))
	cpvi_id = db.Column(db.String(2))
	cdis_id = db.Column(db.String(2))

	def __repr__(self):
		return '<Contacto %r>' % self.descripcion

	def getAlias(self):
		return self.descripcion

	def getRazon(self):
		return self.coordinador

	def getDepartamento(self):
		return Departamento.query.filter_by(cdep_id=self.cdep_id).first().vdep_nom

	def getProvincia(self):
		return Provincia.query.filter_by(cdep_id=self.cdep_id, cpvi_id=self.cpvi_id).first().vpvi_nom

	def getDistrito(self):
		return Distrito.query.filter_by(cdep_id=self.cdep_id, cpvi_id=self.cpvi_id, cdis_id=self.cdis_id).first().vdis_nom

	def getPersonas(self):
		return ContactoPersona.query.filter_by(contacto_id=self.id).all()

class ContactoPersona(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(255))
	telefono = db.Column(db.String(255))
	correo = db.Column(db.String(255))

	contacto_id = db.Column(db.Integer) #, db.ForeignKey("contacto.id")
	#contacto = db.relationship("Contacto", backref=db.backref("contacto_persona", lazy="joined"))

	def __repr__(self):
		return '<Contacto %r>' % self.descripcion

class GuiaTipo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(255), unique=True)

	def __repr__(self):
		return '<GuiaTipo %r>' % self.descripcion

class Guia(db.Model):
	igui_id = db.Column(db.Integer, primary_key=True)
	dgui_fee = db.Column(db.DateTime)
	cgui_ser = db.Column(db.String(3))
	cgui_num = db.Column(db.String(11))
	icli_id = db.Column(db.Integer, db.ForeignKey("contacto.id"))
	contacto = db.relationship("Contacto", backref=db.backref('guia', lazy='dynamic'))

	tipo_id = db.Column(db.Integer, db.ForeignKey("guia_tipo.id"))
	tipo = db.relationship("GuiaTipo", backref=db.backref("guia", lazy="dynamic"))

	cia_id = db.Column(db.Integer, db.ForeignKey("cia.id"))

	cerrado = db.Column(db.Integer)
	vgui_est = db.Column(db.String(11))

	def __repr__(self):
		return '<Guia %r-%r>' % (self.cgui_ser, self.cgui_num)

	def getNumero(self):
		if self.cerrado==0:
			return "EN PROCESO"
		else:
			return '%s-%s' % (self.cgui_ser, self.cgui_num)

	def getFecha(self):
		return self.dgui_fee.strftime('%d-%m-%Y')

	def isAnulado(self):
		return "N" if self.vgui_est=="GENERADO" else "S"

class GuiaSalidaDetalle(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	guia_id = db.Column(db.Integer, db.ForeignKey("guia.igui_id"))
	guia = db.relationship("Guia", backref=db.backref('guia_salida_detalle', lazy='dynamic'))
	producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))
	producto = db.relationship("Producto", backref=db.backref('guia_salida_detalle', lazy='dynamic'))
	cantidad = db.Column(db.Integer)

	def __repr__(self):
		return '<GuiaSalidaDetalle %r>' % (self.id)

class Compra(db.Model):
	icom_id = db.Column(db.Integer, primary_key=True)
	dcom_fee = db.Column(db.DateTime)
	ccom_num = db.Column(db.String(50))
	guia_compra = db.Column(db.String(50))

	ipve_id = db.Column(db.Integer, db.ForeignKey("contacto.id"))
	contacto = db.relationship("Contacto", backref=db.backref('compra', lazy='dynamic'))

	#detalle_compra = db.relationship("DetalleCompra", backref=db.backref("compra", lazy="joined"), lazy="dynamic")

	def __repr__(self):
		return '<Compra %r>' % self.ccom_num

	def fecha(self):
		return self.dcom_fee.strftime('%d-%m-%Y')

class DetalleCompra(db.Model):
	idco_id = db.Column(db.Integer, primary_key=True)
	icom_id = db.Column(db.Integer, db.ForeignKey("compra.icom_id"))
	compra = db.relationship("Compra", backref=db.backref("detalle_compra", lazy="joined"))

	iins_id = db.Column(db.Integer, db.ForeignKey("producto.id"))
	producto = db.relationship("Producto", backref=db.backref("detalle_compra", lazy="joined"))

	def __repr__(self):
		return '<DetalleCompra %r>' % self.idco_id

class Producto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	serie = db.Column(db.String(255), unique=True)
	familia_id = db.Column(db.Integer, db.ForeignKey("familia.id"))
	familia = db.relationship("Familia", backref=db.backref("producto", lazy="dynamic"))
	marca_id = db.Column(db.Integer, db.ForeignKey("marca.id"))
	marca = db.relationship("Marca", backref=db.backref("producto", lazy="dynamic"))
	modelo_id = db.Column(db.Integer, db.ForeignKey("modelo.id"))
	modelo = db.relationship("Modelo", backref=db.backref("producto", lazy="dynamic"))
	tipo_id = db.Column(db.Integer, db.ForeignKey("tipo_producto.id"))
	tipo = db.relationship("TipoProducto", backref=db.backref("producto", lazy="dynamic"))
	guia_id = db.Column(db.Integer, db.ForeignKey("guia.igui_id"))
	guia = db.relationship("Guia", backref=db.backref("producto", lazy="dynamic"))
	producto_id = db.Column(db.Integer)
	#producto_id = db.Column(db.Integer, db.ForeignKey("producto.id"))
	#producto = db.relationship("Producto", backref=db.backref("producto", lazy="dynamic"))
	capacidad = db.Column(db.String(255))

	def __repr__(self):
		return "<Producto %r>" % self.serie

class Usuario(db.Model):
	iusu_id = db.Column(db.Integer, primary_key=True)
	vusu_nom = db.Column(db.String(100))
	vusu_ape = db.Column(db.String(100))
	vusu_usu = db.Column(db.String(100), unique=True)
	vusu_cla = db.Column(db.String(32))

	def generate_auth_token(self, expiration = 6000):
		s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return s.dumps({'id': self.iusu_id})

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # token valido pero expiro
		except BadSignature:
			return None # token invalido
		user = Usuario.query.get(data['id'])
		return user

	def __repr__(self):
		return "<Usuario %r>" % self.vusu_usu

	def login(self, clave):
		return self.vusu_cla == clave