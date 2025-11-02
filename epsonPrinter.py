from escpos.printer import Usb
from customLog import Log
import random
import string
import threading


class Printer:
    def __init__(self):
        self.id_vendor = 0x04B8
        self.id_product = 0x0E15
        self.logging = Log()

    def print(self, codigo="TEST", mensaje="TEST"):
        thread = threading.Thread(
            target=self._print_job, args=(codigo, mensaje), daemon=True
        )
        thread.start()

    def _print_job(self, codigo, mensaje):
        try:
            uid = self._generateUID()
            self.logging.log(f"Print request received {codigo} {uid}")
            p = Usb(self.id_vendor, self.id_product, timeout=4000)
            p.set(double_height=True, double_width=True)
            p.text(f"{uid}\n")
            p.qr(codigo, size=11)
            p.text(f"\n{mensaje}\n")
            p.cut()
            p.close()
            self.logging.log("Printed successfully")
        except Exception as exc:
            self.logging.log(f"Error during printing: {str(exc)}")

    def _generateUID(self):
        return "".join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10
            )
        )
