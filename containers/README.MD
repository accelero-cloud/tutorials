## Running multiple micro-services as standalone docker containers

The following tutorial shows how to package the different APIs into microservice containers.

### Prepare pre-requisites

We will use a common, dedicated network for all services:
```bash
docker network create service_net
```

The Mongo database is also encapsulated in a docker container: 
```bash
docker create -v ~/data:/data/db -p 27017:27017 --net service_net --name mongo mongo
docker start mongo
```
Create a base image with the common code used for this tutorial:
```bash
docker build -t tutorial-base .
```


### Create and start services

#### Build teh images
```bash
for n in $(ls -d ./containers/*/); do s=${n#./containers/}; docker build -t ${s%/} ${n}; done
```
The command above it is the equivalent of issuing the following command 4 times with different service names:
```bash
docker build -t inventory ./containers/inventory
```

Build and run the Inventory Service:
```bash
docker run --name inventory -d -p 5001:5000 --net service_net inventory
```

Build and run the Order Service:
```bash
docker run --name orders -d -p 5000:5000 --net service_net orders
```

Build and run the Payments Service:
```bash
docker run --name payments -d -p 5002:5000 --net service_net payments
```

Build and run the Shipping Service:
```bash
docker run --name shipping -d -p 5003:5000 --net service_net shipping
```

### Test the services:
```bash
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
    "_type": "tutorials.order_service.Order",
    "delivery_address": {
        "_type": "tutorials.models.Address",
        "city": "Big City",
        "country": "Country",
        "first_name": "John",
        "last_name": "Doe",
        "postal_code": "1234",
        "street": "some address 8"
    },
    "id": "Oc2e5b438-8d12-4533-b085-c38add1e126d",
    "order_date": "2018-09-04T18:51:18.547186",
    "payment_method": {
        "_type": "tutorials.models.Payment",
        "customer_id": "1234567890123456789012",
        "customer_secret": "120",
        "method": "PAYPAL"
    },
    "products": [
        {
            "_type": "tests.test_util.Product",
            "code": "BTX",
            "name": "t-shirt",
            "price": {
                "_type": "money.money.Money",
                "amount": 10,
                "currency": "EUR"
            },
            "size": "M"
        },
        {
            "_type": "tests.test_util.Product",
            "code": "BTX",
            "name": "t-shirt",
            "price": {
                "_type": "money.money.Money",
                "amount": 12,
                "currency": "EUR"
            },
            "size": "L"
        }
    ]
}
' \
 'http://localhost:5000/orders/'
```

### Cleanup

After having fun with the little setup and you'd like to clean up the place, just follow the steps bellow:
```bash
for n in $(ls -d ./containers/*/); do s=$(echo ${n}|cut -d/ -f3); docker stop ${s}; docker rm ${s}; docker rmi ${s}; done
```
The code from above is the 
```bash
docker stop shipping payments inventory orders
docker rm shipping payments inventory orders
docker rmi shipping payments inventory orders
```