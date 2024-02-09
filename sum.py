# some ctf solver..?
from pwn import *

context.log_level = 'error'

# Define the target host and port
target_host = "4.234.214.36"
target_port = 1256  # Replace with the actual port

i=0

conn = remote(target_host, target_port)

def solve(line,i):
    decoded_line = line.decode('utf-8')[2:-1]
    decoded_bytes = base64.b64decode(decoded_line)
    decoded_string = decoded_bytes.decode('utf-8')
    print('received ',decoded_string)
    op = decoded_string.split()
    num1 = int(op[0])
    operator = op[1]
    num2 = int(op[2])
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    elif operator == '/':
        result = num1 / num2
    result=str(result)
    print('sent ', result)
    conn.sendline(result)
    
while True:
    
    try:    
        if i == 100:
            print('aici')
            print(conn.recvall())

        # Wait for the 'hello' message
        c = conn.recvline().strip()

        

        solve(c,i)
        i=i+1
    except EOFError as e:
        # Socket is closed, exit the loop
        print(e)
        break   
  
conn.close()  # Close the connection

print("Brute-force complete.")
