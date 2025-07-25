from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route('/api/enviar_correo', methods=['POST'])
def enviar_correo():
    data = request.json
    correo = data.get('correo')
    productos = data.get('productos')  # se espera lista con dicts o detalles

    if not correo or productos is None:
        return jsonify({'error': 'Faltan parámetros correo o productos'}), 400

    # Simulación de envío de correo (solo log)
    logging.info(f"Enviando correo a: {correo}")
    logging.info(f"Productos adquiridos:")
    for p in productos:
        # suponemos que p tiene nombre, cantidad y costo_total (o similar)
        logging.info(f"- {p.get('nombre', 'producto unknown')} x {p.get('cantidad', '?')} - Costo: ${p.get('costo_total', '?')}")

    logging.info(f"Correo enviado con éxito a: {correo}")

    return jsonify({'status': 'correo enviado (simulado)'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
