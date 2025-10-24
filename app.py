from flask import Flask, request
from escpos.printer import Usb
import usb.core
import os
from datetime import datetime

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


def reset_printer():
    dev = usb.core.find(idVendor=id_vendor, idProduct=id_product)
    if dev:
        try:
            dev.reset()
            log("USB printer reset successfully")
        except Exception as e:
            log(f"USB reset failed: {e}")
    else:
        log("Printer device not found for reset")


log(f"--- App started ---")


@app.route("/", methods=["GET"])
def print_codigo():
    codigo = request.args.get("codigo", "testapi")
    ref = request.args.get("ref", "")
    pedido = request.args.get("pedido", "")
    operario = request.args.get("oper", "")
    mez = request.args.get("mez", "")

    mensaje = (
        f"Codigo: {codigo}\n"
        f"Referencia: {ref}\n"
        f"Mezcla: {mez}\n"
        f"Operador: {operario}\n"
        f"Pedido: {pedido}"
    )

    log(f"Print request received: {codigo}")

    p = None
    try:
        p = Usb(id_vendor, id_product)
        p.set(double_height=True, double_width=True)
        p.text(mensaje)
        p.qr(codigo, size=13)
        p.cut()
        p.close()
    except Exception as exc:
        log(f"Error during printing: {exc}")
    finally:
        reset_printer()

    return ({}, 200, {"Content-Type": "application/json"})
