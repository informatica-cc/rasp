from flask import Flask, request
from escpos.printer import Usb

app = Flask(__name__)

# https://python-escpos.readthedocs.io/en/latest/user/methods.html#escpos-class


@app.route("/", methods=["GET"])
def print():
    codigo = request.args.get("codigo", "")
    ref = request.args.get("ref", "")
    pedido = request.args.get("pedido", "")
    operario = request.args.get("oper", "")
    mez = request.args.get("mez", "")
    if not codigo:
        return error("missing codigo", 400)

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

    p = None
    try:
        p = Usb(0x04B8, 0x0E15)
        p.set(double_height=True, double_width=True)
        p.text(mensaje)
        p.qr(codigo, size=13)
        p.cut()
        p.close()

    except Exception as exc:
        print("Error printing: ")
        print(str(exc))
        try:
            if p:
                p.cut()
                p.close()
        except:
            print("Error closing printer")

    return (
        {},
        200,
        {"Content-Type": "application/json"},
    )


def error(msg, code):
    return ({"err": msg}, code, {"Content-Type": "application/json"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
