# Web Store Cart
This microservice specializes in handling a Cart where user puts his or her products in order to finally buy them.
Architecture used in this project is called an **Onion (Layered)** and is meant to be used in a medium to big-sized
projects. You can treat this as a more scalable version of **Ports And Adapters**. FastAPI framework is used to handle
requests.

## Hosts
| Hostname            | Development    | Compose/Swarm               |
|---------------------|----------------|-----------------------------|
| **web_store_cart**      | 127.0.0.1:8002 | mr.localhost/web_store_cart/* |
| **web_store_cart_worker** | manually       | -                           |
| **web_store_cart_db**     | localhost:5435 | web_store_cart_db:5432        |