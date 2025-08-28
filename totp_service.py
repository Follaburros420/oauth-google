import pyotp
import datetime
import base64
import requests
import time
import os
import sys

# ==============================
# CONFIGURACIÓN
# ==============================
SECRET = os.getenv("TOTP_SECRET", "").strip()
WEBHOOKS = os.getenv("WEBHOOKS", "").split(",")
TIME_WINDOW_MINUTES = int(os.getenv("TIME_WINDOW_MINUTES", "5"))
SLEEP_BETWEEN_BLOCKS = int(os.getenv("SLEEP_BETWEEN_BLOCKS", "2"))

# ==============================
# VALIDACIÓN DE CONFIGURACIÓN
# ==============================
def validar_config():
    if not SECRET:
        print("❌ Error: No se definió la variable de entorno TOTP_SECRET")
        sys.exit(1)
    try:
        base64.b32decode(SECRET, casefold=True)
    except Exception:
        print("❌ Error: La clave no es válida en formato Base32.")
        sys.exit(1)
    if not WEBHOOKS or WEBHOOKS == [""]:
        print("❌ Error: No se definieron URLs en la variable de entorno WEBHOOKS")
        sys.exit(1)

# ==============================
# GENERADOR DE CÓDIGOS
# ==============================
def generar_codigos(secret, window_minutes=5):
    totp = pyotp.TOTP(secret)
    ahora = datetime.datetime.now()
    timestamp_actual = int(ahora.timestamp())

    codigos = []
    pasos = window_minutes * 60 // 30

    for i in range(-pasos, pasos + 1):
        ts = timestamp_actual + (i * 30)
        codigo = totp.at(ts)
        tiempo = datetime.datetime.fromtimestamp(ts)
        codigos.append((tiempo.strftime("%Y-%m-%d %H:%M:%S"), codigo))

    return codigos

# ==============================
# NOTIFICADOR DE WEBHOOKS
# ==============================
def notificar_webhooks(codigos):
    for i in range(0, len(codigos), 5):
        bloque = codigos[i:i+5]
        payload = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "codes": [{"time": t, "code": c} for t, c in bloque]
        }
        for url in WEBHOOKS:
            try:
                r = requests.post(url.strip(), json=payload, timeout=10)
                print(f"Enviado a {url.strip()} -> {r.status_code}")
            except Exception as e:
                print(f"Error enviando a {url.strip()}: {e}")
        time.sleep(SLEEP_BETWEEN_BLOCKS)

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    validar_config()
    print("✅ Servicio TOTP iniciado...")

    while True:
        codigos = generar_codigos(SECRET, TIME_WINDOW_MINUTES)
        print(f"Generados {len(codigos)} códigos a las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        notificar_webhooks(codigos)
        time.sleep(TIME_WINDOW_MINUTES * 60)
