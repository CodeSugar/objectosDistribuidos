from flask import Flask, request, jsonify
from flask_cors import CORS
import grpc
import calculator_pb2
import calculator_pb2_grpc
import random
import os

app = Flask(__name__)
CORS(app)

# gRPC server endpoints
SERVERS = [
    'grpc-server-1:50051',
    'grpc-server-2:50051', 
    'grpc-server-3:50051'
]

COUNTER_SERVER = 'counter-server:50054'

def get_grpc_client():
    server = random.choice(SERVERS)
    channel = grpc.insecure_channel(server)
    return calculator_pb2_grpc.CalculatorStub(channel), server

def get_counter_client():
    channel = grpc.insecure_channel(COUNTER_SERVER)
    return calculator_pb2_grpc.CounterStub(channel), COUNTER_SERVER

@app.route('/add', methods=['POST'])
def add():
    try:
        data = request.json
        stub, server = get_grpc_client()
        
        request_msg = calculator_pb2.NumberRequest(a=data['a'], b=data['b'])
        response = stub.Add(request_msg)
        
        return jsonify({
            'result': response.result,
            'server_id': response.server_id,
            'grpc_server': server
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/multiply', methods=['POST'])
def multiply():
    try:
        data = request.json
        stub, server = get_grpc_client()
        
        request_msg = calculator_pb2.NumberRequest(a=data['a'], b=data['b'])
        response = stub.Multiply(request_msg)
        
        return jsonify({
            'result': response.result,
            'server_id': response.server_id,
            'grpc_server': server
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/info', methods=['POST'])
def info():
    try:
        stub, server = get_grpc_client()
        
        request_msg = calculator_pb2.Empty()
        response = stub.GetServerInfo(request_msg)
        
        return jsonify({
            'server_id': response.server_id,
            'server_name': response.server_name,
            'port': response.port,
            'grpc_server': server
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/up', methods=['POST'])
def counter_up():
    try:
        stub, server = get_counter_client()
        
        request_msg = calculator_pb2.Empty()
        response = stub.Up(request_msg)
        
        return jsonify({
            'value': response.value,
            'server_id': response.server_id,
            'grpc_server': server
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/down', methods=['POST'])
def counter_down():
    try:
        stub, server = get_counter_client()
        
        request_msg = calculator_pb2.Empty()
        response = stub.Down(request_msg)
        
        return jsonify({
            'value': response.value,
            'server_id': response.server_id,
            'grpc_server': server
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/counter', methods=['POST'])
def get_counter():
    try:
        stub, server = get_counter_client()
        
        request_msg = calculator_pb2.Empty()
        response = stub.GetCounter(request_msg)
        
        return jsonify({
            'value': response.value,
            'server_id': response.server_id,
            'grpc_server': server
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)