# Simple Distributed Counter Example

A minimal educational example demonstrating the core concepts of distributed objects with gRPC.

## 🎯 Learning Objectives

This simple example focuses on the fundamental concepts:

- **Distributed Object**: A counter service running in a separate container
- **Remote Procedure Call**: HTTP client calling gRPC server through a gateway
- **Data Persistence**: Counter value persists across container restarts
- **Service Communication**: Client → Gateway → gRPC Server

## 🏗️ Architecture

```
┌─────────────┐
│   Browser   │ (HTTP Client)
└─────┬───────┘
      │ HTTP/HTTPS
      ▼
┌─────────────┐
│   Gateway   │ (Protocol Translation)
│   :8090     │
└─────┬───────┘
      │ gRPC
      ▼
┌─────────────┐
│Counter Srv  │ (Persistent Storage)
│   :50055    │
└─────────────┘
```

## 🚀 Quick Start

### **Run the Example**
```bash
cd simple-example
docker-compose up --build
```

### **Access the Client**
- **Local**: http://localhost:8080
- **Codespaces**: Port 8080 will be auto-forwarded

### **Test the System**
1. Click "Counter Up ⬆️" button
2. Watch the counter increment
3. Check the logs for request/response flow
4. Restart containers to verify persistence: `docker-compose restart`

## 📂 Files

```
simple-example/
├── simple-counter.proto      # gRPC service definition
├── counter_server.py         # Counter service implementation
├── gateway.py               # HTTP-to-gRPC gateway
├── client/index.html        # Simple web interface
├── docker-compose.yml       # Container orchestration
├── Dockerfile.counter       # Counter server image
└── Dockerfile.gateway       # Gateway image
```

## 🎓 What You'll Learn

### **1. Distributed Objects**
- The counter is an object that runs in a different process/container
- Client doesn't know where the counter physically exists
- Transparent remote access through the gateway

### **2. Protocol Translation**
- Gateway converts HTTP requests to gRPC calls
- Enables web clients to communicate with gRPC services
- Demonstrates how different protocols can interoperate

### **3. Data Persistence**
- Counter value is saved to a file
- Data survives container restarts
- Shows how distributed services maintain state

### **4. Service Boundaries**
- Clear separation between client, gateway, and server
- Each component has a single responsibility
- Easy to understand request flow

## 🔍 Key Differences from Full Example

| Feature | Simple Example | Full Example |
|---------|---------------|--------------|
| Operations | Only "Up" | Add, Multiply, Up, Down, Get |
| Servers | 1 Counter Server | 3 Calculator + 1 Counter |
| Gateways | 1 Gateway | 3 Load-Balanced Gateways |
| Visualization | None | Real-time system diagram |
| Complexity | Minimal | Full distributed system |

This simple example is perfect for:
- **First-time learners** understanding distributed concepts
- **Quick demonstrations** of gRPC and Docker
- **Building blocks** before tackling the full system
- **Educational settings** with limited time

## 🔧 Technical Details

- **gRPC Service**: `SimpleCounter` with single `Up()` method
- **Persistence**: Text file in Docker volume
- **Gateway Port**: 8090
- **Counter Port**: 50055 (internal)
- **Client Port**: 8080