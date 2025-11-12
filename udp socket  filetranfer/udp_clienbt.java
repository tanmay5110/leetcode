import java.io.*;
import java.net.*;

public class UDPFileClient {
    public static void main(String[] args) {
        try {
            DatagramSocket socket = new DatagramSocket();
            InetAddress address = InetAddress.getByName("localhost");
            String fileName = "hello.txt"; // Try text, audio, or video file
            
            // Send filename first
            byte[] nameData = fileName.getBytes();
            DatagramPacket namePacket = new DatagramPacket(nameData, nameData.length, 
                                                          address, 12347);
            socket.send(namePacket);
            
            // Send file data in chunks
            FileInputStream fis = new FileInputStream(fileName);
            byte[] buffer = new byte[4096];
            int bytesRead;
            
            while ((bytesRead = fis.read(buffer)) != -1) {
                DatagramPacket packet = new DatagramPacket(buffer, bytesRead, address, 12347);
                socket.send(packet);
                Thread.sleep(1); // small delay to avoid overflow
            }
            
            // Send end signal
            byte[] endData = "END".getBytes();
            DatagramPacket endPacket = new DatagramPacket(endData, endData.length, address, 12347);
            socket.send(endPacket);
            
            fis.close();
            socket.close();
            System.out.println("File sent successfully!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}


/*
===================================================================================
                    COMPREHENSIVE UDP CLIENT THEORY AND LINE-BY-LINE EXPLANATION
===================================================================================

CLIENT-SERVER ARCHITECTURE IN NETWORK PROGRAMMING:
=================================================

CLIENT ROLE:
- Initiates communication with server
- Sends requests or data to server
- May receive responses from server
- Usually short-lived (connects, transfers data, disconnects)

SERVER ROLE:
- Waits for client connections/requests
- Processes incoming data
- May send responses back to clients
- Usually long-running (continuously listening)

UDP CLIENT-SERVER COMMUNICATION FLOW:
====================================

1. CLIENT STARTUP:
   - Create DatagramSocket (no specific port needed)
   - Prepare data to send (filename, file content)
   - Create DatagramPackets with server address/port

2. SERVER STARTUP:
   - Create DatagramSocket bound to specific port
   - Create buffer to receive incoming packets
   - Wait for incoming packets (blocking receive)

3. DATA TRANSFER:
   - Client sends filename packet to server
   - Server receives filename and prepares to receive file
   - Client reads file in chunks and sends each as UDP packet
   - Server receives each packet and writes to output file
   - Client sends "END" signal when file transfer complete
   - Server detects "END" signal and closes file

4. CLEANUP:
   - Both client and server close sockets
   - File streams are closed
   - Resources are released

COMPARISON: TCP vs UDP FILE TRANSFER:
===================================

TCP FILE TRANSFER CHARACTERISTICS:
- Reliable delivery (guaranteed arrival)
- Ordered delivery (packets arrive in sequence)
- Error correction (automatic retransmission)
- Flow control (prevents overwhelming receiver)
- Connection-oriented (handshake required)
- Higher overhead (more complex protocol)

UDP FILE TRANSFER CHARACTERISTICS:
- Best-effort delivery (no guarantees)
- No ordering guarantees (packets may arrive out of order)
- No error correction (application must handle)
- No flow control (sender can overwhelm receiver)
- Connectionless (no handshake needed)
- Lower overhead (simpler protocol)

WHY USE UDP FOR FILE TRANSFER?
- Faster transmission (no connection setup)
- Lower network overhead
- Suitable for local networks (lower packet loss)
- Real-time applications where speed > reliability
- Broadcasting/multicasting scenarios
- Simple protocol implementation

CHALLENGES WITH UDP FILE TRANSFER:
- Packet loss (some data may not arrive)
- Out-of-order delivery (packets may arrive mixed up)
- Duplicate packets (same packet may arrive multiple times)
- No built-in error detection/correction
- No flow control (fast sender may overwhelm slow receiver)

FILE I/O IN JAVA:
================

FileInputStream:
- Reads data from files as bytes
- Sequential reading (start to finish)
- Buffer-based reading for efficiency
- Must be closed to free resources

FileOutputStream:
- Writes data to files as bytes
- Sequential writing (overwrites existing content)
- Buffer-based writing for efficiency
- Must be closed to ensure data is flushed

THREADING CONSIDERATIONS:
========================

SINGLE-THREADED MODEL (current implementation):
- Client sends data sequentially
- Server receives data sequentially
- Simple to implement and debug
- May be slower for large files

MULTI-THREADED MODEL (advanced):
- Separate threads for sending/receiving
- Better performance for concurrent operations
- More complex synchronization required
- Suitable for handling multiple clients

NETWORK PERFORMANCE FACTORS:
===========================

PACKET SIZE OPTIMIZATION:
- Smaller packets: Less data loss per packet, more overhead
- Larger packets: More data loss per packet, less overhead
- MTU (Maximum Transmission Unit): Typical 1500 bytes for Ethernet
- Fragmentation: Large packets split into smaller ones

DELAY AND THROUGHPUT:
- Thread.sleep(1): Prevents overwhelming receiver
- Network latency: Time for packet to travel
- Bandwidth: Amount of data that can be sent per second
- Congestion: Network overload affecting performance

ERROR HANDLING STRATEGIES:
=========================

EXCEPTION TYPES IN NETWORK PROGRAMMING:

IOException:
- Generic I/O error (file not found, read/write errors)
- Network connectivity issues
- File permission problems

SocketException:
- Socket creation failures
- Port already in use
- Network interface issues

UnknownHostException:
- Invalid hostname resolution
- DNS lookup failures
- Network configuration problems

ROBUST ERROR HANDLING APPROACH:
try {
    // Network operations
} catch (UnknownHostException e) {
    // Handle hostname resolution errors
} catch (SocketException e) {
    // Handle socket-specific errors
} catch (IOException e) {
    // Handle general I/O errors
} finally {
    // Cleanup resources (close sockets, streams)
}

PROTOCOL DESIGN ANALYSIS:
========================

COMMUNICATION PROTOCOL STEPS:
1. Client sends filename to establish what's being transferred
2. Server receives filename and prepares to receive file
3. Client reads file in 4KB chunks and sends each as UDP packet
4. Server receives each chunk and writes to output file
5. Client sends "END" signal when file reading complete
6. Server detects "END" and closes file
7. Both client and server clean up resources

POTENTIAL PROTOCOL IMPROVEMENTS:
- Add packet sequence numbers for ordering
- Include file size in initial packet for progress tracking
- Implement acknowledgment system (server confirms receipt)
- Add checksums for data integrity verification
- Include retry mechanism for lost packets
- Add timeout handling for network delays
- Implement compression for large files

LIMITATIONS OF CURRENT IMPLEMENTATION:
- No error recovery (lost packets are lost forever)
- No packet ordering (file could be corrupted if packets arrive out of order)
- No flow control (client might send faster than server can process)
- No data integrity checking (corrupted packets not detected)
- No security features (no authentication or encryption)

REAL-WORLD CONSIDERATIONS:
- Network reliability varies (WiFi vs Ethernet vs Internet)
- Firewalls may block UDP traffic
- Large files increase probability of packet loss
- Server must be running before client starts
- Port 12347 must be available on server machine
*/

/*
===================================================================================
                    DUPLICATED CODE WITH LINE-BY-LINE COMMENTS
===================================================================================
*/

// Line 1: Import all classes from java.io package for file operations
import java.io.*;
// Line 2: Import all classes from java.net package for network operations
import java.net.*;

// Line 4: Declare public class UDPFileClient - class name must match filename
public class UDPFileClient {
    // Line 5: Main method - program entry point executed by JVM
    public static void main(String[] args) {
        // Line 6: Start try-catch block for exception handling
        try {
            // Line 7: Create UDP socket with system-assigned port for sending
            DatagramSocket socket = new DatagramSocket();
            // Line 8: Resolve "localhost" hostname to IP address (127.0.0.1)
            InetAddress address = InetAddress.getByName("localhost");
            // Line 9: Define filename of file to transfer - hardcoded string
            String fileName = "hello.txt"; // Try text, audio, or video file
            
            // Line 11: Comment explaining we send filename first in protocol
            // Send filename first
            // Line 12: Convert filename string to byte array for network transmission
            byte[] nameData = fileName.getBytes();
            // Line 13-14: Create UDP packet with filename, destination address and port
            DatagramPacket namePacket = new DatagramPacket(nameData, nameData.length, 
                                                          address, 12347);
            // Line 15: Send filename packet to server at specified address/port
            socket.send(namePacket);
            
            // Line 17: Comment explaining file data transmission phase
            // Send file data in chunks
            // Line 18: Open file for reading as stream of bytes
            FileInputStream fis = new FileInputStream(fileName);
            // Line 19: Create 4KB buffer array for reading file chunks
            byte[] buffer = new byte[4096];
            // Line 20: Variable to store actual number of bytes read from file
            int bytesRead;
            
            // Line 22: Loop to read and send file in chunks until end reached
            while ((bytesRead = fis.read(buffer)) != -1) {
                // Line 23: Create packet with file chunk data for transmission
                DatagramPacket packet = new DatagramPacket(buffer, bytesRead, address, 12347);
                // Line 24: Send file data chunk packet to server
                socket.send(packet);
                // Line 25: Pause 1 millisecond to prevent overwhelming server
                Thread.sleep(1); // small delay to avoid overflow
            }
            
            // Line 28: Comment explaining end signal transmission
            // Send end signal
            // Line 29: Convert "END" string to byte array for final signal
            byte[] endData = "END".getBytes();
            // Line 30: Create packet containing END termination signal
            DatagramPacket endPacket = new DatagramPacket(endData, endData.length, address, 12347);
            // Line 31: Send END signal packet to notify server transfer complete
            socket.send(endPacket);
            
            // Line 33: Close file input stream to release file handle
            fis.close();
            // Line 34: Close UDP socket to release network resources
            socket.close();
            // Line 35: Print success message confirming file was sent
            System.out.println("File sent successfully!");
        // Line 36: Catch any exception that occurs during execution
        } catch (Exception e) {
            // Line 37: Print detailed exception information for debugging
            e.printStackTrace();
        }
    }
}