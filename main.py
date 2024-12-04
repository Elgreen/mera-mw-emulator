import asyncio
import socket

async def handle_client(client, timeout_seconds, chunk_size):
    try:
        while True:
            weight = input("Enter weight: ")

            try:
                weight = float(weight)
            except ValueError:
                print("Input error")
                continue

            code = "<No_Code>"  # Emulate the absence of a product code
            sign = "+"
            weight_string = f"{weight:07.3f}"
            stability = " " 

            message = f"{code}{sign}{weight_string} kg {stability}\r\x1E"

            await send_data(client, message, chunk_size)

            await clear_stream_buffer(client)
            # Confirmation waiting
            confirmation_received = await wait_for_confirmation_with_timeout(client, timeout_seconds)
            if confirmation_received:
                print("Confirmation received")
            else:
                print("Error: Confirmation not received")
    except Exception as ex:
        print("Error: ", ex)
    finally:
        client.close()
        print("Connection closed")

async def send_data(client, message, chunk_size):
    data = message.encode('ascii')
    bytes_sent = 0
    while bytes_sent < len(data):
        bytes_to_send = min(chunk_size, len(data) - bytes_sent)
        client.sendall(data[bytes_sent:bytes_sent + bytes_to_send])
        bytes_sent += bytes_to_send
        await asyncio.sleep(0.05)
    print("Data sent to client")

async def wait_for_confirmation_with_timeout(client, timeout_seconds):
    buffer = bytearray(1)
    try:
        while True:
            client.settimeout(timeout_seconds)
            try:
                bytes_read = client.recv_into(buffer)
                if bytes_read > 0:
                    received_char = chr(buffer[0])
                    print(f"Received char: {received_char}")
                    

                    if received_char == '!':
                        return True  # Confirmation received
            except socket.timeout:
                return False  # Timeout
            await asyncio.sleep(0.1)  # Wait before the next cycle
    except Exception:
        pass

    return False  # Timeout

async def clear_stream_buffer(client):
    buffer = bytearray(1024)
    while True:
        client.settimeout(0.1)
        try:
            client.recv_into(buffer)
        except socket.timeout:
            break

async def main():
    port = 10001  # Listening port
    timeout_seconds = 5  # Timeout for waiting for confirmation
    chunk_size = 1024  # Data chunk size for sending

    server = await asyncio.start_server(
        lambda r, w: handle_client(w, timeout_seconds, chunk_size),
        '0.0.0.0', port
    )

    async with server:
        print(f"Mera MW started on port {port}. Waiting for client connection...")
        await server.serve_forever()

asyncio.run(main())