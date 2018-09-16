from appkernel import AppKernelEngine

from checkout import InventoryService

app_id = f"{InventoryService.__name__}"
kernel = AppKernelEngine(app_id)

if __name__ == '__main__':
    inventory_service = InventoryService(kernel)
    kernel.run()
