from flask import Flask, request, jsonify
from model_py.model import (obtener_usuarios, crear_usuario, eliminar_usuario, 
                            obtener_perfiles, modificar_usuario, obtener_usuario_por_id)

app = Flask(__name__)

@app.route('/api/usuarios', methods=['GET'])
def usuarios():
    return jsonify(obtener_usuarios())

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def usuario_por_id(usuario_id):
    usuario = obtener_usuario_por_id(usuario_id)
    if usuario:
        return jsonify(usuario)
    else:
        return {'error': 'Usuario no encontrado'}, 404

@app.route('/api/usuarios', methods=['POST'])
def nuevo_usuario():
    data = request.json
    required_fields = ('nombre_completo', 'login', 'email', 'password', 'id_perfil')
    if not all(k in data for k in required_fields):
        return {'error': 'Faltan datos'}, 400
    crear_usuario(data['nombre_completo'], data['login'], data['email'], data['password'], data['id_perfil'])
    return {'status': 'ok'}, 201

@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    data = request.json
    nombre_completo = data.get('nombre_completo')
    login = data.get('login')
    email = data.get('email')
    password = data.get('password')
    id_perfil = data.get('id_perfil')

    if not all([nombre_completo, login, email, id_perfil]):
        return {'error': 'Faltan campos requeridos'}, 400

    try:
        modificar_usuario(usuario_id, nombre_completo, login, email, password, id_perfil)
    except Exception as e:
        return {'error': str(e)}, 400

    return {'status': 'updated'}, 200

@app.route('/api/perfiles', methods=['GET'])
def perfiles():
    return jsonify(obtener_perfiles())

@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
def borrar_usuario(usuario_id):
    eliminado = eliminar_usuario(usuario_id)
    if eliminado:
        return {'status': 'deleted'}, 200
    else:
        return {'error': 'Usuario no encontrado'}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
