import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class UDPClient {
    public static void main(String[] args) {
        try (DatagramSocket client = new DatagramSocket()) {
            String message = "Hey Server, UDP connection looks good!";
            byte[] buffer = message.getBytes();
            
            InetAddress serverAddress = InetAddress.getByName("localhost");
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length, serverAddress, 12345);
            
            client.send(packet);
            System.out.println("Message sent to server: " + message);

        } catch (Exception e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }
}