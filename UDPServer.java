import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class UDPServer {
    public static void main(String[] args) {
        try (DatagramSocket server = new DatagramSocket(12345)) {
            System.out.println("UDP Server running on 12345...");

            while (true) {
                byte[] buffer = new byte[1024];
                DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                server.receive(packet);

                String msg = new String(packet.getData(), 0, packet.getLength());
                System.out.println("Client: " + msg);
                System.out.println("IP: " + packet.getAddress() + " | Port: " + packet.getPort());
            }

        } catch (Exception e) {
            System.out.println("Server error: " + e.getMessage());
        }
    }
}