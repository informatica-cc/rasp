from flask import Flask, request
from escpos.printer import Usb
import usb.core
import os
from datetime import datetime
import time

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


try:
    log("Releasing usb device...")
    dev = usb.core.find(idVendor=id_vendor, idProduct=id_product)
    usb.util.dispose_resources(dev)
except Exception as e:
    log(f"Error releasing usb device {e}")


p = None
try:
    log("Attempting to connect to printer...")
    p = Usb(id_vendor, id_product)
    log("Connected to printer successfully.")
except Exception as e:
    log(f"Printer connection failed: {e}")


log(f"--- App started ---")


@app.route("/", methods=["GET"])
def print_codigo():
    codigo = request.args.get("codigo", "testapi")
    ref = request.args.get("ref", "")
    pedido = request.args.get("pedido", "")
    operario = request.args.get("oper", "")
    mez = request.args.get("mez", "")
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M")

    mensaje = (
        f"Codigo: {codigo}\n"
        f"Referencia: {ref}\n"
        f"Mezcla: {mez}\n"
        f"Operador: {operario}\n"
        f"Pedido: {pedido}"
        f"{fecha_hora}\n"
    )

    log(f"Print request received: {codigo}")

    if p is None:
        log("Printer not connected.")
        return ({}, 200, {"Content-Type": "application/json"})

    try:
        p.set(double_height=True, double_width=True)
        p.text(mensaje)
        p.qr(codigo, size=13)
        p.cut()
    except Exception as exc:
        log(f"Error during printing: {exc}")
    finally:
        time.sleep(1.5)

    return ({}, 200, {"Content-Type": "application/json"})
