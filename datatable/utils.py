import json

def get_params(request):
    raw_data = request.get_data()
    return json.loads(raw_data)
