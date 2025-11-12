import java.io.*;
import java.net.*;

public class TCPFileClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 12346);
            DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
            
            String fileName = "example.txt"; // Change filename here
            FileInputStream fis = new FileInputStream(fileName);
            
            // Send file name first
            dos.writeUTF(fileName);
            
            byte[] buffer = new byte[4096];
            int bytesRead;
            
            while ((bytesRead = fis.read(buffer)) != -1) {
                dos.write(buffer, 0, bytesRead);
            }
            
            System.out.println("File sent successfully: " + fileName);
            
            fis.close();
            dos.close();
            socket.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}