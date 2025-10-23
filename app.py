from flask import Flask, request
from escpos.printer import Usb
import os
from datetime import datetime

app = Flask(__name__)

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


log(f"--- App started, logging to {log_path} ---")


@app.route("/", methods=["GET"])
def print_codigo():
    codigo = request.args.get("codigo", "test2api")
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

    log(f"Print request received:\n{codigo}")

    p = None
    try:
        p = Usb(0x04B8, 0x0E15)
        p.set(double_height=True, double_width=True)
        p.text(mensaje)
        p.qr(codigo, size=13)
        p.cut()
        p.close()
        log("Print job completed successfully.")
    except Exception as exc:
        log(f"Error during printing: {exc}")
        try:
            if p:
                p.cut()
                p.close()
        except Exception as e:
            log(f"Error closing printer: {e}")

    return ({}, 200, {"Content-Type": "application/json"})
