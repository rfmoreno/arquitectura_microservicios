from flask import Flask, request, jsonify
from model_py.model import crear_pedido, obtener_pedidos
import requests
import os

app = Flask(__name__)

PRODUCTOS_API = os.getenv('PRODUCTOS_API', 'http://flask_api_productos:5001/api/productos')

@app.route('/api/pedidos', methods=['GET'])
def pedidos():
    return jsonify(obtener_pedidos())

@app.route('/api/pedidos', methods=['POST'])
def nuevo_pedido():
    data = request.json
    usuario_id = data.get('usuario_id')
    productos_pedido = data.get('productos', [])

    if not usuario_id or not productos_pedido:
        return {'error': 'Faltan datos de usuario o productos'}, 400

    detalles = []
    total = 0.0
    for idx, item in enumerate(productos_pedido):
        r = requests.get(f"{PRODUCTOS_API}/{item['productoId']}")
        if r.status_code != 200:
            return {'error': f"Producto {item['productoId']} no encontrado"}, 400
        prod_data = r.json()
        cantidad = item.get('cantidad', 0)
        if prod_data.get('stock', 0) < cantidad:
            return {'error': f"Stock insuficiente para producto {prod_data.get('nombre', 'desconocido')}"}, 400
        subtotal = prod_data.get('precio', 0) * cantidad
        total += subtotal
        detalles.append(f"{prod_data.get('nombre', '???')} x {cantidad} (${prod_data.get('precio')} c/u = ${subtotal})")

    detalles_str = "; ".join(detalles)
    estado_pago = 'pagado'  # simulado

    pedido_id = crear_pedido(usuario_id, estado_pago, detalles_str, total)
    return jsonify({'pedido_id': pedido_id, 'status': 'confirmado', 'total': total})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
