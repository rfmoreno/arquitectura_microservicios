const express = require('express');
const axios = require('axios');
const app = express();

app.set('view engine', 'pug');
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const API_LOGIN = process.env.API_LOGIN || 'http://login_flaskapi:5005/api/login';

app.get('/login', (req, res) => {
  res.render('login', { error: null });
});

app.post('/login', async (req, res) => {
  try {
    const { login, password } = req.body;
    const response = await axios.post(API_LOGIN, { login, password });

    // Si login exitoso, redirige a pedidos o muestra info
    res.render('login_success', { usuario: response.data });
  } catch (error) {
    let errMsg = 'Error desconocido';
    if (error.response && error.response.data && error.response.data.error) {
      errMsg = error.response.data.error;
    }
    res.render('login', { error: errMsg });
  }
});

const port = 3005;
app.listen(port, () => {
  console.log(`Vista Login corriendo en http://localhost:${port}/login`);
});
