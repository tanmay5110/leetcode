import java.io.*;
import java.net.*;

public class HelloServer {
    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(12345);
            System.out.println("Server is listening on port 12345...");
            
            Socket socket = serverSocket.accept();
            System.out.println("Client connected: " + socket.getInetAddress());
            
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            
            String message = in.readLine();
            System.out.println("Client says: " + message);
            
            out.println("Hello Client! This is Server.");
            
            socket.close();
            serverSocket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}