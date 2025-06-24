import grpc
from concurrent import futures
import simple_counter_pb2
import simple_counter_pb2_grpc
import os
import threading

class SimpleCounterService(simple_counter_pb2_grpc.SimpleCounterServicer):
    def __init__(self, server_id, data_file):
        self.server_id = server_id
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
        print(f"[{self.server_id}] Simple Counter initialized with value: {self._current_value}")

    def _save_counter(self):
        """Save counter value to file"""
        with open(self.data_file, 'w') as f:
            f.write(str(self._current_value))

    def Up(self, request, context):
        with self.lock:
            self._current_value += 1
            self._save_counter()
            print(f"[{self.server_id}] Counter UP: {self._current_value}")
            return simple_counter_pb2.CounterResponse(
                value=self._current_value,
                server_id=self.server_id
            )

def serve():
    server_id = os.getenv('SERVER_ID', 'simple-counter')
    port = int(os.getenv('PORT', '50055'))
    data_dir = os.getenv('DATA_DIR', '/data')
    data_file = os.path.join(data_dir, 'simple-counter.txt')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    simple_counter_pb2_grpc.add_SimpleCounterServicer_to_server(
        SimpleCounterService(server_id, data_file), server
    )
    
    listen_addr = f'0.0.0.0:{port}'
    server.add_insecure_port(listen_addr)
    
    print(f"Starting Simple Counter Server ({server_id}) on {listen_addr}")
    print(f"Data file: {data_file}")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()