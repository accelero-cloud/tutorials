```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -U appkernel
pip install money
```

Try out wth curl:
```bash
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
orderservice \
 'http://127.0.0.1:5000/orders/'
```