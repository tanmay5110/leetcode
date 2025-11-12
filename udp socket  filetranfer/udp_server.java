import java.io.*;
import java.net.*;

public class UDPFileServer {
    public static void main(String[] args) {
        try {
            DatagramSocket socket = new DatagramSocket(12347);
            byte[] buffer = new byte[4096];
            
            // Receive filename first
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            socket.receive(packet);
            String fileName = new String(packet.getData(), 0, packet.getLength());
            System.out.println("Receiving file: " + fileName);
            
            FileOutputStream fos = new FileOutputStream("udp_received_" + fileName);
            
            while (true) {
                packet = new DatagramPacket(buffer, buffer.length);
                socket.receive(packet);
                String msg = new String(packet.getData(), 0, packet.getLength());
                if (msg.equals("END")) break; // End of file signal
                fos.write(packet.getData(), 0, packet.getLength());
            }
            
            fos.close();
            socket.close();
            System.out.println("File received successfully!");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}


/*
===================================================================================
                    COMPREHENSIVE TCP/UDP NETWORKING THEORY AND EXPLANATION
===================================================================================

WHAT IS NETWORK PROGRAMMING?
===========================
Network programming allows applications running on different computers to communicate
over a network (LAN/WAN/Internet). Java provides robust networking capabilities through
the java.net package, which includes classes for both TCP and UDP communication.

TCP vs UDP - FUNDAMENTAL DIFFERENCES:
====================================

TCP (Transmission Control Protocol):
-----------------------------------
CHARACTERISTICS:
- Connection-oriented protocol
- Reliable data delivery guaranteed
- Data arrives in order (sequencing)
- Error detection and correction
- Flow control (prevents overwhelming receiver)
- Congestion control (prevents network overload)
- Higher overhead due to reliability features

WHEN TO USE TCP:
- File transfers (reliability crucial)
- Web browsing (HTTP/HTTPS)
- Email (SMTP, POP3, IMAP)
- Remote login (SSH, Telnet)
- Database connections
- Any application where data integrity is critical

TCP CONNECTION PROCESS (3-Way Handshake):
1. Client sends SYN (synchronize) to server
2. Server responds with SYN-ACK (synchronize-acknowledge)
3. Client sends ACK (acknowledge) back to server
4. Connection established - data transfer can begin

TCP DATA TRANSFER:
- Data sent in segments with sequence numbers
- Receiver sends acknowledgments for received data
- Lost packets are automatically retransmitted
- Duplicate packets are discarded
- Data delivered to application in correct order

TCP CONNECTION TERMINATION (4-Way Handshake):
1. Client sends FIN (finish) to server
2. Server sends ACK for the FIN
3. Server sends its own FIN to client
4. Client sends ACK for server's FIN
5. Connection closed

UDP (User Datagram Protocol):
----------------------------
CHARACTERISTICS:
- Connectionless protocol
- No reliability guarantees (best-effort delivery)
- No ordering guarantees
- No error correction (only detection)
- No flow control
- No congestion control
- Lower overhead (faster)
- Smaller packet headers

WHEN TO USE UDP:
- Real-time applications (video/audio streaming)
- Online gaming (low latency required)
- DNS queries (small, quick requests)
- DHCP (network configuration)
- Broadcasting/multicasting
- Applications where speed > reliability

UDP COMMUNICATION PROCESS:
1. Create datagram packet with data
2. Send packet to destination
3. No connection establishment needed
4. No acknowledgment expected
5. Packet may arrive, may not arrive, may arrive out of order

JAVA NETWORKING CLASSES:
=======================

UDP CLASSES:
-----------
DatagramSocket:
- Represents a socket for sending/receiving datagram packets
- Can bind to specific port for receiving
- Used by both client and server

DatagramPacket:
- Represents a datagram packet
- Contains data, length, destination address, and port
- Immutable once created

InetAddress:
- Represents an IP address (IPv4 or IPv6)
- Used to specify destination for packets
- Can resolve hostnames to IP addresses

TCP CLASSES (for comparison):
----------------------------
Socket (Client):
- Represents client-side TCP connection
- Provides input/output streams for communication
- Connects to server socket

ServerSocket (Server):
- Listens for incoming TCP connections
- Creates new Socket for each client connection
- Runs on specific port

DATAGRAM PACKET STRUCTURE:
=========================
UDP Header (8 bytes):
- Source Port (2 bytes): Sender's port number
- Destination Port (2 bytes): Receiver's port number  
- Length (2 bytes): Total length of UDP header + data
- Checksum (2 bytes): Error detection (optional in IPv4)

Data Payload:
- Maximum theoretical size: 65,507 bytes (65,535 - 8 - 20)
- Practical limit often much smaller (MTU restrictions)
- Common sizes: 512-1500 bytes to avoid fragmentation

NETWORK ADDRESSING:
==================
IP Address: Unique identifier for network devices
- IPv4: 32-bit address (192.168.1.1)
- IPv6: 128-bit address (2001:db8::1)

Port Numbers: Identify specific services/applications
- Range: 0-65535
- Well-known ports: 0-1023 (HTTP=80, HTTPS=443, FTP=21)
- Registered ports: 1024-49151
- Dynamic/Private ports: 49152-65535

Socket: Combination of IP address + port number
- Example: 192.168.1.1:8080
- Uniquely identifies communication endpoint

NETWORK COMMUNICATION FLOW:
===========================

CLIENT-SERVER MODEL:
Server:
1. Create server socket and bind to port
2. Listen for incoming connections/packets
3. Process received data
4. Send response if needed
5. Continue listening (usually in loop)

Client:
1. Create client socket
2. Connect to server (TCP) or prepare packet (UDP)
3. Send data to server
4. Receive response if expected
5. Close connection/socket

FILE TRANSFER CONSIDERATIONS:
============================

CHALLENGES IN NETWORK FILE TRANSFER:
- File size may exceed single packet capacity
- Network packets may be lost or arrive out of order
- Different systems may have different file formats
- Network congestion can affect transfer speed
- Security concerns (authentication, encryption)

CHUNKING STRATEGY:
- Divide large files into smaller chunks
- Send chunks sequentially
- Include sequence numbers for ordering
- Implement acknowledgment mechanism
- Handle retransmission of lost chunks

ERROR HANDLING:
- Network timeouts
- Connection failures  
- File I/O errors
- Invalid addresses/ports
- Insufficient permissions

PERFORMANCE OPTIMIZATION:
========================

BUFFER SIZING:
- Larger buffers: Fewer system calls, higher memory usage
- Smaller buffers: More system calls, lower memory usage
- Optimal size depends on network conditions and available memory
- Common sizes: 1024, 4096, 8192 bytes

NETWORK EFFICIENCY:
- Minimize packet count (combine small messages)
- Use appropriate protocol (TCP vs UDP)
- Implement proper error handling
- Consider compression for large data
- Use asynchronous I/O for better concurrency

SECURITY CONSIDERATIONS:
=======================

NETWORK SECURITY THREATS:
- Packet interception (sniffing)
- Man-in-the-middle attacks
- Denial of Service (DoS)
- Port scanning
- Data tampering

MITIGATION STRATEGIES:
- Use encryption (SSL/TLS for TCP, DTLS for UDP)
- Implement authentication mechanisms
- Validate all input data
- Use firewalls and access controls
- Monitor network traffic for anomalies

JAVA NETWORKING BEST PRACTICES:
==============================

1. RESOURCE MANAGEMENT:
   - Always close sockets and streams
   - Use try-with-resources for automatic cleanup
   - Handle exceptions appropriately

2. THREAD SAFETY:
   - Use separate threads for server handling multiple clients
   - Synchronize access to shared resources
   - Consider thread pools for better performance

3. ERROR HANDLING:
   - Catch specific exceptions (IOException, SocketException)
   - Implement retry mechanisms for transient failures
   - Log errors for debugging purposes

4. PERFORMANCE:
   - Set appropriate socket timeouts
   - Use buffered streams for better performance
   - Consider non-blocking I/O (NIO) for high-performance applications

5. CONFIGURATION:
   - Make addresses and ports configurable
   - Allow adjustment of buffer sizes
   - Provide options for timeout values

COMMON NETWORK PROGRAMMING PITFALLS:
===================================

1. Not handling network failures gracefully
2. Blocking operations without timeouts
3. Not properly closing network resources
4. Ignoring thread safety in multi-threaded applications
5. Not validating input from network sources
6. Hardcoding network addresses and ports
7. Not considering network latency and bandwidth limitations
8. Insufficient error logging and monitoring

DEBUGGING NETWORK APPLICATIONS:
==============================

TOOLS AND TECHNIQUES:
- Wireshark: Packet capture and analysis
- netstat: Show network connections and statistics
- telnet: Test TCP connections manually
- ping: Test basic network connectivity
- Java debugging: Print statements, logging frameworks
- Network simulators: Test under various conditions

TESTING STRATEGIES:
- Unit tests for individual components
- Integration tests with actual network communication
- Load testing for performance under stress
- Error injection testing for failure scenarios
- Security testing for vulnerability assessment


PROTOCOL ANALYSIS:
=================

FILE TRANSFER PROTOCOL DESIGN:
1. Client sends filename as first packet
2. Server receives filename and creates output file
3. Client sends file data in chunks (packets)
4. Server receives and writes each chunk to file
5. Client sends "END" signal when complete
6. Server detects END signal and closes file

POTENTIAL ISSUES WITH THIS IMPLEMENTATION:
- No error checking for lost packets
- No sequence numbers (packets could arrive out of order)
- No acknowledgments (client doesn't know if server received data)
- No flow control (client might overwhelm server)
- No authentication or security measures
- Fixed buffer size may not be optimal for all scenarios

IMPROVEMENTS THAT COULD BE MADE:
- Add packet sequence numbers
- Implement acknowledgment system
- Add checksums for data integrity
- Include file size in initial packet
- Add timeout handling
- Implement retry mechanism for lost packets
- Add compression for large files
- Include authentication mechanism


/*
===================================================================================
                    DUPLICATED CODE WITH LINE-BY-LINE COMMENTS
===================================================================================
*/

// Line 1: Import all classes from java.io package for file input/output operations
import java.io.*;
// Line 2: Import all classes from java.net package for network communication
import java.net.*;

// Line 4: Declare a public class named UDPFileServer - must match filename
public class UDPFileServer {
    // Line 5: Main method - entry point where JVM starts program execution
    public static void main(String[] args) {
        // Line 6: Begin try block to handle potential exceptions during execution
        try {
            // Line 7: Create UDP socket bound to port 12347 for receiving packets
            DatagramSocket socket = new DatagramSocket(12347);
            // Line 8: Create byte array buffer of 4096 bytes to store incoming data
            byte[] buffer = new byte[4096];
            
            // Line 10: Comment indicating we receive filename first in protocol
            // Receive filename first
            // Line 11: Create DatagramPacket using buffer to receive incoming packet
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
            // Line 12: Block and wait for incoming packet, fills packet with received data
            socket.receive(packet);
            // Line 13: Convert received bytes to String, using exact length received
            String fileName = new String(packet.getData(), 0, packet.getLength());
            // Line 14: Print message showing which file we're receiving
            System.out.println("Receiving file: " + fileName);
            
            // Line 16: Create FileOutputStream to write received file data to disk
            FileOutputStream fos = new FileOutputStream("udp_received_" + fileName);
            
            // Line 18: Start infinite loop to receive file data packets
            while (true) {
                // Line 19: Create new DatagramPacket for each file chunk reception
                packet = new DatagramPacket(buffer, buffer.length);
                // Line 20: Receive next packet containing file data or END signal
                socket.receive(packet);
                // Line 21: Convert packet data to string to check for termination signal
                String msg = new String(packet.getData(), 0, packet.getLength());
                // Line 22: Check if received message is END signal, break loop if true
                if (msg.equals("END")) break; // End of file signal
                // Line 23: Write received packet data to output file on disk
                fos.write(packet.getData(), 0, packet.getLength());
            }
            
            // Line 26: Close file output stream to ensure data is saved properly
            fos.close();
            // Line 27: Close UDP socket to release network resources and port
            socket.close();
            // Line 28: Print success message indicating file transfer completed
            System.out.println("File received successfully!");
        // Line 29: Catch any exception that occurs during execution
        } catch (Exception e) {
            // Line 30: Print complete stack trace of exception for debugging
            e.printStackTrace();
        }
    }
}