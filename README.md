## Serverside processing with Python

This builds the backend engine that handles processing of a [JQuery DataTable](https://datatables.net/).

Server side processing is ideal to prevent processing of large data directly on the client side. This implementation does it in python.

---

Example using flask

```python
from flask import Flask

app = Flask(__name__)

@app.route('/api', methods=["GET", "POST"])
def api():
    pass
```

