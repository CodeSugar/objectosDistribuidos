from flask import Flask, request, jsonify
from flask_cors import CORS
import grpc
import simple_counter_pb2
import simple_counter_pb2_grpc
import os

app = Flask(__name__)
CORS(app)

COUNTER_SERVER = 'simple-counter:50055'

def get_counter_client():
    channel = grpc.insecure_channel(COUNTER_SERVER)
    return simple_counter_pb2_grpc.SimpleCounterStub(channel), COUNTER_SERVER

@app.route('/up', methods=['POST'])
def counter_up():
    try:
        stub, server = get_counter_client()
        
        request_msg = simple_counter_pb2.Empty()
        response = stub.Up(request_msg)
        
        return jsonify({
            'value': response.value,
            'server_id': response.server_id,
            'grpc_server': server
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'simple-gateway'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8090))
    print(f"Starting Simple Gateway on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)