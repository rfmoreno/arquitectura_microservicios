const express = require('express');
const axios = require('axios');
const app = express();

app.set('view engine', 'pug');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// URLs de los servicios (ajusta según tus servicios y entorno Docker)
const API_USUARIOS = process.env.API_URL || 'http://flask_api_usuarios:5002/api/usuarios';
const API_PERFILES = process.env.API_URL_PERFILES || 'http://flask_api_usuarios:5002/api/perfiles';

// Listar usuarios y perfiles, mostrar formulario para agregar
app.get('/usuarios', async (req, res) => {
  try {
    const [usuariosRes, perfilesRes] = await Promise.all([
      axios.get(API_USUARIOS),
      axios.get(API_PERFILES)
    ]);
    res.render('usuarios', {
      usuarios: usuariosRes.data,
      perfiles: perfilesRes.data
    });
  } catch (err) {
    res.status(500).send('Error al obtener datos de usuarios o perfiles');
  }
});

// Mostrar formulario de edición
app.get('/usuarios/:id/edit', async (req, res) => {
  try {
    const id = req.params.id;
    const [usuarioRes, perfilesRes] = await Promise.all([
      axios.get(`${API_USUARIOS}/${id}`),
      axios.get(API_PERFILES)
    ]);
    res.render('usuario_edit', {
      usuario: usuarioRes.data,
      perfiles: perfilesRes.data
    });
  } catch (err) {
    res.status(500).send('Error al obtener datos del usuario');
  }
});

// Crear usuario
app.post('/usuarios', async (req, res) => {
  try {
    await axios.post(API_USUARIOS, {
      nombre_completo: req.body.nombre_completo,
      login: req.body.login,
      email: req.body.email,
      password: req.body.password,
      id_perfil: req.body.id_perfil
    });
    res.redirect('/usuarios');
  } catch (err) {
    res.status(500).send('Error al crear usuario');
  }
});

// Actualizar usuario
app.post('/usuarios/:id/edit', async (req, res) => {
  try {
    const id = req.params.id;
    await axios.put(`${API_USUARIOS}/${id}`, {
      nombre_completo: req.body.nombre_completo,
      login: req.body.login,
      email: req.body.email,
      password: req.body.password || undefined,
      id_perfil: req.body.id_perfil
    });
    res.redirect('/usuarios');
  } catch (err) {
    res.status(500).send('Error al actualizar usuario');
  }
});

// Eliminar usuario
app.post('/usuarios/:id/delete', async (req, res) => {
  try {
    await axios.delete(`${API_USUARIOS}/${req.params.id}`);
    res.redirect('/usuarios');
  } catch (err) {
    res.status(500).send('Error al eliminar usuario');
  }
});

const port = 3002;
app.listen(port, () => {
  console.log(`Vista Usuarios corriendo en http://localhost:${port}/usuarios`);
});
