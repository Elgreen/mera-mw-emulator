import asyncio

async def handle_client(reader, writer, timeout_seconds, chunk_size):
    try:
        while True:
            # Read weight input from the user
            input_weight = await asyncio.get_event_loop().run_in_executor(None, input, "Enter weight: ")
            try:
                weight = float(input_weight)
            except ValueError:
                print("Invalid weight input.")
                continue

            code = "<No_Code>"  # Simulate absence of product code
            sign = "+"
            weight_string = "{:07.3f}".format(weight)  # Format weight as "000.000"
            stability = " "  # Stable weight

            # Form the message according to the protocol
            message = f"{code}{sign}{weight_string} kg {stability}\x0d\x1E"

            await send_data(writer, message, chunk_size)
            await clear_stream_buffer(reader)

            # Wait for confirmation
            confirmation_received = await wait_for_confirmation_with_timeout(reader, timeout_seconds)
            if confirmation_received:
                print("Confirmation received.")
            else:
                print("Error: confirmation not received.")
    except Exception as ex:
        print(f"Error working with client: {ex}")
    finally:
        writer.close()
        await writer.wait_closed()
        print("Client disconnected.")

async def send_data(writer, message, chunk_size):
    data = message.encode('ascii')
    bytes_sent = 0
    while bytes_sent < len(data):
        bytes_to_send = min(chunk_size, len(data) - bytes_sent)
        writer.write(data[bytes_sent:bytes_sent + bytes_to_send])
        await writer.drain()
        bytes_sent += bytes_to_send
        await asyncio.sleep(0.05)
    print("Data sent to client")

async def wait_for_confirmation_with_timeout(reader, timeout_seconds):
    try:
        while True:
            try:
                data = await asyncio.wait_for(reader.read(1), timeout=timeout_seconds)
                if data:
                    received_char = data.decode('ascii')
                    print(f"Received character: {received_char}")
                    if received_char == '!':
                        return True  # Confirmation received
                else:
                    # No data received, connection closed
                    return False
            except asyncio.TimeoutError:
                # Timeout occurred
                return False
            await asyncio.sleep(0.1)
    except Exception as ex:
        # An error occurred
        print(f"Error: {ex}")
        return False

async def clear_stream_buffer(reader):
    try:
        while True:
            try:
                data = await asyncio.wait_for(reader.read(1024), timeout=0.1)
                if not data:
                    break
                # Ignore read data
            except asyncio.TimeoutError:
                break
    except Exception:
        pass

async def main():
    port = 10001  # Server port
    timeout_seconds = 5  # Timeout for confirmation
    chunk_size = 1024  # Size of data chunk to send

    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, timeout_seconds, chunk_size),
        '0.0.0.0', port)

    print(f"Server started on port {port}. Waiting for client connection...")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as ex:
        print(f"Server error: {ex}")
