# Testing in GitHub Codespaces

## Quick Start

1. **Start the services**:
   ```bash
   docker-compose up --build
   ```

2. **Wait for all services to start** (you'll see logs from all containers)

3. **Access the web client**:
   - Codespaces will automatically forward port 8080
   - Click the "Open in Browser" popup or go to the Ports tab
   - The client will auto-detect Codespaces and use HTTPS URLs

## How Port Forwarding Works in Codespaces

- **Port 8080**: Web client (automatically forwarded)
- **Ports 8081-8083**: Gateway services (forwarded on demand)
- **Internal gRPC servers**: Not exposed (internal Docker network)

## Testing Steps

1. **Open the web interface** at the forwarded 8080 port
2. **Try the operations**:
   - Enter numbers (e.g., 5 and 3)
   - Click "Add" or "Multiply"
   - Click "Get Server Info"
3. **Watch the visualization**:
   - Servers light up when processing requests
   - Logs show request/response flow
   - Load balancing rotates between servers

## Troubleshooting

**If you see connection errors:**
1. Check all containers are running: `docker-compose ps`
2. Make sure ports 8081-8083 are forwarded in the Ports tab
3. The client will automatically detect Codespaces and use HTTPS

**To see server logs:**
```bash
docker-compose logs gateway-1
docker-compose logs grpc-server-1
```

**To restart services:**
```bash
docker-compose down
docker-compose up --build
```

## Architecture in Codespaces

```
Browser (port 8080) 
    ↓ HTTPS
Gateway 1-3 (ports 8081-8083)
    ↓ gRPC (internal)
gRPC Servers 1-3 (internal network)
```

The client automatically detects Codespaces environment and switches to HTTPS URLs with proper port forwarding.