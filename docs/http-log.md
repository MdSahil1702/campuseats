# HTTP Log

## Request 1 — GET `/users/1`

### Request

```sh
curl.exe -i https://jsonplaceholder.typicode.com/users/1
```

### Response

```text
HTTP/1.1 200 OK
Date: Sun, 16 Aug 2026 15:22:18 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 509
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"1fd-+2Y3G3w049iSZtw5t1mzSnunngE"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=6DQIIPkCgnZS0mG6n6a1gC5gfYOBpO568WJCudBefYY%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786671173"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=6DQIIPkCgnZS0mG6n6a1gC5gfYOBpO568WJCudBefYY%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786671173"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786671192
Age: 20522
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2c16f0b8b9811ea-BOM
alt-svc: h3=":443"; ma=86400

{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  "address": {
    "street": "Kulas Light",
    "suite": "Apt. 556",
    "city": "Gwenborough",
    "zipcode": "92998-3874",
    "geo": {
      "lat": "-37.3159",
      "lng": "81.1496"
    }
  },
  "phone": "1-770-736-8031 x56442",
  "website": "hildegard.org",
  "company": {
    "name": "Romaguera-Crona",
    "catchPhrase": "Multi-layered client-server neural-net",
    "bs": "harness real-time e-markets"
  }
} 
```
**Status:** `200` means the server successfully processed the request and returned the requested resource.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.



## Request 2 — GET `/posts/1`

### Request

```sh
curl.exe -i https://jsonplaceholder.typicode.com/posts/1
```

### Response

```text

HTTP/1.1 200 OK
Date: Sun, 16 Aug 2026 15:26:28 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 292
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=vm67FVLNHsCgrFgubRa04ooDeMKdgwXS9H3i2IbjuoY%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785194657"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=vm67FVLNHsCgrFgubRa04ooDeMKdgwXS9H3i2IbjuoY%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785194657"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1785194663
Age: 91
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2c17525c9c6d5f0-BOM
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
  "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
}
```
**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.

**Content-Type:** `application/json; charset=utf-8` means the response body is JSON data encoded using UTF-8.


## Request 3 — GET `/todos/1`

### Request

```sh
curl.exe -i https://jsonplaceholder.typicode.com/todos/1
```

### Response

```text

HTTP/1.1 200 OK
Date: Sun, 16 Aug 2026 15:27:08 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 83
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"53-hfEnumeNh6YirfjyjaujcOPPT+s"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=pPIQx95rCmGqlkWM4Hc1nzNceT7AChYmtTSg7OBqihc%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1785250921"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=pPIQx95rCmGqlkWM4Hc1nzNceT7AChYmtTSg7OBqihc%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1785250921"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1785250943
Age: 25113
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2c1761b18407e53-BOM
alt-svc: h3=":443"; ma=86400

{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.

**Content-Type:** `application/json; charset=utf-8` means the response body is JSON data encoded using UTF-8.


## Request 4 — GET `/comments/1`

### Request

```sh
curl.exe -i https://jsonplaceholder.typicode.com/comments/1
```

### Response

```text
HTTP/1.1 200 OK
Date: Sun, 16 Aug 2026 15:27:35 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 268
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"10c-KJ4I9RM/+33TKdV8CFsIvqsDSP0"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=nYPoC1gKsN%2FWHl3MMiIpAyInG0MEmJ5oMG0PaRWh8QE%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786889562"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=nYPoC1gKsN%2FWHl3MMiIpAyInG0MEmJ5oMG0PaRWh8QE%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786889562"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786889565
Age: 4492
Accept-Ranges: bytes
cf-cache-status: HIT
CF-RAY: a2c176c45efd066f-BOM
alt-svc: h3=":443"; ma=86400

{
  "postId": 1,
  "id": 1,
  "name": "id labore ex et quam laborum",
  "email": "Eliseo@gardner.biz",
  "body": "laudantium enim quasi est quidem magnam voluptate ipsam eos\ntempora quo necessitatibus\ndolor quam autem quasi\nreiciendis et nam sapiente accusantium"
}
```

**Status:** `200 OK` means the server successfully processed the request and returned the requested resource.

**Content-Type:** `application/json; charset=utf-8` means the response body is JSON data encoded using UTF-8.

## Request 5 — GET `/users/9999` — Deliberate 404

### Request

```sh
curl.exe -i https://jsonplaceholder.typicode.com/users/9999
```

### Response

```text
HTTP/1.1 404 Not Found
Date: Sun, 16 Aug 2026 15:28:17 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 2
Connection: keep-alive
access-control-allow-credentials: true
Cache-Control: max-age=43200
etag: W/"2-vyGp6PvFo4RvsFtPoIWeCReyIC8"
expires: -1
nel: {"report_to":"heroku-nel","response_headers":["Via"],"max_age":3600,"success_fraction":0.01,"failure_fraction":0.1}
pragma: no-cache
report-to: {"group":"heroku-nel","endpoints":[{"url":"https://nel.heroku.com/reports?s=Guo8a%2BWQglUA%2FR3OJXttbRAaZ3fpLFgQqwlRFYgag%2Bc%3D\u0026sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d\u0026ts=1786894097"}],"max_age":3600}
reporting-endpoints: heroku-nel="https://nel.heroku.com/reports?s=Guo8a%2BWQglUA%2FR3OJXttbRAaZ3fpLFgQqwlRFYgag%2Bc%3D&sid=e11707d5-02a7-43ef-b45e-2cf4d2036f7d&ts=1786894097"
Server: cloudflare
vary: Origin, Accept-Encoding
via: 2.0 heroku-router
x-content-type-options: nosniff
x-powered-by: Express
x-ratelimit-limit: 1000
x-ratelimit-remaining: 999
x-ratelimit-reset: 1786894125
cf-cache-status: MISS
CF-RAY: a2c177c9ccb03a59-BOM
alt-svc: h3=":443"; ma=86400

{}
```
**Status:** `404 Not Found` means the server could not find the requested resource at the specified URL.
**Content-Type:** `application/json; charset=utf-8` means the response is JSON data encoded using UTF-8.
