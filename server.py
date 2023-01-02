import socket as s
import select as sel
import sys

HOST = ''
PORT = 4444
SOCKET_LIST = []
RECEIVE_BUFF = 4096

def chat_server():
    server_socket=s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    server_socket.bind((HOST,PORT))
    server_socket.listen(10)
    SOCKET_LIST.append(server_socket)

    print("Chat server started, listening on port {}",str(PORT))

    while True:
        #blocking the flow for new incoming connection...
        ready_read, ready_write, error = sel.select(SOCKET_LIST, [], [], 0)

        for sock in ready_read:
            print("Edhachum sollu na......")
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                SOCKET_LIST.append(client_socket)
                print(addr)
                print("Client {}:{} Connected.".format(addr[0],addr[1]))
                broadcast(server_socket, client_socket, "{} entered out chatting room... \n".format(addr))

            else:
                try:
                    data = sock.recv(RECEIVE_BUFF)
                    data = data.decode()
                    if data:
                        broadcast(server_socket, client_socket, "[{}] {}".format(sock.getpeername(), data))
                    else:
                        broadcast(server_socket, client_socket, "[{}] {}".format(sock.getpeername(), "Client is offline \n"))
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        
                except:
                    broadcast(server_socket, client_socket, "[{}] {}".format(sock.getpeername(), "Client is offline, excption \n"))
                    continue
    #TODO: Plan exit strategy
    #server_socket.close()

def broadcast(server_socket, client_socket, message):
    print("broadcast: " + message)
    for socket in SOCKET_LIST:
        #print(SOCKET_LIST)
        if socket != server_socket and socket != client_socket:
            try:
                socket.send(message.encode())
                
            except:
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


if __name__== "__main__":
    sys.exit(chat_server())