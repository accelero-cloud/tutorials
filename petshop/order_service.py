from datetime import datetime

from appkernel import MongoRepository, Model, Property, create_uuid_generator, date_now_generator, Service

from petshop.models import Product


class Order(Model, MongoRepository, Service):
    id = Property(str, generator=create_uuid_generator('O'))
    products = Property(list, sub_type=Product, required=True)
    order_date = Property(datetime, required=True, generator=date_now_generator())

    def save(self):
        super(MongoRepository, self).save()


