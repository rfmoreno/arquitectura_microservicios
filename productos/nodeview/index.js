const express = require('express');
const axios = require('axios');
const app = express();
app.set('view engine', 'pug');
app.use(express.urlencoded({ extended: true }));

const API_URL = process.env.API_URL || 'http://flask_api_productos:5001/api/productos';

app.get('/productos', async (req, res) => {
  try {
    const { data } = await axios.get(API_URL);
    res.render('productos', { productos: data });
  } catch (error) {
    res.status(500).send("Error al obtener productos");
  }
});

app.post('/productos', async (req, res) => {
  try {
    await axios.post(API_URL, req.body);
    res.redirect('/productos');
  } catch (error) {
    res.status(500).send("Error al crear producto");
  }
});

// Ruta para eliminar producto
app.post('/productos/:id/delete', async (req, res) => {
  const id = req.params.id;
  try {
    await axios.delete(`${API_URL}/${id}`);
    res.redirect('/productos');
  } catch (error) {
    res.status(500).send("Error al eliminar producto");
  }
});

app.listen(3001, () => console.log('Vista Productos en puerto 3001'));














