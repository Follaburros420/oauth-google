# Imagen base de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements si existiera
# RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias necesarias
RUN pip install pyotp requests

# Copiar el código de la aplicación
COPY totp_service.py .

# Comando por defecto
CMD ["python", "totp_service.py"]
