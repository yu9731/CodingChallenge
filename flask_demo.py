from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/check', methods=['POST'])
def check_status():
    data = request.get_json()

    station_graph = data.get('station_graph', [])
    routes = data.get('routes', [])
    check_route = data.get('check_route', {})

    result = is_route_conflict(station_graph, routes, check_route)
    return jsonify(result)

def is_route_conflict(station_graph, routes, check_route):
    try:
        # Extract the start and end points of the check route
        start = check_route.get('start')
        end = check_route.get('end')

        # Create a list for containing all station names, so that the bi-direction function can be achieved
        station_name = []
        for station in station_graph:
            if station.get('start') not in station_name:
                station_name.append(station.get('start'))
            else:
                pass
        
        # Check if the start and end points in current station and if the check route are occupied
        if (start in station_name) and (end in station_name):
            i = 0
            while i < len(routes):
                if (routes[i].get('start') == start) and (routes[i].get('end') == end):
                    if (routes[i].get('occupied') == "true"):
                        i += 1
                        return {"success": True}
                    else:
                        i += 1
                        return {"success": False}
                else:
                    i += 1
        else:
            return {"success": False}

    except Exception as e:
        # Handle any exceptions, returning {"success": false}
        return {"success": False}

#app.run()
http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()