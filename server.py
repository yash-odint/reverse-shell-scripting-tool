#this file will go to server (Our created droplet on DigitalOcean)
import socket
import sys

def create_socket():
    try:
        global host
        global port 
        global s
        
        #Here host = "" means it will automatically get its own ip
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket connection error : " + msg)

def bind_socket():
    try:
        global host
        global port 
        global s

        print("Binding the port " + str(port))

        s.bind((host, port))
        s.listen(5)
    
    except socket.error as msg:
        print("Socket binding error " + msg)
        bind_socket()

def socket_accept():
    conn, address = s.accept()
    print("Connection has established | IP " + address[0] + "| PORT " + str(address[1]))
    send_commands(conn)
    conn.close()

def send_commands(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), 'utf-8')
            print(client_response, end='')
        

def main():
    create_socket()
    bind_socket()
    socket_accept()

main()