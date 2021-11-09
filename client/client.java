import java.io.*;
import java.net.*;
import javax.sound.sampled.*;
import javax.swing.JOptionPane; 

class Client {
    public final static String SERVER = JOptionPane.showInputDialog("Please enter server    ip");
    public static TargetDataLine microphone = null;
    public static Socket connection = null;
    public static DataOutputStream dos = null;

    public static void main(String[] args) throws Exception {

        AudioFormat format = new AudioFormat(8000.0f,8,1,true,false);
        DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
        microphone = (TargetDataLine)AudioSystem.getLine(info);
        microphone.open(format);
        microphone.start();

        try {
            connection = new Socket(SERVER,5000);
            System.out.println("Connected to the server horray :)");
        } catch (ConnectException e) {
            System.out.println("[-] Unable to connect to the server. Host seems down :(");
            return;
        }

        dos = new DataOutputStream(connection.getOutputStream());

        Thread inThread = new Thread(new SoundReceiver(connection));
        inThread.start();
        send();

    }

    public static void send() throws Exception {
        int bytesRead = 0;
        byte[] soundData = new byte[1];

        while(bytesRead != -1) {
            bytesRead = microphone.read(soundData, 0, soundData.length);
            if(bytesRead >= 0) {
                try {
                    dos.write(soundData, 0, bytesRead);
                } catch (Exception e){
                    break;
                }
            }
        }

        System.out.println("[-] Server Connection Lost :(");
        
    }
}


class SoundReceiver implements Runnable {
    Socket connection = null;
    DataInputStream soundIn = null;
    SourceDataLine inSpeaker = null;

    public SoundReceiver(Socket connection) throws Exception {
        connection = connection;
        soundIn = new DataInputStream(connection.getInputStream());
        AudioFormat af = new AudioFormat(8000.0f,8,1,true,false);
        DataLine.Info info = new DataLine.Info(SourceDataLine.class, af);
        inSpeaker = (SourceDataLine)AudioSystem.getLine(info);
        inSpeaker.open(af);
    }

    public void run() {
        int bytesRead = 0;
        byte[] inSound = new byte[1];
        inSpeaker.start();
        while(bytesRead != -1) {
            try{
                bytesRead = soundIn.read(inSound, 0, inSound.length);
            } catch (Exception e){
                break;
            }
            if(bytesRead >= 0) {
                inSpeaker.write(inSound, 0, bytesRead);
            }
        }
    }
}