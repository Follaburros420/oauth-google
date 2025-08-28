import base64
import datetime
import logging
import os
import sys
import time

import pyotp
import requests

# ==============================
# CONFIGURACION
# ==============================
SECRET = os.getenv("TOTP_SECRET", "").strip()
WEBHOOKS = os.getenv("WEBHOOKS", "").split(",")
TIME_WINDOW_MINUTES = int(os.getenv("TIME_WINDOW_MINUTES", "5"))
SLEEP_BETWEEN_BLOCKS = int(os.getenv("SLEEP_BETWEEN_BLOCKS", "2"))


# ==============================
# VALIDACION DE CONFIGURACION
# ==============================
def validar_config():
    if not SECRET:
        logging.error("Config error: falta TOTP_SECRET")
        sys.exit(1)
    try:
        base64.b32decode(SECRET, casefold=True)
    except Exception:
        logging.error("Config error: TOTP_SECRET no es Base32 valido")
        sys.exit(1)
    if not WEBHOOKS or WEBHOOKS == [""]:
        logging.error("Config error: falta WEBHOOKS")
        sys.exit(1)


# ==============================
# GENERADOR DE CODIGOS
# ==============================
def generar_codigos(secret: str, window_minutes: int = 5):
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
            "codes": [{"time": t, "code": c} for t, c in bloque],
        }
        for url in WEBHOOKS:
            try:
                r = requests.post(url.strip(), json=payload, timeout=10)
                logging.info("Enviado a %s -> %s", url.strip(), r.status_code)
            except Exception as e:
                logging.warning("Error enviando a %s: %s", url.strip(), e)
        time.sleep(SLEEP_BETWEEN_BLOCKS)


# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    # Configurar logging a stdout
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    validar_config()
    logging.info("Servicio TOTP iniciado")

    while True:
        try:
            codigos = generar_codigos(SECRET, TIME_WINDOW_MINUTES)
            logging.info(
                "Generados %d codigos a las %s",
                len(codigos),
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            notificar_webhooks(codigos)
        except Exception:
            logging.exception("Fallo en ciclo principal")
            time.sleep(5)
        time.sleep(TIME_WINDOW_MINUTES * 60)

