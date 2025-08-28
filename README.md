# Google TOTP Generator API

Microservicio para generar códigos TOTP de Google.

## 🚀 Inicio Rápido

```bash
# Docker Compose (Recomendado)
docker-compose up --build

# Docker manual
docker build -t google-totp-generator .
docker run -p 3000:3000 google-totp-generator

# Desarrollo local
npm install && npm start
```

## 📡 API Endpoints

### `GET /totp` - Código TOTP actual
```json
{
  "status": "success",
  "data": {
    "code": "085389",
    "timeRemaining": 25,
    "generatedAt": "2025-08-27T08:00:00.000Z",
    "expiresAt": "2025-08-27T08:00:30.000Z"
  }
}
```

### `GET /health` - Health check
```json
{
  "status": "healthy",
  "timestamp": "2025-08-27T08:00:00.000Z"
}
```

## 📋 Uso

```bash
# Obtener código TOTP
curl http://localhost:3000/totp

# Health check
curl http://localhost:3000/health
```

## 🔧 Variables de Entorno

| Variable | Por Defecto |
|----------|-------------|
| `PORT` | `3000` |
| `GOOGLE_TOTP_SECRET` | `pumx4n26255yb52amsatqytkfjxbcrql` |

## 🐳 Docker

```bash
# Construir y ejecutar
docker-compose up --build -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```
