import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc
import os
import threading

class CounterService(calculator_pb2_grpc.CounterServicer):
    def __init__(self, server_id, server_name, port, data_file):
        self.server_id = server_id
        self.server_name = server_name
        self.port = port
        self.data_file = data_file
        self.lock = threading.Lock()
        self._ensure_data_file()

    def _ensure_data_file(self):
        """Ensure the counter file exists and initialize if needed"""
        try:
            with open(self.data_file, 'r') as f:
                self._current_value = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self._current_value = 0
            self._save_counter()
        print(f"[{self.server_id}] Counter initialized with value: {self._current_value}")

    def _save_counter(self):
        """Save counter value to file"""
        with open(self.data_file, 'w') as f:
            f.write(str(self._current_value))

    def Up(self, request, context):
        with self.lock:
            self._current_value += 1
            self._save_counter()
            print(f"[{self.server_id}] Counter UP: {self._current_value}")
            return calculator_pb2.CounterResponse(
                value=self._current_value,
                server_id=self.server_id
            )

    def Down(self, request, context):
        with self.lock:
            self._current_value -= 1
            self._save_counter()
            print(f"[{self.server_id}] Counter DOWN: {self._current_value}")
            return calculator_pb2.CounterResponse(
                value=self._current_value,
                server_id=self.server_id
            )

    def GetCounter(self, request, context):
        with self.lock:
            print(f"[{self.server_id}] Counter GET: {self._current_value}")
            return calculator_pb2.CounterResponse(
                value=self._current_value,
                server_id=self.server_id
            )

def serve():
    server_id = os.getenv('SERVER_ID', 'counter-server')
    server_name = os.getenv('SERVER_NAME', 'Counter Server')
    port = int(os.getenv('PORT', '50054'))
    data_dir = os.getenv('DATA_DIR', '/data')
    data_file = os.path.join(data_dir, 'counter.txt')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CounterServicer_to_server(
        CounterService(server_id, server_name, port, data_file), server
    )
    
    listen_addr = f'0.0.0.0:{port}'
    server.add_insecure_port(listen_addr)
    
    print(f"Starting {server_name} ({server_id}) on {listen_addr}")
    print(f"Data file: {data_file}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()