# JWT Demo

## Start server
```
$ docker compose up
```

## Endpoint
| Endpoint | Method | Description |
| :--      | :---:  | :---        |
| `/`      | `ANY`  | healthcheck endpoint |
| `/api/v0/secret-key` | `GET` | Server will return keys that used to validate JWT with `{ "key": "<secret-key>" }` |
| `/api/v0/goods/return` | `POST` | Simulate the communication between client and server |
