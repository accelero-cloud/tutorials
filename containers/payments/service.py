from appkernel import AppKernelEngine

from checkout import PaymentService

app_id = f"{PaymentService.__name__}"
kernel = AppKernelEngine(app_id)

if __name__ == '__main__':
    kernel.register(PaymentService())
    kernel.run()
