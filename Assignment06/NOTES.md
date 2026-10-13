# CS543 — Assignment 6 NOTES
## Honest Responses: status codes, errors & validation

## Team
- **Team ID:** T-04
- **Member 1:** Sahil  — Roll No.20252651055
- **Member 2:** Ritik  — Roll No. 20252651043
- **Member 3:** Jeeshan — Roll No. 20252651026
- **Member 4:** Kruti  — Roll No. 20252651027
- **Repo:** https://github.com/MdSahil1702/campuseats

---

## A1 — Outcome → status map

| Endpoint | Method | Success | Failures |
|---|---|---|---|
| /orders | POST | 201 Created | 400 malformed JSON, 401 missing token, 406 bad Accept, 422 validation |
| /orders/{id} | GET | 200 OK | 404 missing, 406 bad Accept |
| /orders/{id}/cancellation | POST | 200 OK | 401, 404, 409 illegal transition |
| /rate | GET | — | 429 with Retry-After: 30 |

**A2 — Fixed responses:** In A5, some errors returned `200 {"ok":false}`. In A6, every failure returns the correct 4xx/5xx status + Problem Details body. 200 is used only for genuine success.

**A3 — Location on create:** `POST /orders` → `201 Created` with `Location: /orders/{id}`.

**A4 — Retry safety:**
- 429 / 503 include `Retry-After` (seconds).
- Safe to retry: 429, 500, 502, 503, 504, network timeouts.
- Never retry: 400, 401, 403, 404, 406, 409, 412, 422.

---

## B1 — One error shape (RFC 7807 Problem Details)

Every failure passes through `send_problem()` and returns:
```json
{
  "type":   "https://campuseats.example.com/problems/validation-failed",
  "title":  "Validation Failed",
  "status": 422,
  "detail": "One or more fields failed validation.",
  "errors": [{"field": "items[0].qty", "reason": "must be >= 1"}]
}
