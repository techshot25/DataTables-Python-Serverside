import sys

from flask import Flask, render_template, request, jsonify
import numpy as np

sys.path.append('..')

from datatables import DataTable, get_params

fake_data = {"a": np.random.rand(100_000), "b": np.random.rand(100_000)}
dt = DataTable(fake_data)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route('/api', methods=['GET', 'POST'])
def api():
    params = get_params(request=request)
    result = dt(params)
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5050, debug=True)


