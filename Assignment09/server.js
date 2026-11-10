require('dotenv').config();
const express = require('express');
const path = require('path');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const SECRET = process.env.JWT_SECRET;
if (!SECRET) {
  console.error('JWT_SECRET is not set. Copy .env.example to .env and fill it in.');
  process.exit(1);
}

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ---------- Users (seeded, passwords stored only as bcrypt hashes) ----------
const users = [
  { id: 1, username: 'alice', role: 'customer',   passwordHash: bcrypt.hashSync('alice123', 10) },
  { id: 2, username: 'bob',   role: 'restaurant', passwordHash: bcrypt.hashSync('bob123', 10) },
];

// ---------- Catalogue data (from Assignment 8) ----------
const items = [
  { id: 1, name: 'Veg Thali',   price: 120, available: true  },
  { id: 2, name: 'Masala Dosa', price: 80,  available: true  },
  { id: 3, name: 'Paneer Wrap', price: 100, available: false },
  { id: 4, name: 'Cold Coffee', price: 60,  available: true  },
];
let nextId = items.length + 1;

// ---------- Middleware ----------
// Who are you?
function auth(req, res, next) {
  const token = (req.get('Authorization') || '').split(' ')[1];
  try {
    req.user = jwt.verify(token, SECRET);
    next();
  } catch {
    res.status(401).json({ error: 'invalid token' });
  }
}

// May you?
const requireRole = (...ok) => (req, res, next) =>
  ok.includes(req.user.role) ? next() : res.status(403).json({ error: 'forbidden' });

// ---------- Routes ----------
// Public: this is how a token is obtained
app.post('/login', (req, res) => {
  const { username, password } = req.body || {};
  const user = users.find((u) => u.username === username);
  if (!user || !bcrypt.compareSync(String(password || ''), user.passwordHash)) {
    return res.status(401).json({ error: 'invalid credentials' });
  }
  const token = jwt.sign({ id: user.id, role: user.role }, SECRET, { expiresIn: '1h' });
  res.json({ token });
});

// Authentication only
app.get('/items', auth, (req, res) => {
  res.status(200).json(items);
});

app.get('/items/:id', auth, (req, res) => {
  const id = Number(req.params.id);
  const item = items.find((i) => i.id === id);
  if (!item) {
    return res.status(404).json({ error: `item ${req.params.id} not found` });
  }
  res.status(200).json(item);
});

// Authentication + role
app.post('/items', auth, requireRole('restaurant', 'admin'), (req, res) => {
  const { name, price, available } = req.body || {};

  const missing = [];
  if (name === undefined || String(name).trim() === '') missing.push('name');
  if (price === undefined || price === null || price === '') missing.push('price');
  if (missing.length > 0) {
    return res.status(422).json({ error: `${missing.join(', ')} required` });
  }

  const priceNum = Number(price);
  if (Number.isNaN(priceNum) || priceNum < 0) {
    return res.status(422).json({ error: 'price must be a non-negative number' });
  }

  const newItem = {
    id: nextId++,
    name: String(name).trim(),
    price: priceNum,
    available: available === undefined ? true : Boolean(available),
  };
  items.push(newItem);
  res.status(201).json(newItem);
});

app.listen(PORT, () => {
  console.log(`Secured CampusEats Catalogue API running at http://localhost:${PORT}`);
});
