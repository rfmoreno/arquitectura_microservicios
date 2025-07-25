const express = require('express');
const axios = require('axios');
const session = require('express-session');
const app = express();

app.set('view engine', 'pug');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Configura la sesión para mantener usuario logueado (ajusta el secret en producción)
app.use(session({
  secret: 'pedidos_secret_key',
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false } // true solo con HTTPS en producción
}));

const API_PEDIDOS = process.env.API_URL || 'http://flask_api_pedidos:5003/api/pedidos';
const API_USUARIOS = process.env.API_USUARIOS || 'http://flask_api_usuarios:5002/api/usuarios';
const API_PRODUCTOS = process.env.API_PRODUCTOS || 'http://flask_api_productos:5001/api/productos';
const API_MENSAJERIA = process.env.API_MENSAJERIA || 'http://mensajeria_flaskapi:5006/api/enviar_correo';

// Middleware para simular usuario logueado (debes adaptar para sesión real)
app.use(async (req, res, next) => {
  if (!req.session.usuario) {
    try {
      const usuarioRes = await axios.get(`${API_USUARIOS}/1`); // Por defecto usuario id=1
      req.session.usuario = {
        login: usuarioRes.data.login,
        perfil: usuarioRes.data.perfil,
        email: usuarioRes.data.email,
        id: usuarioRes.data.id
      };
    } catch (e) {
      req.session.usuario = { login: 'invitado', perfil: '-', email: '', id: null };
    }
  }
  next();
});

// Ruta para mostrar la vista de pedidos
app.get('/pedidos', async (req, res) => {
  try {
    const [pedidosRes, productosRes] = await Promise.all([
      axios.get(API_PEDIDOS),
      axios.get(API_PRODUCTOS)
    ]);

    res.render('pedidos', {
      pedidos: pedidosRes.data,
      productos: productosRes.data,
      usuario: req.session.usuario
    });
  } catch (error) {
    res.status(500).send('Error al obtener datos de pedidos o productos.');
  }
});

// Ruta para simular la pantalla de pago
app.post('/pagos', async (req, res) => {
  try {
    const productos = JSON.parse(req.body.productos);
    const usuarioActivo = req.session.usuario;

    res.render('pago_fake', {
      usuario_id: usuarioActivo.id,
      productos: productos,
      total: productos.reduce((acc, p) => acc + Number(p.costo_total), 0),
      usuario: usuarioActivo
    });
  } catch (error) {
    res.status(500).send('Error al procesar pago: ' + error.message);
  }
});

// **Nuevo:** Ruta para confirmar pago y llamar al microservicio mensajería
app.post('/confirmar_pago', async (req, res) => {
  try {
    const usuario = req.session.usuario;
    let productos = [];
    if (typeof req.body.productos === 'string') {
      productos = JSON.parse(req.body.productos);
    } else if (Array.isArray(req.body.productos)) {
      productos = req.body.productos;
    }

    // Consumir el microservicio mensajería para "enviar" el correo
    await axios.post(API_MENSAJERIA, {
      correo: usuario.email,
      productos: productos
    });

    // Aquí puedes redireccionar o renderizar mensaje de éxito
    res.send(`<h1>Pago realizado y correo enviado exitosamente a ${usuario.email}</h1>
              <p><a href="/pedidos">Volver a Pedidos</a></p>`);
  } catch (error) {
    console.error(error?.response?.data || error.message);
    res.status(500).send('Error al procesar el pago y enviar correo.');
  }
});

const port = 3003;
app.listen(port, () => {
  console.log(`Vista Pedidos corriendo en http://localhost:${port}/pedidos`);
});
