from appkernel import AppKernelEngine

from checkout import ShippingService

app_id = f"{ShippingService.__name__}"
kernel = AppKernelEngine(app_id)

if __name__ == '__main__':
    kernel.register(ShippingService())
    kernel.run()
