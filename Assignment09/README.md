# CampusEats Catalogue – Secured API (CS543 Assignment 9)

Catalogue REST service from Assignment 8, now secured with **bcrypt**, **JWT**, an `auth` middleware and a `requireRole` middleware.

## Team

| Name              | Role        | Roll / Enrollment No. |
| ----------------- | ----------- | --------------------- |
| Siddiqui Md Sahil | Team Leader | 20252651055           |
| Ritik Kumar Sinha | Team Member | 20252651043           |
| Jeeshan Adil      | Team Member | 20252651026           |
| Kruti Kansagara   | Team Member | 20252651027           |

## Demo (Drive link)

https://drive.google.com/drive/folders/1t_5XmKHfiwpgexTz6giEAzN4N9nLOx_S?usp=drive_link
## Run locally

```bash
npm install
cp .env.example .env      # then put a long random value in JWT_SECRET
npm start                 # http://localhost:3000
```

Seeded users (passwords are stored only as bcrypt hashes):

| username | password | role       |
| -------- | -------- | ---------- |
| alice    | alice123 | customer   |
| bob      | bob123   | restaurant |

## Routes

| Method | Path         | Guard                                        |
| ------ | ------------ | -------------------------------------------- |
| POST   | `/login`     | public                                       |
| GET    | `/items`     | `auth`                                       |
| GET    | `/items/:id` | `auth`                                       |
| POST   | `/items`     | `auth` + `requireRole('restaurant','admin')` |

## Demo commands (curl)

```bash
# 1) No token -> 401
curl -i http://localhost:3000/items

# 2) Login -> token
curl -s -X POST http://localhost:3000/login -H 'Content-Type: application/json' \
  -d '{"username":"alice","password":"alice123"}'
# (do the same for bob; copy each token into CUSTOMER_TOKEN / RESTAURANT_TOKEN)

# 3) With token -> 200
curl -i http://localhost:3000/items -H "Authorization: Bearer $CUSTOMER_TOKEN"

# 4) Restaurant creates item -> 201
curl -i -X POST http://localhost:3000/items -H "Authorization: Bearer $RESTAURANT_TOKEN" \
  -H 'Content-Type: application/json' -d '{"name":"Samosa Chaat","price":50}'

# 5) Customer on the write route -> 403
curl -i -X POST http://localhost:3000/items -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  -H 'Content-Type: application/json' -d '{"name":"Hack","price":1}'
```

Expected results: `401` (no token), `200` + token (login), `200` (GET with token), `201` (restaurant POST), `403` (customer POST).

The web page (`public/index.html`) also has a login bar: log in as `alice` to view the menu, or as `bob` to add dishes.

---

## Answers

### 1. Which routes need only authentication, and which also need a role?

- **Authentication only:** `GET /items` and `GET /items/:id` – any user with a valid token (customer, restaurant, admin).
- **Authentication + role:** `POST /items` – only `restaurant` (or `admin`).
- `POST /login` is public (it is how a token is obtained).

### 2. One 401 and one 403, and why

- **401** – `GET /items` with no `Authorization` header: the server does not know *who* the caller is (no valid token), so authentication failed. It is not 403 because we never got as far as checking permissions.
- **403** – `POST /items` by `alice` (customer) with a valid token: the server knows exactly who she is (authentication passed), but her role is not allowed to write. It is not 401 because her identity is valid.

### 3. JWT payload, trusting the role, and the secret

- **Payload:** `{ "id": 2, "role": "restaurant", "iat": ..., "exp": ... }` – user id, role, issued-at and expiry (1 hour).
- **Why the role claim can be trusted:** the token is signed (HMAC-SHA256) with the server's secret. If a client edits the payload (e.g. changes `customer` to `restaurant`), the signature no longer matches and `jwt.verify` rejects it. Only a holder of the secret can create a valid token.
- **Why the secret must stay out of the code:** anyone who learns the secret can forge tokens with any role (e.g. admin). Code goes to GitHub, so the secret is read from `process.env.JWT_SECRET` (a git-ignored `.env`); only `.env.example` with a blank value is committed.
