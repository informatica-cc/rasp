from escpos.printer import Usb
from printlog import Log
import sys, json


id_vendor = 0x04B8
id_product = 0x0E15

logging = Log()

logging.log("Detached spawner here, initializing printer")

try:
    payload = json.loads(sys.argv[1])
    codigo = payload.get("codigo", "TEST")
    mensaje = payload.get("mensaje", "TEST")
    uid = payload.get("uid", "N/A")
    logging.log(f"Preparing to print for {uid}")
    p = Usb(id_vendor, id_product, timeout=5000)
    p.set(double_height=True, double_width=True)
    p.text(f"{uid}\n")
    p.qr(codigo, size=11)
    p.text(f"\n{mensaje}\n")
    p._raw(b"\n")
    p.cut()
    p.close()
    logging.log(f"Printed succesfully")
except Exception as exc:
    logging.log(f"Error during printing: {str(exc)}")
