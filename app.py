from flask import Flask, request
from epsonPrinter import Printer


app = Flask(__name__)

printer = Printer()


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    response.headers.add("Connection", "close")
    return response


@app.route("/", methods=["POST", "OPTIONS"])
def print_codigo():
    if request.method == "OPTIONS":
        return ({}, 200, {"Content-Type": "application/json"})

    data = request.get_json(force=True, silent=True) or {}
    mensaje = data.get("mensaje", "Test")
    codigo = data.get("codigo", "Test")

    printer.print(codigo, mensaje)

    return ({}, 200, {"Content-Type": "application/json"})
