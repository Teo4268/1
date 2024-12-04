import asyncio
import websockets
import json

async def handle_mining_client(websocket, path):
    try:
        # Nhận thông điệp từ client, trong đó có địa chỉ pool (host và cổng)
        initial_message = await websocket.recv()
        print(f"Received initial message from client: {initial_message}")
        
        # Giả sử thông điệp client chứa thông tin pool dưới dạng JSON: {"host": "mining-pool.example.com", "port": 3333}
        pool_info = parse_pool_info(initial_message)
        
        if pool_info is None:
            raise Exception("Unable to extract pool information from client message")
        
        pool_host = pool_info['host']
        pool_port = pool_info['port']
        
        # Kết nối đến mining pool
        async with websockets.connect(f"ws://{pool_host}:{pool_port}") as pool_websocket:
            print(f"Connected to pool at {pool_host}:{pool_port}")
            
            # Chuyển tiếp dữ liệu từ client tới pool
            async def forward_client_to_pool():
                try:
                    while True:
                        # Nhận tất cả thông điệp từ client (bao gồm mining submit, hash, nonce, v.v...)
                        message = await websocket.recv()  
                        print(f"Forwarding message from client to pool: {message}")
                        
                        # Gửi tới mining pool
                        await pool_websocket.send(message)
                except websockets.ConnectionClosed:
                    print("Client disconnected")

            # Chuyển tiếp dữ liệu từ pool tới client (bao gồm kết quả từ pool)
            async def forward_pool_to_client():
                try:
                    while True:
                        # Nhận tất cả thông điệp từ pool (bao gồm kết quả đào coin, trạng thái share, v.v...)
                        message = await pool_websocket.recv()  
                        print(f"Forwarding message from pool to client: {message}")
                        
                        # Gửi kết quả từ pool tới client
                        await websocket.send(message)
                except websockets.ConnectionClosed:
                    print("Mining pool disconnected")

            # Chạy cả hai luồng đồng thời
            await asyncio.gather(forward_client_to_pool(), forward_pool_to_client())
    
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()

# Hàm phân tích thông điệp của client để lấy thông tin pool (host và port)
def parse_pool_info(message):
    try:
        # Phân tích thông điệp JSON
        data = json.loads(message)
        if 'host' in data and 'port' in data:
            return {'host': data['host'], 'port': data['port']}
        else:
            return None
    except json.JSONDecodeError:
        return None

async def main():
    # Chạy proxy server trên localhost:3333
    server = await websockets.serve(handle_mining_client, "localhost", 3333)
    print("Mining proxy server is running at ws://localhost:3333")
    await server.wait_closed()

# Chạy server proxy
asyncio.run(main())
