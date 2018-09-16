from appkernel import AppKernelEngine

from checkout import Order

app_id = f"{Order.__name__} Service"
kernel = AppKernelEngine(app_id)

if __name__ == '__main__':
    kernel.register(Order, methods=['GET', 'POST', 'DELETE'])
    kernel.run()
