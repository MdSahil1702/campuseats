
const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;


app.use(express.json());


app.use(express.static(path.join(__dirname, 'public')));


const items = [
  { id: 1, name: 'Veg Thali',        price: 120, available: true  },
  { id: 2, name: 'Masala Dosa',      price: 80,  available: true  },
  { id: 3, name: 'Paneer Wrap',      price: 100, available: false },
  { id: 4, name: 'Cold Coffee',      price: 60,  available: true  },
];
let nextId = items.length + 1;


app.get('/items', (req, res) => {
  res.status(200).json(items);
});

app.get('/items/:id', (req, res) => {
  const id = Number(req.params.id);
  const item = items.find((i) => i.id === id);
  if (!item) {
    return res.status(404).json({ error: `item ${req.params.id} not found` });
  }
  res.status(200).json(item);
});


app.post('/items', (req, res) => {
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
  console.log(`CampusEats Catalogue API running at http://localhost:${PORT}`);
});
