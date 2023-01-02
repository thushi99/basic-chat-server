import sys
import socket
import select as sel

SOCK_LIST = [sys.stdin]
RECEIVE_BUFF = 4096

def chat_client():
    if len(sys.argv) < 3:
        print("Usage: python3 {} hostname port".format(sys.argv[0]))
    
    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    s.settimeout(100)

    try:
        s.connect((host,port))
    except:
        print("Cannot reach the {}:{}...".format(host, port))
        sys.exit(-1)

    print("Connected to remote host. You can start sending messages...")
    sys.stdout.write("> ")
    sys.stdout.flush()

    while True:
        read_ready, write_ready, error = sel.select(SOCK_LIST, [], [])
        for sock in read_ready:
            if sock == s:
                data = data.recv(RECEIVE_BUFF)
                if not data:
                    print("Chat disconnected.")
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.write("> ")
                    sys.stdout.flush()
            else:
                msg = sys.stdin.readline()
                s.send(msg.encode())
                sys.stdout.write("> ")
                sys.stdout.flush()
                

if __name__ == "__main__":
    sys.exit(chat_client())
