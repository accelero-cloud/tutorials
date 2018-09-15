import datetime

from appkernel import AppKernelEngine
from flask import Flask

from checkout import Order

if __name__ == '__main__':
    app_id = f"{Order.__name__} Service"
    kernel = AppKernelEngine(app_id)
    kernel.register(Order, methods=['GET', 'POST', 'DELETE'])
    kernel.run()
