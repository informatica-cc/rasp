from flask import Flask, request
from escpos.printer import Usb
import os
from datetime import datetime
import random
import string

app = Flask(__name__)

id_vendor = 0x04B8
id_product = 0x0E15

# --- Homemade logging setup ---
script_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(script_dir, "printer.log")


def log(message: str):
    """Simple homemade logger that appends messages to printer.log."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {message}\n"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print(f"Logging failed: {e}")


def generateUID():
    return "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10
        )
    )


p = None
try:
    log("Attempting to connect to printer...")
    p = Usb(id_vendor, id_product)
    p.set(double_height=True, double_width=True)
    log("Connected to printer successfully.")
except Exception as e:
    log(f"Printer connection failed: {e}")


log(f"--- App started ---")


@app.route("/", methods=["POST"])
def print_codigo():
    data = request.get_json(force=True, silent=True) or {}
    mensaje = data.get("mensaje", "Test")
    codigo = data.get("codigo", "Test")

    uid = generateUID()

    log(f"Print request received: {codigo} | UID: {uid}")

    if p is None:
        log("Printer not connected.")
        return ({}, 200, {"Content-Type": "application/json"})

    try:
        p.text(f"UID: {uid}\n")
        p.qr(codigo, size=11)
        p.text(mensaje)
        p._raw(b"\n")
        p.cut()
    except Exception as exc:
        log(f"Error during printing: {str(exc)}")

    return ({}, 200, {"Content-Type": "application/json"})
