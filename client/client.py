import socket
import threading
import pyaudio

Format = pyaudio.paInt16
Chunks = 4096
Channels = 2
Rate = 44100

class Client:
    def __init__(self, host):
        self.client = socket.socket()
        self.host = host
        self.port = 5000

        self.client.connect((self.host, self.port))

        print(f"Connected to the server horray :)")

        self.audio_pipe = pyaudio.PyAudio()

        self.input_stream = self.audio_pipe.open(format = Format,
                      channels = Channels,
                      rate = Rate,
                      input = True,
                      frames_per_buffer = Chunks)

        self.output_stream = self.audio_pipe.open(format = Format,
                      channels = Channels,
                      rate = Rate,
                      output = True,
                      frames_per_buffer = Chunks)

        self.shutdown = True
        self.send_thread = threading.Thread(target = self.send)
        self.recieve_thread = threading.Thread(target = self.receive)

    def start(self):
        self.shutdown = False

        self.recieve_thread.start()
        self.send()

    def send(self):
        while not self.shutdown:
            try:
                data = self.input_stream.read(Chunks)
                self.client.send(data)
            except:
                print("[-] Server Connection Lost :(")
                break
        self.close()

    def receive(self):
        while not self.shutdown:
            try:
                data = self.client.recv(Chunks)
                self.output_stream.write(data)
            except:
                break

    def close(self):
        print("[-] Closing the client gracefully ..")
        self.shutdown = True

        self.recieve_thread.join()

        self.input_stream.close()
        self.output_stream.close()
        self.audio_pipe.terminate()

if __name__ == '__main__':
    try:
        client = Client("<HOST_IP>")
        client.start()
    except ConnectionRefusedError as e:
        print("[-] Unable to connect to the server. Host seems down :(")
    except KeyboardInterrupt:
        client.close()

