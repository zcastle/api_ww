from init import db

class Familia(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(255), unique=True)
	#producto = db.relationship('Producto', backref='familia', lazy='dynamic')
	#orden = db.Column(db.Integer)
	#orden2 = db.Column(db.Integer)

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
		return '<Producto_Tipo %r>' % self.descripcion

class Contacto(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	descripcion = db.Column(db.String(255), unique=True)

	def __repr__(self):
		return '<Contacto %r>' % self.descripcion

	def alias(self):
		return self.descripcion
		
class Guia(db.Model):
	igui_id = db.Column(db.Integer, primary_key=True)
	dgui_fee = db.Column(db.DateTime)
	cgui_ser = db.Column(db.String(3))
	cgui_num = db.Column(db.String(11))

	icli_id = db.Column(db.Integer, db.ForeignKey("contacto.id"))
	contacto = db.relationship("Contacto", backref=db.backref('producto', lazy='dynamic'))

	def __repr__(self):
		return '<Guia %r-%r>' % (self.cgui_ser, self.cgui_num)

	def numero(self):
		return '%s-%s' % (self.cgui_ser, self.cgui_num)

	def fecha(self):
		return self.dgui_fee.strftime('%d-%m-%Y')

class Compra(db.Model):
	icom_id = db.Column(db.Integer, primary_key=True)
	dcom_fee = db.Column(db.DateTime)
	ccom_num = db.Column(db.String(50))
	guia_compra = db.Column(db.String(50))

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
	capacidad = db.Column(db.String(255))

	def __repr__(self):
		return "<Producto %r>" % self.serie