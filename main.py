from init import app, api, auth
from flask import g, jsonify, make_response
from controllers.productos import ProductosAll, Productos
from controllers.contactos import ContactosAll, Contactos, ContactosFacturasPendientes
from controllers.guias import GuiasAll, GuiasDetalle, GuiasDetalleResumen, GuiasTipo
from models import Usuario

@app.errorhandler(404)
def not_found(error):
	response = {
		"error": True,
		"message": "No encontrado"
	}
	return make_response(jsonify(response), 404)

@app.route("/")
def index():
	return "HW"

@auth.verify_password
def verify_password(usuario_or_token, clave):
	#print(usuario_or_token)
	#print(clave)
	user = Usuario.verify_auth_token(usuario_or_token)
	if not user:
		user = Usuario.query.filter_by(vusu_usu=usuario_or_token).first()
		if not user or not user.login(clave):
			return False
	g.user = user
	return True

@app.route('/api/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii')})

@app.route('/api/login')
@auth.login_required
def login():
	return jsonify({"success": True})

api.add_resource(ProductosAll, 
	'/api/producto/listar',
	'/api/producto/listar/<string:serie>/<string:exacta>')
api.add_resource(Productos, 
	'/api/producto',
	'/api/producto/<int:id>')

api.add_resource(ContactosAll, 
	'/api/contacto/listar',
	'/api/contacto/listar/<string:nombre>')
api.add_resource(Contactos, 
	'/api/contacto',
	'/api/contacto/<int:id>')
api.add_resource(ContactosFacturasPendientes, 
	'/api/contacto/facturas/pendientes/<int:id>')

api.add_resource(GuiasAll, 
	'/api/guia/listar/<int:ciaId>',
	'/api/guia/listar/<int:ciaId>/<int:contactoId>/<string:numero>/<int:pagina>')

api.add_resource(GuiasTipo, '/api/guia/tipo/listar')

api.add_resource(GuiasDetalle, '/api/guia/detalle/<int:id>')

api.add_resource(GuiasDetalleResumen, '/api/guia/detalle/resumen/<int:id>')

#if __name__ == "__main__":
#	app.run(debug=True)