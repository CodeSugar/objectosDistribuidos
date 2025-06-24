import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc
import os
import random
import time

class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
    def __init__(self, server_id, server_name, port):
        self.server_id = server_id
        self.server_name = server_name
        self.port = port

    def Add(self, request, context):
        result = request.a + request.b
        time.sleep(random.uniform(0.1, 0.5))  # Simulate processing time
        print(f"[{self.server_id}] Add: {request.a} + {request.b} = {result}")
        return calculator_pb2.NumberResponse(result=result, server_id=self.server_id)

    def Multiply(self, request, context):
        result = request.a * request.b
        time.sleep(random.uniform(0.1, 0.5))  # Simulate processing time
        print(f"[{self.server_id}] Multiply: {request.a} * {request.b} = {result}")
        return calculator_pb2.NumberResponse(result=result, server_id=self.server_id)

    def GetServerInfo(self, request, context):
        print(f"[{self.server_id}] GetServerInfo requested")
        return calculator_pb2.ServerInfo(
            server_id=self.server_id,
            server_name=self.server_name,
            port=self.port
        )

def serve():
    server_id = os.getenv('SERVER_ID', 'server-1')
    server_name = os.getenv('SERVER_NAME', 'Calculator Server 1')
    port = int(os.getenv('PORT', '50051'))
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorService(server_id, server_name, port), server
    )
    
    listen_addr = f'0.0.0.0:{port}'
    server.add_insecure_port(listen_addr)
    
    print(f"Starting {server_name} ({server_id}) on {listen_addr}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()