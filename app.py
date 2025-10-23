from flask import Flask, request
from escpos.printer import Usb
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(
    filename="/home/cc/rasp/printer.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


@app.route("/", methods=["GET"])
def print_codigo():
    codigo = request.args.get("codigo", "test2api")
    ref = request.args.get("ref", "")
    pedido = request.args.get("pedido", "")
    operario = request.args.get("oper", "")
    mez = request.args.get("mez", "")

    mensaje = (
        "Codigo: "
        + codigo
        + "\nReferencia: "
        + ref
        + "\nMezcla: "
        + mez
        + "\nOperador: "
        + operario
        + "\nPedido: "
        + pedido
    )

    logging.info(f"Print request received:\n{codigo}")

    p = None
    try:
        p = Usb(0x04B8, 0x0E15)
        p.set(double_height=True, double_width=True)
        p.text(mensaje)
        p.qr(codigo, size=13)
        p.cut()
        p.close()
        logging.info("Print job completed successfully.")
    except Exception as exc:
        logging.error(f"Error during printing: {exc}")
        try:
            if p:
                p.cut()
                p.close()
        except Exception as e:
            logging.error(f"Error closing printer: {e}")

    return ({}, 200, {"Content-Type": "application/json"})
