from flask import Flask, request
from escpos.printer import Usb
import os
from datetime import datetime
import random
import string


class Log:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_path = os.path.join(self.script_dir, "printer.log")

    def log(self, message: str):
        """Simple homemade logger that appends messages to printer.log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} | {message}\n"
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(line)
        except Exception as e:
            print(f"Logging failed: {e}")


class Printer:
    id_vendor = 0x04B8
    id_product = 0x0E15
    usb_printer = None

    def __init__(self):
        self.usb_printer = None

    def loadUsbPrinter(self):
        try:
            logging.log("Attempting to connect to printer...")
            self.usb_printer = Usb(self.id_vendor, self.id_product)
            self.usb_printer.set(double_height=True, double_width=True)
            logging.log("Connected to printer successfully.")
        except Exception as e:
            logging.log(f"Printer connection failed: {e}")

    def getUsb(self):
        if not self.usb_printer:
            self.loadUsbPrinter()
        return self.usb_printer


def http_response():
    return ({}, 200, {"Content-Type": "application/json"})


def generateUID():
    return "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10
        )
    )


app = Flask(__name__)
logging = Log()
printer = Printer()


logging.log(f"--- App started ---")


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


@app.route("/", methods=["POST", "OPTIONS"])
def print_codigo():
    if request.method == "OPTIONS":
        return http_response()

    data = request.get_json(force=True, silent=True) or {}
    mensaje = data.get("mensaje", "Test")
    codigo = data.get("codigo", "Test")

    uid = generateUID()

    logging.log(f"Print request received: {codigo} | UID: {uid}")

    p = printer.getUsb()

    if not p:
        logging.log("Error: Printer not connected.")
        return http_response()

    try:
        p.text(f"{uid}\n")
        p.qr(codigo, size=11)
        p._raw(b"\n")
        p.text(mensaje)
        p._raw(b"\n")
        p.cut()
    except Exception as exc:
        logging.log(f"Error during printing: {str(exc)}")

    return http_response()
