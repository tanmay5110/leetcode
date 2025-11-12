import java.io.*;
import java.net.*;

public class TCPFileServer {
    public static void main(String[] args) {
        try {
            ServerSocket serverSocket = new ServerSocket(12346);
            System.out.println("Server is waiting for file...");
            
            Socket socket = serverSocket.accept();
            System.out.println("Connected to: " + socket.getInetAddress());
            
            DataInputStream dis = new DataInputStream(socket.getInputStream());
            
            // Receive file name first
            String fileName = dis.readUTF();
            FileOutputStream fos = new FileOutputStream("received_" + fileName);
            
            byte[] buffer = new byte[4096];
            int bytesRead;
            
            while ((bytesRead = dis.read(buffer)) != -1) {
                fos.write(buffer, 0, bytesRead);
            }
            
            System.out.println("File received successfully: " + fileName);
            
            fos.close();
            dis.close();
            socket.close();
            serverSocket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}