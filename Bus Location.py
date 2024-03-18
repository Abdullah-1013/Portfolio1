
import http.server
import json
from urllib.parse import urlparse, parse_qs
import requests
import time
import threading

bus_locations = {}
server_thread = None

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        response = self.update_location(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)
        bus_id = query.get('bus_id', [''])[0]
        
        response = self.get_location(bus_id)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def update_location(self, data):
        bus_id = data.get('bus_id')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        bus_locations[bus_id] = {'latitude': latitude, 'longitude': longitude}
        return {'status': 'success'}

    def get_location(self, bus_id):
        location = bus_locations.get(bus_id)
        if location:
            return location
        else:
            return {'error': 'Bus not found'}

def monitor_bus_location(bus_ids):
    previous_locations = {bus_id: None for bus_id in bus_ids}

    while True:
        for bus_id in bus_ids:
            location = get_bus_location(bus_id)
            if location:
                previous_location = previous_locations[bus_id]
                if location != previous_location:
                    print(f"Bus {bus_id} location changed: {location}")
                    previous_locations[bus_id] = location
                else:
                    print(f"Bus {bus_id} location unchanged")
            else:
                print(f"Error fetching location for bus {bus_id}")
        time.sleep(10)  # Check every 10 seconds

def get_bus_location(bus_id):
    response = requests.get(f'http://localhost:8000/get_location?bus_id={bus_id}')
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def run_server():
    global server_thread
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print("Starting server on port 8000")
    httpd.serve_forever()

if __name__ == '__main__':
    # Simulating bus IDs obtained from a data source
    bus_ids = ['bus_1', 'bus_2', 'bus_3']  # Replace this with your actual bus IDs
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    # Start monitoring bus location changes for all bus IDs
    monitor_thread = threading.Thread(target=monitor_bus_location, args=(bus_ids,))
    monitor_thread.start()
