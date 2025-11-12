import java.io.*;
import java.net.*;

public class UDPSender {

    public static void main(String[] args) throws Exception {

        String SERVER_IP = "127.0.0.1"; // Use receiver IP if on another machine
        int PORT = 5005;
        int BUFFER_SIZE = 4096;

        DatagramSocket socket = new DatagramSocket();
        InetAddress serverAddr = InetAddress.getByName(SERVER_IP);

        // Files to send (ensure they exist in the current directory)
        String[] filesToSend = {"example.txt", "example.js", "tiny_audio.mp3", "ro.mp4"};

        for (String fileName : filesToSend) {
            File file = new File(fileName);

            // Send filename
            byte[] nameData = fileName.getBytes();
            socket.send(new DatagramPacket(nameData, nameData.length, serverAddr, PORT));

            // Wait for ACK
            byte[] ackBuf = new byte[BUFFER_SIZE];
            DatagramPacket ackPacket = new DatagramPacket(ackBuf, ackBuf.length);
            socket.receive(ackPacket);
            String ack = new String(ackPacket.getData(), 0, ackPacket.getLength());

            if (!ack.equals("FILENAME_RECEIVED")) {
                System.out.println("Receiver did not acknowledge " + fileName);
                continue;
            }

            // Send file data
            FileInputStream fis = new FileInputStream(file);
            byte[] buffer = new byte[BUFFER_SIZE];
            int bytesRead;

            while ((bytesRead = fis.read(buffer)) != -1) {
                socket.send(new DatagramPacket(buffer, bytesRead, serverAddr, PORT));
            }

            fis.close();

            // Send EOF
            socket.send(new DatagramPacket("EOF".getBytes(), 3, serverAddr, PORT));
            System.out.println("Sent file: " + fileName);
        }

        // Send EXIT
        socket.send(new DatagramPacket("EXIT".getBytes(), 4, serverAddr, PORT));
        socket.close();
        System.out.println("All files sent successfully!");
    }
}


