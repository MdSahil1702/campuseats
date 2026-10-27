# CampusEats — Assignment 7 (GraphQL: Dish / Catalogue service)

**Team T-04**

| Name | Roll No. |
|---|---|
| Sahil | 20252651055 |
| Ritik | 20252651043 |
| Jeeshan | 20252651026 |
| Kruti | 20252651027 |

**Repo:** https://github.com/MdSahil1702/campuseats

## How to run
```bash
cd Assignment07
mysql -u root -p < schema.sql      # creates DB + dishes table + 4 seed rows
npm install
DB_PASSWORD=yourpass npm start     # open http://localhost:4000  (GraphQL at /graphql)
```
(Env vars `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `PORT` are optional.)

## Answers

**1. Which CampusEats service did you pick?**
The **Catalogue service**, modelled around the `Dish` (menu item) entity: `id, name, price, available, description`.
Query: `dishes`, `dish(id)`. Mutations: `addDish`, `setDishAvailability`.

**2. One field a client can skip, one it cannot.**
- Can skip: `description` (declared `String`, nullable) — a client may also omit `available` in `AddDishInput`; it defaults to true.
- Cannot skip: `name` (`String!`) — and `price` (`Float!`). The `!` makes the field non-null, so the server must always return a value and the client must always supply it on input; leaving it out is rejected by validation before any resolver runs. This gives clients a guaranteed contract.

**3. Mapping to SQL.**
- `dishes(availableOnly: true)` became `SELECT * FROM dishes WHERE available = 1`; `dish(id: 2)` became `WHERE id = ?` (parameterised).
- The **`addDish` mutation resolver** runs the `INSERT INTO dishes (name, price, available, description) VALUES (?, ?, ?, ?)`; `setDishAvailability` runs the `UPDATE dishes SET available = ? WHERE id = ?`.

## Files
`schema.graphql`, `server.js`, `db.js`, `schema.sql`, `public/index.html`, `package.json`
