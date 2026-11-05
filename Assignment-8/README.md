# CampusEats Catalogue – REST API (CS543 Assignment 8)

**Run it:** `npm install && npm start`, then open http://localhost:3000

## Team

| Name              | Role        | Roll / Enrollment No. |
| ----------------- | ----------- | --------------------- |
| Siddiqui Md Sahil | Team Leader | 20252651055           |
| Ritik Kumar Sinha | Team Member | 20252651043           |
| Jeeshan Adil      | Team Member | 20252651026           |
| Kruti Kansagara   | Team Member | 20252651027           |

## Links

- Demo video (Google Drive): https://drive.google.com/file/d/1Nzo2o5gEeVc49NGXbJZUGRIqAoJfgefD/view?usp=drive_link
- Screenshots: Added at the path  /screenshots/before.png, /screenshots/after.png

## Answers

**1. Which CampusEats service did you pick, and what are its routes?**

We picked the **Menu / Catalogue** service. Each item has `id`, `name`, `price`, `available`.

| Method | Path         | Purpose                  |
| ------ | ------------ | ------------------------ |
| GET    | `/items`     | List all menu items      |
| GET    | `/items/:id` | Fetch one menu item      |
| POST   | `/items`     | Create a new menu item   |

**2. Which status codes did you return, and for which outcomes?**

- **200 OK** – `GET /items` and `GET /items/:id` when the item exists.
- **201 Created** – `POST /items` when the item was created (the new item is returned).
- **404 Not Found** – `GET /items/:id` when no item has that id.
- **422 Unprocessable Entity** – `POST /items` when a required field (`name` or `price`) is missing, or `price` is not a valid number.

**3. Where did you use `req.params` and where `req.body`? Why does POST need `express.json()`?**

- `req.params.id` is used in `GET /items/:id` to read the id from the URL path.
- `req.body` is used in `POST /items` to read the JSON the client sent (`name`, `price`, `available`).
- By default Express does not read the request body, so `req.body` would be `undefined`. `app.use(express.json())` parses JSON bodies and fills `req.body`.

## Files

- `server.js` – Express API (routes, validation, in-memory data)
- `package.json` – lists `express` as a dependency
- `public/index.html`, `public/style.css` – page that lists and adds items

## Contributions

- Siddiqui Md Sahil – `server.js`, repo setup, submission
- Ritik Kumar Sinha – `public/index.html`
- Jeeshan Adil – `public/style.css`
- Kruti Kansagara – `README.md`, `package.json`, screenshots and demo video
