const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const mysql = require('mysql2');

const app = express();
app.use(cors());
app.use(bodyParser.json());

// ✅ MySQL connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',     // your MySQL username
  password: '',     // your MySQL password
  database: 'demo_db'
});

db.connect(err => {
  if (err) {
    console.log('❌ MySQL connection error:', err);
  } else {
    console.log('✅ Connected to MySQL Database');
  }
});

// ✅ API to save user
app.post('/api/users', (req, res) => {
  const { name, email } = req.body;

  const sql = 'INSERT INTO users (name, email) VALUES (?, ?)';
  db.query(sql, [name, email], (err, result) => {
    if (err) {
      console.log(err);
      return res.json({ message: 'Error saving user' });
    }
    res.json({ message: 'User saved successfully!' });
  });
});

// ✅ API to get all users
app.get('/api/users', (req, res) => {
  db.query('SELECT * FROM users', (err, results) => {
    if (err) throw err;
    res.json(results);
  });
});

// ✅ Start the server
app.listen(5000, () => {
  console.log('🚀 Server running on http://localhost:5000');
});
