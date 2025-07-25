from flask import Flask, request, jsonify
import requests
import hashlib
import os
import pika
import json

app = Flask(__name__)

API_USUARIOS = os.getenv('API_USUARIOS', 'http://flask_api_usuarios:5002/api/usuarios')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')

def enviar_evento_login(usuario_id, login):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='logins')
        mensaje = json.dumps({'usuario_id': usuario_id, 'login': login})
        channel.basic_publish(exchange='', routing_key='logins', body=mensaje)
        connection.close()
    except Exception as e:
        print(f"No se pudo enviar evento a RabbitMQ: {e}")

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user_login = data.get('login')
    password = data.get('password')
    
    if not user_login or not password:
        return {'error': 'Faltan login o password'}, 400

    # Obtener lista de usuarios para buscar login
    resp = requests.get(API_USUARIOS)
    if resp.status_code != 200:
        return {'error': 'No se pudo validar usuario'}, 500

    usuarios = resp.json()
    
    # Buscar usuario por login
    usuario = next((u for u in usuarios if u['login'] == user_login), None)
    if usuario is None:
        return {'error': 'Usuario no encontrado'}, 404

    # Calcular hash MD5 del password recibido
    hash_submit = hashlib.md5(password.encode('utf-8')).hexdigest()

    # Obtener datos detallados del usuario para obtener el hash almacenado y el perfil
    user_detail_resp = requests.get(f"{API_USUARIOS}/{usuario['id']}")
    if user_detail_resp.status_code != 200:
        return {'error': 'Error al obtener detalles de usuario'}, 500
    
    user_detail = user_detail_resp.json()
    hash_guardado = user_detail.get('hash_password')

    if hash_guardado != hash_submit:
        return {'error': 'Password incorrecta'}, 401
    
    perfil = user_detail.get('perfil', 'desconocido')

    # Enviar evento a RabbitMQ (opcional)
    enviar_evento_login(usuario['id'], usuario['login'])

    # Devolver respuesta con perfil incluido
    return {
        'message': 'Login exitoso',
        'usuario_id': usuario['id'],
        'login': usuario['login'],
        'perfil': perfil
    }, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
