# Imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Evitar buffering de stdout/stderr para ver logs en Docker
ENV PYTHONUNBUFFERED=1

# Instalar dependencias necesarias
RUN pip install --no-cache-dir pyotp requests

# Copiar el codigo de la aplicacion
COPY totp_service.py .

# Comando por defecto
CMD ["python", "totp_service.py"]
