import java.io.*;
import java.net.*;

public class TCPClient {
    public static void main(String[] args) {
        try (Socket socket = new Socket("localhost", 12345);
             BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {

            out.println("Hey Server, connection looks good!");
            System.out.println("Server replied: " + in.readLine());

        } catch (IOException e) {
            System.out.println("Client error: " + e.getMessage());
        }
    }
}