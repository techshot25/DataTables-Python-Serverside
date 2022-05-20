import sys
import json

from flask import Flask, render_template, request, jsonify
import numpy as np

sys.path.append("../datatables")

from datatables import DataTable

fake_data = {"a": np.random.rand(100_000), "b": np.random.rand(100_000)}
dt = DataTable(fake_data)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/api', methods=['GET', 'POST'])
def api():
    config_data = request.get_data()
    config_data_dict = json.loads(config_data)
    print(config_data_dict)
    resp = dt(config_data_dict)

    return jsonify(resp)

if __name__ == "__main__":
    app.run(port=5050, debug=True)


