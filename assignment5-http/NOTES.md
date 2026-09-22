# CS543 — Assignment 5 NOTES

## Team
- **Member 1:** Sahil — Roll No. 20252651055
- **Member 2:** Ritik — Roll No. 20252651043
- **Member 3:** Jeeshan — Roll No. 20252651026
- **Member 4:** Kruti — Roll No. 20252651027
- **Repo:** https://github.com/MdSahil1702/campuseats

---

## A1 — Campus Eats Method Map (action → method + URL)

| Action | Method | URL | Safe? | Idempotent? |
|---|---|---|---|---|
| List orders | GET | `/orders` | ✅ | ✅ |
| Read order | GET | `/orders/{id}` | ✅ | ✅ |
| Create order | POST | `/orders` | ❌ | ❌ (retry-safe via Idempotency-Key) |
| Replace order | PUT | `/orders/{id}` | ❌ | ✅ |
| Modify order | PATCH | `/orders/{id}` | ❌ | ❌ (guarded by If-Match) |
| Delete order | DELETE | `/orders/{id}` | ❌ | ✅ |
| Cancel order | POST | `/orders/{id}/cancellation` | ❌ | ❌ (guarded; 409 on repeat) |
| Checkout | POST | `/orders/{id}/checkout` | ❌ | ❌ |
| Set availability | POST | `/restaurants/{id}/availability` | ❌ | ❌ |
| Options / discovery | OPTIONS | `/orders` | ✅ | ✅ |
| Redirect to order | GET | `/orders/{id}/receipt` | ✅ | ✅ |

**No verb leaked into a URL** — verbs (`cancel`, `checkout`, `availability`) live only inside sub-resource paths, never as the URI action.

---

## A6 — One full exchange (raw HTTP)

```
POST /orders HTTP/1.1                          ← request line
Host: localhost:8085                           ← required header
Authorization: Bearer campuseats-token         ← auth
Content-Type: application/json                 ← body type
Accept: application/json                       ← desired response
Idempotency-Key: demo-key-1                    ← retry safety
Content-Length: 71

{"customer":"sahil","items":[{"id":"pizza","qty":2}]}   ← body
```
```
HTTP/1.1 201 Created                           ← status line
Location: /orders/1                            ← new resource URI
ETag: "a1b2c3d4e5f60718"                       ← concurrency token
Content-Type: application/json
Content-Length: 89

{"id":1,"customer":"sahil","items":[...],"status":"PLACED"}
```
Request line = `POST /orders HTTP/1.1` → **HTTP version = HTTP/1.1**.

---

## D2 — Headers table

| Endpoint | Method | Request headers needed | Response headers set |
|---|---|---|---|
| `/orders` | GET | `Accept`, `Accept-Encoding` | `Content-Type`, `X-RateLimit-*`, `Cache-Control` |
| `/orders` | POST | `Authorization`, `Content-Type`, `Idempotency-Key`, `Accept` | `Location`, `ETag`, `X-RateLimit-*` |
| `/orders/{id}` | GET | `Authorization`, `If-None-Match`, `Accept` | `ETag`, `Cache-Control`, `X-RateLimit-*` |
| `/orders/{id}` | PUT | `Authorization`, `If-Match`, `Content-Type` | `ETag` |
| `/orders/{id}` | PATCH | `Authorization`, `If-Match`, `Content-Type` | `ETag` |
| `/orders/{id}` | DELETE | `Authorization` | *(none, 204)* |
| `/orders/{id}/cancellation` | POST | `Authorization`, `Content-Type` | `ETag` |
| Any | OPTIONS | `Origin`, `Access-Control-Request-Method` | `Allow`, `Access-Control-Allow-*` |
| Any (error) | — | — | `X-Content-Type-Options: nosniff`, `Strict-Transport-Security` |

---

## C4 — Safe-retry plan

| Endpoint | Safe? | Idempotent? | Mechanism | Why |
|---|---|---|---|---|
| `GET /orders` | ✅ | ✅ | none needed | Pure read |
| `GET /orders/{id}` | ✅ | ✅ | `If-None-Match` + ETag | 304 saves bandwidth |
| `POST /orders` | ❌ | ❌ | **Idempotency-Key** | Prevents duplicate charges/orders |
| `PUT /orders/{id}` | ❌ | ✅ | `If-Match` | Prevents lost updates |
| `PATCH /orders/{id}` | ❌ | ❌ | `If-Match` | Prevents lost updates |
| `DELETE /orders/{id}` | ❌ | ✅ | none (DELETE is idempotent) | 2nd call → 404, no harm |
| `POST .../cancellation` | ❌ | ❌ | 409 on repeat | Prevents refund-twice |

**Where a duplicate would do real damage:** `POST /orders` — a network retry after a lost 201 could create a second order and double-charge the customer. Idempotency-Key collapses the retry to the original result.

---

## C1/C2 — ETag demonstration

**Initial GET produces:** `ETag: "a1b2c3d4e5f60718"`

**Request → 304 Not Modified:**
```
GET /orders/1 HTTP/1.1
Authorization: Bearer campuseats-token
If-None-Match: "a1b2c3d4e5f60718"
```
**Response:** `304 Not Modified` — saves **bandwidth** (no body re-sent).

**Request → 412 Precondition Failed:**
```
PUT /orders/1 HTTP/1.1
Authorization: Bearer campuseats-token
If-Match: "stale-etag-00000000"
Content-Type: application/json

{"status":"PAID"}
```
**Response:** `412 Precondition Failed` — prevents **lost update** when another writer changed the resource first.

---

## ANSWERS TO THE 8 QUESTIONS

### 1. Three endpoints — method, success status, most important header

| Endpoint | Method | Status | Key header | Why |
|---|---|---|---|---|
| `POST /orders` | POST | **201** | `Location` | Client must learn the new resource URI |
| `GET /orders/{id}` | GET | **200** | `ETag` | Enables conditional GET → 304 |
| `PUT /orders/{id}` | PUT | **200** | `ETag` (new) | Lets subsequent writes use `If-Match` |

### 2. Safe / idempotent / neither

- **Safe:** all GETs, OPTIONS.
- **Idempotent:** GET, PUT, DELETE, OPTIONS.
- **Neither:** `POST /orders`, `PATCH /orders/{id}`, `POST .../cancellation`.
- **Made retry-safe:** `POST /orders` uses the **Idempotency-Key** header. Same key → identical 201 with no duplicate order created.

### 3. ETag / 304 / 412

- ETag from service: `"a1b2c3d4e5f60718"` on `GET /orders/1`.
- **304 request:** `If-None-Match: "a1b2c3d4e5f60718"` → saves **bandwidth and CPU** on repeated reads.
- **412 request:** `PUT` with a stale `If-Match` → prevents **lost updates** between concurrent writers.

### 4. 422 vs 400

- **422 Unprocessable Entity:** syntactically valid JSON but semantically wrong —
  `POST /orders` with body `{"customer":"","items":[]}` → 422 (missing required fields).
- **400 Bad Request:** unparseable JSON —
  `POST /orders` with body `{"customer":` → 400 (JSON syntax error).
- **Difference:** 400 = parser refused; 422 = parser accepted but the domain layer rejected.

### 5. Cross-origin browser blocked but server logs 200

The **browser (Same-Origin Policy)** blocks the response — the server actually returned 200. Fix: send `Access-Control-Allow-Origin: *` (or the exact origin) **and** answer the OPTIONS preflight with `Access-Control-Allow-Methods` / `Access-Control-Allow-Headers`. Both are set in `server5.py`.

### 6. Cache-Control choices

- **Caching allowed:** `GET /orders/{id}` → `Cache-Control: public, max-age=60`. Public read-only data, safe to cache for 60 s.
- **no-store required:** `GET /orders/{id}/checkout-result` (or any endpoint returning a payment/personal payload) → `Cache-Control: no-store` so intermediaries and the browser never persist it.

### 7. Why is search a GET, and when would POST be right?

- Search is a **pure read**: no state change, so GET is correct, and the query string is cacheable and shareable.
- Use **POST** when: the query is too long for a URL, contains sensitive data you don't want logged, uses a complex structured body, or spans non-idempotent semantics.
- **Give up:** HTTP caching, safe/idempotent guarantees, bookmarkability, and standard 200-from-cache behaviour.

### 8. Location on 201 vs 3xx

- **201 Created:** `Location` points to the **newly created resource** (`/orders/1`).
- **3xx (302/303):** `Location` points to the **target of the redirect** — here `/orders/{id}/receipt` → `303 See Other` → `Location: /orders/{id}`.
