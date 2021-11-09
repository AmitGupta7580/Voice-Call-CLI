# Voice Call App
Implement an CLI Voice Calling Application.

## Client
Created in both Python and Java language

### Python
- Audio Library : (pyaudio)
- Usage:
  - Run `pip install pyaudio` in the terminal.
  - Change the host IP with your server IP.
  - Run `python client.py` in the terminal.

### Java
- Audio Library : (javax.sound.sampled.*)
- Usage:
  - Compile java code `javac client.java` in the terminal.
  - Run `java Client` in the terminal.
  - Enter the server IP in the poped dialogbox.

## Server

### Deployment (Azure Cloud VM)
- Create a VM on AZURE cloud with public IP enable in the Network Interface.
- Change the Inbound Rule in Networking and allow port `5000` for communication.
- Login to VM via ssh client : `putty` or terminal
- Run `scp server.py username@IP:~/` in the terminal or clone this git repo `git clone https://github.com/AmitGupta7580/Voice-Call-CLI.git` to get the server code file on VM.

### Usage
- Run `python server.py` in the terminal.
- A Log file will be created after the whole execution to store the record what happens when.
