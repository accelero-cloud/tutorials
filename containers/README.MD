## Running multiple micro-services as standalone docker containers

The following tutorial shows how to package the different APIs into microservice containers.
The task at hand also could be achieved with Docker Compose (or Docker Swarm or Kubernetes), 
however the purpose of this tutorial is to provide a glimpse on the basics.

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
Creat a central folder for the logs from all services (make sure that ):
```bash
mkdir logs
```

### Create and start services

#### Build teh images
```bash
for n in $(ls -d ./containers/*/); do s=${n#./containers/}; docker build -t ${s%/} ${n}; done
```
The command above it is the equivalent of issuing the following command 4 times with different service names, where 
the **inventory** is the name of one service:
```bash
docker build -t inventory ./containers/inventory
```

Build and run the Inventory Service:
```bash
docker run --name inventory -d -v $(pwd)/logs:/logs -p 5001:5000 --net service_net inventory

```

Build and run the Order Service:
```bash
docker run --name orders -d -v $(pwd)/logs:/logs -p 5000:5000 --net service_net orders
```

Build and run the Payments Service:
```bash
docker run --name payments -d -v $(pwd)/logs:/logs -p 5002:5000 --net service_net payments
```

Build and run the Shipping Service:
```bash
docker run --name shipping -d -v $(pwd)/logs:/logs -p 5003:5000 --net service_net shipping
```

### Check the status

```bash
docker ps
```
The expected output is:
```bash
ONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                              NAMES
022bd90ce981        shipping            "python service.py"      35 seconds ago       Up 35 seconds       5003/tcp, 0.0.0.0:5003->5000/tcp   shipping
e77e06aca71f        payments            "python service.py"      41 seconds ago       Up 40 seconds       5002/tcp, 0.0.0.0:5002->5000/tcp   payments
194897a60688        orders              "python service.py"      47 seconds ago       Up 46 seconds       0.0.0.0:5000->5000/tcp             orders
60d4c511b383        inventory           "python service.py"      About a minute ago   Up About a minute   5001/tcp, 0.0.0.0:5001->5000/tcp   inventory
6c897f1c41d0        mongo               "docker-entrypoint.s…"   3 hours ago          Up 3 hours          0.0.0.0:27017->27017/tcp           mongo
```

You also should be able to see the log files for each service:
```bash
ls -a ./logs

.             ..            inventory.log orders.log    payments.log  shipping.log
```

You can tail it in one terminal window right away:
```bash
tail -fn 300 ./logs/orders.log

2018-09-16 13:45:46,690 - INFO - flask.app:360 - Logger initialised
2018-09-16 13:45:46,698 - INFO - flask.app:249 - ===== Starting Order Service =====
2018-09-16 13:45:46,699 - DEBUG - flask.app:250 - --> registered routes:
 Map([<Rule '/orders/aggregate/' (HEAD, GET, OPTIONS) -> orders_aggregate_get>,
 <Rule '/orders/schema' (HEAD, GET, OPTIONS) -> orders_schema_get>,
 <Rule '/orders/meta' (HEAD, GET, OPTIONS) -> orders_meta_get>,
 <Rule '/orders/' (HEAD, GET, OPTIONS) -> orders_find_by_query_get>,
 <Rule '/orders/' (PUT, OPTIONS) -> orders_replace_object_put>,
 <Rule '/orders/' (POST, OPTIONS) -> orders_save_object_post>,
 <Rule '/orders/<object_id>' (DELETE, OPTIONS) -> orders_delete_by_id_delete>,
 <Rule '/orders/<object_id>' (HEAD, GET, OPTIONS) -> orders_find_by_id_get>,
 <Rule '/orders/<object_id>' (PATCH, OPTIONS) -> orders_save_object_patch>,
 <Rule '/static/<filename>' (HEAD, GET, OPTIONS) -> static>])
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