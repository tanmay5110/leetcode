import java.io.*;
import java.net.*;

public class TCPServer {
    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(12345)) {
            System.out.println("Server running on port 12345... Waiting for client");

            try (Socket client = serverSocket.accept();
                 BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
                 PrintWriter out = new PrintWriter(client.getOutputStream(), true)) {

                System.out.println("Connected to: " + client.getInetAddress());
                String msg = in.readLine();
                System.out.println("Client: " + msg);
                out.println("Received: " + msg);
            }
        } catch (IOException e) {
            System.out.println("Server error: " + e.getMessage());
        }
    }
}