import java.io.*;
import java.net.*;

public class UDPReceiver {

    public static void main(String[] args) throws Exception {

        int PORT = 5005;
        int BUFFER_SIZE = 4096;

        DatagramSocket socket = new DatagramSocket(PORT);
        System.out.println("Receiver running... waiting for files.");

        byte[] buffer = new byte[BUFFER_SIZE];
        File receiverFolder = new File(System.getProperty("user.home") + "/udp_receiver");
        receiverFolder.mkdirs();

        while (true) {
            // Receive filename
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            socket.receive(packet);

            String fileName = new String(packet.getData(), 0, packet.getLength());
            if (fileName.equals("EXIT")) break;

            // Send ACK
            InetAddress clientAddr = packet.getAddress();
            int clientPort = packet.getPort();
            String ack = "FILENAME_RECEIVED";
            socket.send(new DatagramPacket(ack.getBytes(), ack.length(), clientAddr, clientPort));

            // Save file
            File file = new File(receiverFolder, fileName);
            FileOutputStream fos = new FileOutputStream(file);

            while (true) {
                DatagramPacket chunkPacket = new DatagramPacket(buffer, buffer.length);
                socket.receive(chunkPacket);
                String data = new String(chunkPacket.getData(), 0, chunkPacket.getLength());
                if (data.equals("EOF")) break;

                fos.write(chunkPacket.getData(), 0, chunkPacket.getLength());
            }

            fos.close();
            System.out.println("File " + fileName + " received successfully!");
        }

        System.out.println("All files received.");
        socket.close();
    }
}

