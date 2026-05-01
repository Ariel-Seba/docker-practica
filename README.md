# Docker Practica — DiploDevOps

Stack Docker completo construido como práctica de Docker y Docker Compose.

## Arquitectura

```
Internet
   │
   ▼
Traefik :80  (reverse proxy + autodescubrimiento)
   ├── /          →  Nginx (frontend HTML)
   ├── /api       →  FastAPI (backend)
   └── /whoami    →  whoami (servicio de prueba)
         │
         ▼
     PostgreSQL (red interna, con volumen persistente)
```

## Servicios

| Servicio | Imagen | Descripción |
|---|---|---|
| `traefik` | traefik:v2.11 | Reverse proxy con autodescubrimiento via labels |
| `web` | nginx:alpine | Sirve el frontend estático |
| `backend` | python:3.12-slim | API REST con FastAPI |
| `db` | postgres:16.3-alpine3.20 | Base de datos con volumen persistente |
| `whoami` | traefik/whoami | Servicio de prueba |
| `atlas` | keinstien/atlas | Visualización gráfica de la red Docker |

## Endpoints

| URL | Descripción |
|---|---|
| http://localhost | Frontend — agenda de contactos |
| http://localhost/api/contactos | API REST |
| http://localhost/whoami | Info del request |
| http://localhost:8090 | Dashboard de Traefik |
| http://localhost:5001 | Atlas — visualización de red |

## Requisitos

- Docker
- Docker Compose

## Configuración

Crear un archivo `.env` en la raíz del proyecto:

```env
POSTGRES_DB=agenda
POSTGRES_USER=<usuario>
POSTGRES_PASSWORD=<password>
```

> El `.env` está en `.gitignore` y nunca se sube al repositorio.

## Levantar el stack

```bash
docker compose up --build -d
```

## Detener

```bash
docker compose down
```

Para eliminar también los datos persistentes:

```bash
docker compose down -v
```

## CI/CD

GitHub Actions ejecuta un escaneo de seguridad con **Checkov** en cada push a `main`, analizando los `Dockerfile` y `docker-compose.yml` en busca de malas prácticas de seguridad.
