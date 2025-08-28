FROM python:3.13-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY totp_service.py /app/

# Instalar dependencias necesarias
RUN pip install --no-cache-dir pyotp requests

# Comando por defecto
CMD ["python", "totp_service.py"]
