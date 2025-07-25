# arquitectura_microservicios
Este manual guía el despliegue de la solución completa del repositorio arquitectura_microservicios usando Docker Compose.
1. Pre-requisitos
    Docker instalado en tu sistema (Descargar Docker).
    Docker Compose instalado (Instrucciones Docker Compose).
    Acceso al repositorio (clonado en tu máquina local):
    bash
    git clone https://github.com/rfmoreno/arquitectura_microservicios.git
    cd arquitectura_microservicios
2. Estructura de Contenedores
El sistema levantará los siguientes servicios (cada uno con su contenedor):
    MySQL: Base de datos central.
    RabbitMQ: Broker de mensajería (con panel en :15672).
    API Flask de Usuarios (flask_api_usuarios)
    Vista Node.js de Usuarios (nodeview_usuarios)
    API Flask de Productos (flask_api_productos)
    Vista Node.js de Productos (nodeview_productos)
    API Flask de Pedidos (flask_api_pedidos)
    Vista Node.js de Pedidos (nodeview_pedidos)
    API Flask Login (login_flaskapi)
    Vista Node.js Login (login_nodeview)
    API Flask Mensajería (mensajeria_flaskapi)
3. Primeros pasos y configuración inicial
    Configura las variables de entorno si lo deseas.
    Puedes editar variables directamente en el archivo docker-compose.yml según tus necesidades (ejemplo: credenciales de DB, nombres de host/servicio).
    Revisa y personaliza los puertos expuestos en docker-compose.yml si tienes conflictos en tu máquina.
4. Despliegue de todos los servicios
    Desde la raíz del proyecto:
    bash
    docker compose build
    docker compose up -d
    Esto construirá (si es la primera vez) e iniciará todos los servicios en segundo plano (modo daemon).
5. Acceso a cada interfaz y paneles
    Usuarios
        Frontend: http://localhost:3002/usuarios
        API: http://localhost:5002/api/usuarios
    Productos
        Frontend: http://localhost:3001/productos
        API: http://localhost:5001/api/productos
    Pedidos
        Frontend: http://localhost:3003/pedidos
        API: http://localhost:5003/api/pedidos
    Login
        Interfaz: http://localhost:3005/login
        API: http://localhost:5005/api/login
    Mensajería
        API: http://localhost:5006/api/enviar_correo
    RabbitMQ
        Panel de gestión: http://localhost:15672
        Usuario/Contraseña por defecto: guest / guest
    MySQL
        Puerto: 3306, se puede conectar usando cualquier cliente compatible con MySQL.
6. Detener y eliminar los contenedores
    Para detener todos los servicios:
    bash
    docker compose down

    Para limpiar volúmenes (datos de bases de datos):

    bash
    docker compose down -v

7. Consideraciones y comandos útiles
    Para reconstruir un servicio tras cambios en código:
    bash
    docker compose build <nombre_servicio>
    docker compose restart <nombre_servicio>
Ejemplo para usuarios:
    bash
    docker compose build flask_api_usuarios nodeview_usuarios
    docker compose restart flask_api_usuarios nodeview_usuarios
Para ver el estado de los contenedores:
    bash
    docker compose ps
Para ver los logs de un servicio (ayuda para depuración):
    bash
    docker compose logs <nombre_servicio>
8. Flujo resumido de uso
    Arranca toda la arquitectura (docker compose up -d).
    Accede a las interfaces web para crear usuarios, productos, pedidos, realizar logins, etc.
    Cuando realices un pago desde la vista de pedidos, el microservicio de mensajería simulará el envío de correo (visible por consola en los logs de mensajería).
    Detén o reinicia servicios según tu flujo de trabajo.
9. Notas finales
    El sistema está diseñado para uso y pruebas educativas, no para producción directa.
    La mensajería y los pagos son simulados, configurados para demostrar flujos y no realizar operaciones reales.
    Puedes consultar la arquitectura y versiones en el archivo docker-compose.yml.
