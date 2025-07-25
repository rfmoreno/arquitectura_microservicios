from flask import Flask, request, jsonify
from model_py.model import obtener_productos, crear_producto, eliminar_producto

app = Flask(__name__)

@app.route('/api/productos', methods=['GET'])
def productos():
    return jsonify(obtener_productos())

@app.route('/api/productos', methods=['POST'])
def nuevo_producto():
    data = request.json
    crear_producto(data['nombre'], data['precio'], data['stock'])
    return {'status': 'ok'}, 201

@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def borrar_producto(producto_id):
    eliminado = eliminar_producto(producto_id)
    if eliminado:
        return {'status': 'deleted'}, 200
    else:
        return {'error': 'Producto no encontrado'}, 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

