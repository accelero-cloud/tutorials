#!/usr/bin/env python3

from appkernel import AppKernelEngine
from flask import Flask

from checkout import InventoryService
from checkout import Order
from checkout import PaymentService
from checkout import ShippingService

if __name__ == '__main__':
    # starts all 4 services to make the running of this tutorial simpler
    app_id = "{} Service".format(Order.__name__)
    kernel = AppKernelEngine(app_id, app=Flask(app_id), development=True, enable_defaults=True)
    kernel.register(Order, methods=['GET', 'POST', 'DELETE'])

    # o = Order(products=[Product(code='BTX', name='t-shirt', size=ProductSize.M, price=Money(10, 'EUR'))])
    # o.delivery_address = Address(first_name='John', last_name='Doe', city='Big City', street='some address 8',
    #                              country='Country', postal_code='1234')
    # o.payment_method = Payment(method=PaymentMethod.PAYPAL, customer_id='1234567', customer_secret='120')
    # print(o.dumps(pretty_print=True))
    inventory_service = InventoryService(kernel)
    kernel.register(PaymentService())
    kernel.register(ShippingService())
    kernel.run()
