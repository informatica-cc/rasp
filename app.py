import os
from flask import Flask, request
import random
import string
from printlog import Log
import subprocess
import json

current_dir = os.path.dirname(os.path.abspath(__file__))

os.path.dirname(os.path.abspath(__file__))


def generateUID():
    return "".join(
        random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10
        )
    )


app = Flask(__name__)
logging = Log()


logging.log(f"--- App started ---")


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

    uid = generateUID()

    logging.log(f"Print request received: {codigo} | UID: {uid}")

    payload = json.dumps({"codigo": codigo, "mensaje": mensaje, "uid": uid})

    try:
        subprocess.Popen(
            [
                os.path.join(current_dir, "venv/bin/python"),
                os.path.join(current_dir, "print.py"),
                payload,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp,
        )
        logging.log(f"Spawned detached print.py for {uid}")
    except Exception as e:
        logging.log(f"Failed to spawn detached print_worker.py: {e}")

    return ({}, 200, {"Content-Type": "application/json"})
