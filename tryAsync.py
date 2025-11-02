from epsonPrinter import Printer
import time

printer = Printer()
printer.print("TEST", "ASYNC TEST")

time.sleep(3)
