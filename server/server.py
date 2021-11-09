from datetime import datetime
import socket
import threading

logfile = open(".log", "w")

class Member:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.log_client("Connected")

    def disconnect(self):
        self.conn.close()
        print("[-] Client Disconnected: {self.addr}")
        self.log_client("Disconnected")

    def log_client(self, status):
        # save the user addresses and thier status
        time = str(datetime.now())
        logfile.write(f"[{time}] Client {status}: {self.addr}\n")
        pass

class Server:
    def __init__(self, host):
        self.host = host
        self.port = 5000

        self.server = socket.socket()
        self.server.bind((self.host, self.port))
        self.server.listen(5)

        self.cnt_members = 0
        self.active_members = []
        self.members_thread = []

    def start(self):
        print(f"[+] Service started at {self.host}:{self.port}")
        self.log_server(f"Service started at {self.host}:{self.port}")
        while(True):
            conn, addr = self.server.accept()
            member = Member(conn, addr)
            self.cnt_member += 1
            print(f"[+] Got connection from {addr}, Total clients : {self.cnt_member}")
            self.log_server(f"Got connection from {addr}, Total clients : {self.cnt_member}")

            member_thread = threading.Thread(target = self.handel_client, args = (member, ))
            
            # storing client data
            self.active_members.append(member)
            self.members_thread.append(member_thread)

            # handel client
            member_thread.start()

    def handel_client(self, client):
        try:
            while(True):
                data = client.conn.recv(4096)
                for member in self.active_members:
                    if member.addr != client.addr:
                        # filter whom this message has to be sended 
                        # currently it sending message to all other members except you
                        member.conn.send(data)
        except:
            client.disconnect()

    def close(self):
        print("[-] Closing the server Gracefully")
        log_server("Closing the server Gracefully")

        for member in self.active_members:
            member.disconnect()

        for thread in self.members_thread:
            thread.join()

        self.server.close()

    def log_server(self, message):
        # save the logs
        time = str(datetime.now())
        logfile.write(f"[{time}] {message}\n")
        pass

if __name__ == "__main__":
    server = Server("0.0.0.0")
    try:
        server.start()
    except KeyboardInterrupt:
        server.close()
