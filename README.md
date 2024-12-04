# Mera MW scales protocol emulator

## Run

Run emulator:

```
python3 main.py
```

## Config

Default parameters can be configured in main() function:

```
    port = 10001  # Server port
    timeout_seconds = 5  # Timeout for confirmation
    chunk_size = 1024  # Size of data chunk to send
```

## Instructions to connect and get values using telnet

1. **Start the Emulator**:
   Run the emulator using the command:
   ```
   python3 main.py
   ```

2. **Connect Using Telnet**:
   Open a terminal and connect to the emulator using telnet:
   ```
   telnet localhost 10001
   ```

3. **Enter Weight**:
   Once connected, you will be prompted to enter a weight in emulator console. Type the weight value and press Enter. The emulator will send the weight data and wait for a confirmation.

4. **Receive Confirmation**:
   Enter `!` in telnet console and press Enter to send it. If the confirmation character `!` is received, it will print "Confirmation received." Otherwise, it will print "Error: confirmation not received."

5. **Repeat**:
   You can continue to enter weight values and receive confirmations as needed.