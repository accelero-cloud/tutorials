from datetime import datetime

from appkernel import MongoRepository, Model, Property, create_uuid_generator, date_now_generator, NotEmpty
from appkernel.configuration import config
from money import Money

from checkout.core.models import Product, PaymentMethod, Address, Payment
from checkout.core.util import get_client_proxy
from checkout.inventory.inventory_service import Reservation
from checkout.shipping.shipping_service import Shipping


class AuthorisationRequest(Model):
    payment_method = Property(PaymentMethod, required=True)
    amount = Property(Money, required=True)
    external_reference = Property(str, required=True, validators=NotEmpty)


class Order(Model, MongoRepository):
    id = Property(str, generator=create_uuid_generator('O'))
    payment_method = Property(Payment, required=True)
    products = Property(list, sub_type=Product, required=True)
    order_date = Property(datetime, required=True, generator=date_now_generator)
    delivery_address = Property(Address, required=True)
    inventory_client = get_client_proxy('inventory')
    payment_client = get_client_proxy('payments')
    shipping_client = get_client_proxy('shipping')

    @classmethod
    def before_post(cls, *args, **kwargs):
        order: Order = kwargs.get('model')
        order.finalise_and_validate()
        status_code, rsp_dict = Order.inventory_client.reservations.post(Reservation(order_id=order.id, products=order.products))
        order.update(reservation_id=rsp_dict.get('result'))

    @classmethod
    def after_post(cls, *args, **kwargs):
        order: Order = kwargs.get('model')
        amount = sum([p.price.amount for p in order.products])
        auth_req = AuthorisationRequest(payment_method=order.payment_method, amount=amount)
        auth_req.external_reference = order.id
        status_code, rsp_dict = Order.payment_client.wrap('/payments/authorize').post(auth_req)
        print(f'<authorisation response> {rsp_dict}')
        if status_code not in [200, 201]:
            code, canceled_reservation = Order.inventory_client.wrap(f'/reservations/{order.reservation_id}/cancel').patch()
            if code not in [200, 201]:
                config.app_engine.logger.warn('reservation was not successful.')
            raise Exception('It is not aurhorised')
        else:
            code, result = Order.shipping_client.shippings.post(
                Shipping(reservation_id=order.reservation_id, delivery_address=order.delivery_address))
            print(f':: {result.tracking_id}')
