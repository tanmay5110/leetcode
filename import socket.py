import socket

# Method: URL -> IP
def url_to_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "Invalid domain name"

# Method: IP -> URL
def ip_to_url(ip):
    try:
        return socket.gethostbyaddr(ip)[0]  # [0] = hostname
    except socket.herror:
        return "Invalid IP address"

# Main loop
while True:
    print("\nChoose an option:")
    print("1. IP to URL")
    print("2. URL to IP")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")
    
    if choice == "1":
        ip = input("Enter IP address: ")
        print("URL:", ip_to_url(ip))
    elif choice == "2":
        domain = input("Enter domain name: ")
        print("IP:", url_to_ip(domain))
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid choice, try again.")








"""


Choose an option:
1. IP to URL
2. URL to IP
3. Exit
Enter your choice (1/2/3): 2
Enter domain name: google.com
IP: 142.250.67.206

Choose an option:
1. IP to URL
2. URL to IP
3. Exit
Enter your choice (1/2/3): 1
Enter IP address: 142.250.67.206
URL: bom12s08-in-f14.1e100.net




"""













































"""
===================================================================================
                    COMMENTED VERSION WITH DETAILED EXPLANATIONS
===================================================================================
"""

# Import the socket module - Python's built-in networking library that provides
# functions for DNS lookups, creating network connections, and handling network protocols
import socket

# Define a function to convert domain names to IP addresses (Forward DNS Lookup)
# Parameter: domain - a string containing the domain name (e.g., "google.com")
# Returns: IP address as string or error message
def url_to_ip(domain):
    # Start error handling block - if DNS lookup fails, we catch the exception
    try:
        # socket.gethostbyname() performs forward DNS resolution
        # It contacts DNS servers to find the IP address associated with the domain
        # Example: gethostbyname("google.com") returns "142.250.67.206"
        return socket.gethostbyname(domain)
    # Catch gaierror (Get Address Info Error) - occurs when domain is invalid/non-existent
    # gaierror is raised when DNS resolution fails (domain doesn't exist, network issues)
    except socket.gaierror:
        # Return user-friendly error message instead of crashing the program
        return "Invalid domain name"

# Define a function to convert IP addresses to hostnames (Reverse DNS Lookup)
# Parameter: ip - a string containing the IP address (e.g., "8.8.8.8")
# Returns: hostname as string or error message
def ip_to_url(ip):
    # Start error handling for reverse DNS lookup
    try:
        # socket.gethostbyaddr() performs reverse DNS resolution
        # Returns a tuple: (hostname, aliaslist, ipaddrlist)
        # [0] extracts just the hostname from the tuple
        # Example: gethostbyaddr("8.8.8.8") returns ("dns.google", [], ["8.8.8.8"])
        return socket.gethostbyaddr(ip)[0]  # [0] = hostname from the returned tuple
    # Catch herror (Host Error) - occurs when IP is invalid or has no reverse DNS record
    # herror is raised when reverse DNS fails (invalid IP, no PTR record)
    except socket.herror:
        # Return error message for invalid IP addresses
        return "Invalid IP address"

# Main program loop - creates an interactive menu system
# while True creates an infinite loop that runs until explicitly broken
while True:
    # Print menu header with newline (\n) for better formatting
    print("\nChoose an option:")
    
    # Display menu options - each print statement shows a different choice
    print("1. IP to URL")    # Option to convert IP address to hostname
    print("2. URL to IP")    # Option to convert domain name to IP address  
    print("3. Exit")         # Option to quit the program
    
    # Get user input and store in 'choice' variable
    # input() displays prompt and waits for user to type and press Enter
    # Always returns a string, even if user types numbers
    choice = input("Enter your choice (1/2/3): ")
    
    # Check if user selected option 1 (IP to URL conversion)
    # Note: we compare with string "1", not integer 1
    if choice == "1":
        # Prompt user to enter an IP address
        # Store their input in the 'ip' variable as a string
        ip = input("Enter IP address: ")
        
        # Call our ip_to_url function with user's input
        # Print "URL:" followed by the result (either hostname or error message)
        print("URL:", ip_to_url(ip))
    
    # elif means "else if" - check if user selected option 2
    # Only executes if the previous if condition was false
    elif choice == "2":
        # Prompt user to enter a domain name
        # Store their input in the 'domain' variable
        domain = input("Enter domain name: ")
        
        # Call our url_to_ip function with user's domain input
        # Print "IP:" followed by the result (either IP address or error message)
        print("IP:", url_to_ip(domain))
    
    # Check if user wants to exit (selected option 3)
    elif choice == "3":
        # Print goodbye message
        print("Exiting...")
        
        # Break out of the while loop, which ends the program
        # Without this, the loop would continue forever
        break
    
    # Handle any other input that's not 1, 2, or 3
    else:
        # Print error message for invalid menu selection
        print("Invalid choice, try again.")
        # Program continues to loop and show menu again


"""
===================================================================================
                            POSSIBLE VIVA QUESTIONS AND ANSWERS
===================================================================================

Q1: What is the difference between forward and reverse DNS lookup?
A1: Forward DNS converts domain names to IP addresses (google.com → 142.250.67.206).
    Reverse DNS converts IP addresses to hostnames (8.8.8.8 → dns.google).
    Forward uses A records, reverse uses PTR records in DNS.

Q2: Why do we get different domain names when doing reverse lookup?
A2: Because reverse DNS returns the canonical hostname set by the server owner.
    Multiple domains can point to the same IP (virtual hosting), but reverse DNS
    returns only the primary hostname configured for that IP address.

Q3: What is the purpose of try-except blocks in this code?
A3: To handle DNS resolution errors gracefully without crashing the program.
    gaierror handles invalid domain names, herror handles invalid IP addresses.
    This provides user-friendly error messages instead of technical exceptions.

Q4: Explain the socket.gethostbyaddr() return value.
A4: It returns a tuple with 3 elements:
    - [0]: Primary hostname (what we use)
    - [1]: List of alias names for the host
    - [2]: List of IP addresses for the host
    We use [0] to extract just the hostname.

Q5: What happens if you enter an invalid IP address?
A5: The socket.gethostbyaddr() function raises a socket.herror exception,
    which our except block catches and returns "Invalid IP address" message.

Q6: Why do we use while True instead of for loop?
A6: Because we don't know how many iterations the user wants. while True creates
    an infinite menu loop that continues until the user chooses to exit (break).

Q7: What is the difference between gaierror and herror?
A7: gaierror (Get Address Info Error) occurs during forward DNS lookup failures.
    herror (Host Error) occurs during reverse DNS lookup failures.
    Both inherit from socket.error but handle different types of DNS failures.

Q8: How does DNS hierarchy work in domain resolution?
A8: 1. Query starts at root servers (.)
    2. Root redirects to TLD servers (.com, .org)
    3. TLD redirects to authoritative name servers
    4. Authoritative server returns the IP address
    5. Result is cached for future queries

Q9: What are some limitations of this program?
A9: - Only handles IPv4 addresses properly
    - No timeout handling for slow DNS queries  
    - No validation of input format
    - Doesn't handle multiple IP addresses for one domain
    - No support for IPv6 addresses

Q10: How could you improve this program?
A10: - Add input validation (regex for IP/domain format)
     - Implement timeout handling for DNS queries
     - Support IPv6 addresses
     - Add logging functionality
     - Handle multiple IP addresses per domain
     - Add DNS record type queries (MX, CNAME, etc.)

Q11: What is the significance of the .in-addr.arpa domain?
A11: It's a special domain used for reverse DNS lookups. IP addresses are reversed
     and appended with .in-addr.arpa. For example, 192.168.1.1 becomes
     1.1.168.192.in-addr.arpa for reverse lookup queries.

Q12: Why might some IP addresses not have reverse DNS records?
A12: - Network administrator hasn't configured PTR records
     - IP is from a dynamic range (ISP doesn't set reverse DNS)
     - Security reasons (some organizations don't publish reverse DNS)
     - IP is in a private network range (192.168.x.x, 10.x.x.x)

Q13: What is DNS caching and how does it affect this program?
A13: DNS responses are cached at multiple levels (OS, router, ISP) to improve
     performance. This means repeated queries might return cached results
     instead of fresh DNS lookups, which can be faster but potentially outdated.

Q14: How would you modify this program to handle multiple IP addresses?
A14: Use socket.getaddrinfo() instead of gethostbyname(), which returns all
     IP addresses. Then iterate through the results and display each one.

Q15: What security considerations should be made with DNS lookups?
A15: - DNS spoofing attacks can return fake IP addresses
     - Always validate and sanitize user input
     - Consider using secure DNS (DoH/DoT) for sensitive applications
     - Be aware that DNS queries can reveal browsing patterns
     - Some networks may log or monitor DNS requests

Q16: Explain the difference between hostname and FQDN.
A16: Hostname is just the machine name (e.g., "server1")
     FQDN (Fully Qualified Domain Name) includes the complete path 
     (e.g., "server1.example.com.") with trailing dot indicating root.

Q17: What would happen if we removed the [0] from gethostbyaddr(ip)?
A17: The function would return the complete tuple instead of just the hostname,
     printing something like: ('dns.google', [], ['8.8.8.8']) instead of 'dns.google'

Q18: How does this program handle network connectivity issues?
A18: Currently it doesn't explicitly handle network timeouts. The socket functions
     will eventually timeout and raise exceptions, but there's no custom timeout
     or retry logic implemented.

Q19: What is the maximum length of a domain name?
A19: 253 characters total, with each label (part between dots) maximum 63 characters.
     Only letters, numbers, and hyphens allowed. Must start/end with alphanumeric.

Q20: How would you test this program thoroughly?
A20: Test cases should include:
     - Valid domains (google.com, facebook.com)
     - Invalid domains (nonexistent.xyz, malformed names)
     - Valid IPs (8.8.8.8, 1.1.1.1)
     - Invalid IPs (999.999.999.999, malformed IPs)
     - Edge cases (localhost, private IPs)
     - Network timeout scenarios
"""

"""
===================================================================================
                    COMPREHENSIVE DNS THEORY AND SOCKET LIBRARY DETAILS
===================================================================================

DEEP DIVE INTO DNS (Domain Name System)
======================================

DNS ARCHITECTURE AND COMPONENTS:
-------------------------------
DNS is a distributed, hierarchical database system that translates human-readable
domain names into machine-readable IP addresses. It's one of the most critical
services on the Internet.

1. DNS NAMESPACE HIERARCHY:
   Root Level (.)
   ├── Top-Level Domains (TLD): .com, .org, .net, .edu, .gov, country codes
   │   ├── Second-Level Domains: google.com, microsoft.org
   │   │   ├── Subdomains: www.google.com, mail.google.com
   │   │   └── Further subdomains: docs.google.com, drive.google.com

2. DNS SERVER TYPES:
   a) ROOT SERVERS (13 worldwide):
      - Manage the root zone of DNS
      - Know where to find TLD servers
      - Names: a.root-servers.net to m.root-servers.net
      
   b) TLD SERVERS:
      - Manage top-level domains (.com, .org, etc.)
      - Know authoritative servers for each domain
      
   c) AUTHORITATIVE SERVERS:
      - Hold the actual DNS records for domains
      - Primary source of truth for domain information
      
   d) RECURSIVE RESOLVERS:
      - Your ISP's DNS servers
      - Query other servers on your behalf
      - Cache results to improve performance

DNS RECORD TYPES IN DETAIL:
--------------------------
A Record (Address): Maps domain to IPv4 address
  Example: google.com → 142.250.67.206

AAAA Record: Maps domain to IPv6 address  
  Example: google.com → 2607:f8b0:4004:c1b::65

CNAME (Canonical Name): Alias for another domain
  Example: www.example.com → example.com

MX (Mail Exchange): Mail server for domain
  Example: gmail.com → 10 alt1.gmail-smtp-in.l.google.com

PTR (Pointer): Reverse DNS - IP to hostname
  Example: 8.8.8.8 → dns.google

NS (Name Server): Authoritative servers for domain
  Example: google.com → ns1.google.com, ns2.google.com

TXT: Text records for verification, SPF, DKIM
  Example: "v=spf1 include:_spf.google.com ~all"

SOA (Start of Authority): Administrative info about domain
  Contains: primary server, admin email, serial number, timers

DNS RESOLUTION PROCESS (DETAILED):
---------------------------------
When you type "www.example.com" in browser:

Step 1: LOCAL CACHE CHECK
- Browser checks its DNS cache
- Operating system checks its DNS cache
- Router checks its DNS cache

Step 2: RECURSIVE RESOLVER QUERY
- If not cached, query goes to ISP's recursive resolver
- Resolver checks its own cache first

Step 3: ROOT SERVER QUERY (if needed)
- Resolver asks root server: "Who handles .com domains?"
- Root server responds: "Ask the .com TLD servers"
- Returns IP addresses of .com TLD servers

Step 4: TLD SERVER QUERY
- Resolver asks .com TLD server: "Who handles example.com?"
- TLD server responds: "Ask ns1.example.com (IP: x.x.x.x)"

Step 5: AUTHORITATIVE SERVER QUERY
- Resolver asks ns1.example.com: "What's the IP for www.example.com?"
- Authoritative server responds: "192.0.2.1"

Step 6: RESPONSE AND CACHING
- Resolver returns IP to your computer
- Result is cached at multiple levels for future use
- Your browser connects to 192.0.2.1

DNS CACHING MECHANISMS:
----------------------
TTL (Time To Live): How long to cache a DNS record
- Measured in seconds
- Set by domain owner in DNS records
- Common values: 300s (5min), 3600s (1hr), 86400s (24hr)

CACHE LEVELS:
1. Browser Cache: Typically 1-30 minutes
2. OS Cache: Usually respects TTL from DNS record  
3. Router Cache: Varies by router configuration
4. ISP Cache: Can be hours to days
5. Authoritative Cache: N/A (source of truth)

REVERSE DNS (PTR RECORDS) IN DEPTH:
----------------------------------
Reverse DNS uses a special domain: .in-addr.arpa for IPv4

PROCESS:
1. Take IP address: 192.168.1.100
2. Reverse the octets: 100.1.168.192
3. Append .in-addr.arpa: 100.1.168.192.in-addr.arpa
4. Query for PTR record at this domain

IPv6 REVERSE DNS:
Uses .ip6.arpa domain with hex digits reversed
Example: 2001:db8::1 becomes 1.0.0.0...0.8.b.d.0.1.0.0.2.ip6.arpa

WHY REVERSE DNS MATTERS:
- Email servers use it for spam filtering
- Security logging and forensics
- Network troubleshooting
- Compliance requirements

DNS SECURITY CONSIDERATIONS:
---------------------------
DNS SPOOFING/CACHE POISONING:
- Attacker injects fake DNS responses
- Redirects users to malicious sites
- Mitigation: DNSSEC, encrypted DNS

DNS HIJACKING:
- Changing DNS server settings
- Redirects all traffic through attacker's servers
- Common in malware and router attacks

DNS TUNNELING:
- Using DNS queries to exfiltrate data
- Bypasses firewall restrictions
- Detection requires DNS traffic analysis

DNSSEC (DNS Security Extensions):
- Cryptographically signs DNS records
- Prevents tampering and spoofing
- Uses public key cryptography

ENCRYPTED DNS PROTOCOLS:
- DNS over HTTPS (DoH): Port 443
- DNS over TLS (DoT): Port 853
- DNS over QUIC (DoQ): Newer protocol

===================================================================================
                        PYTHON SOCKET LIBRARY DEEP DIVE
===================================================================================

SOCKET LIBRARY ARCHITECTURE:
---------------------------
The Python socket module is a low-level networking interface that provides:
- BSD socket API wrapper
- Cross-platform networking functionality  
- Direct access to operating system socket calls

SOCKET TYPES:
1. SOCK_STREAM: TCP connections (reliable, ordered)
2. SOCK_DGRAM: UDP connections (fast, unreliable)
3. SOCK_RAW: Raw IP packets (requires privileges)

ADDRESS FAMILIES:
- AF_INET: IPv4 Internet protocols
- AF_INET6: IPv6 Internet protocols  
- AF_UNIX: Unix domain sockets (local)

DNS-RELATED FUNCTIONS IN SOCKET MODULE:
--------------------------------------

1. socket.gethostbyname(hostname):
   INTERNAL PROCESS:
   - Calls getaddrinfo() system call
   - Queries local DNS resolver
   - Returns first IPv4 address found
   - Raises gaierror if resolution fails
   
   LIMITATIONS:
   - Only returns one IP address
   - IPv4 only
   - Deprecated in favor of getaddrinfo()

2. socket.gethostbyaddr(ip_address):
   INTERNAL PROCESS:
   - Performs reverse DNS lookup
   - Constructs .in-addr.arpa domain
   - Queries for PTR record
   - Returns tuple: (hostname, aliases, ip_list)
   
   RETURN TUPLE BREAKDOWN:
   - [0] hostname: Primary canonical name
   - [1] aliases: List of alternative names
   - [2] ip_list: List of IP addresses for this host

3. socket.getaddrinfo(host, port, family, type, proto, flags):
   MODERN REPLACEMENT:
   - Handles both IPv4 and IPv6
   - Returns all available addresses
   - More flexible and robust
   - Used internally by higher-level functions

4. socket.getnameinfo(sockaddr, flags):
   REVERSE LOOKUP FUNCTION:
   - More flexible than gethostbyaddr()
   - Can return numeric addresses if no name found
   - Supports both IPv4 and IPv6

EXCEPTION HIERARCHY:
-------------------
socket.error (base exception)
├── socket.gaierror (getaddrinfo error)
│   ├── Name resolution failures
│   ├── Invalid hostname formats
│   └── Network unreachable errors
├── socket.herror (host error)  
│   ├── Reverse DNS failures
│   ├── Invalid IP addresses
│   └── No PTR record found
└── socket.timeout
    └── DNS query timeout

ERROR CODES AND MEANINGS:
------------------------
gaierror codes (from getaddrinfo):
- EAI_NONAME (-2): Name doesn't exist
- EAI_AGAIN (-3): Temporary failure, try again
- EAI_FAIL (-4): Non-recoverable failure
- EAI_FAMILY (-6): Address family not supported
- EAI_NODATA (-5): No address associated with name

herror codes (from gethostbyaddr):
- HOST_NOT_FOUND (1): Host name not found
- TRY_AGAIN (2): Temporary error, try again
- NO_RECOVERY (3): Non-recoverable error
- NO_DATA (4): Valid name, no data of requested type

SOCKET MODULE IMPLEMENTATION DETAILS:
------------------------------------

C LIBRARY INTEGRATION:
- Python socket module wraps C socket library
- Uses platform-specific resolver libraries
- On Linux: glibc resolver functions
- On Windows: Winsock API

THREAD SAFETY:
- Socket operations are thread-safe
- DNS lookups may block all Python threads
- Use socket.setdefaulttimeout() for timeouts
- Consider asyncio for non-blocking DNS

PERFORMANCE CONSIDERATIONS:
- DNS lookups are synchronous by default
- Can block for 30+ seconds on timeout
- Results depend on network conditions
- Local caching improves repeated lookups

PLATFORM DIFFERENCES:
- Windows: Uses Winsock, different error codes
- Linux/Unix: Uses BSD sockets, POSIX compliance  
- macOS: Similar to Linux but some differences
- Mobile platforms: May have restricted access

RESOLVER CONFIGURATION:
----------------------
The socket module uses system DNS configuration:

LINUX/UNIX (/etc/resolv.conf):
nameserver 8.8.8.8        # Primary DNS server
nameserver 8.8.4.4        # Secondary DNS server  
search example.com         # Default domain suffix
options timeout:2          # Query timeout
options attempts:3         # Retry attempts

WINDOWS (Registry):
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters
- NameServer: DNS server list
- SearchList: Domain search order

DNS RESOLVER BEHAVIOR:
---------------------
QUERY ORDER:
1. Check /etc/hosts file (static mappings)
2. Query configured DNS servers in order
3. Try search domains if unqualified name
4. Return first successful result

TIMEOUT BEHAVIOR:
- Default timeout varies by system (5-30 seconds)
- Retries failed queries automatically
- Falls back to next DNS server on failure

IPV6 CONSIDERATIONS:
-------------------
DUAL-STACK BEHAVIOR:
- Modern systems query both A and AAAA records
- IPv6 preferred if available (Happy Eyeballs)
- Fallback to IPv4 if IPv6 fails

SOCKET MODULE IPV6:
- AF_INET6 address family
- Uses getaddrinfo() for modern lookups  
- Returns IPv6 addresses in brackets: [::1]

ADVANCED SOCKET FEATURES:
------------------------
RAW SOCKETS:
- Direct IP packet manipulation
- Requires root/administrator privileges
- Used for ping, traceroute implementations

SOCKET OPTIONS:
- SO_REUSEADDR: Reuse address binding
- SO_KEEPALIVE: Keep connection alive
- SO_TIMEOUT: Set operation timeout

NON-BLOCKING SOCKETS:
- socket.setblocking(False)
- Returns immediately, may raise EAGAIN
- Used with select/poll for multiplexing

ALTERNATIVE DNS LIBRARIES:
-------------------------
For more advanced DNS operations:

1. dnspython (dns.resolver):
   - Pure Python DNS toolkit
   - Supports all record types
   - Advanced query options
   - Better error handling

2. aiodns (asyncio):
   - Asynchronous DNS resolution
   - Non-blocking operations
   - Better for high-performance applications

3. pycares:
   - Python wrapper for c-ares library
   - Asynchronous DNS resolution
   - Cross-platform support

DEBUGGING DNS ISSUES:
--------------------
COMMAND LINE TOOLS:
- nslookup: Basic DNS queries
- dig: Advanced DNS debugging  
- host: Simple hostname resolution
- ping: Test connectivity with DNS

PYTHON DEBUGGING:
import socket
socket.setdefaulttimeout(10)  # Set timeout
try:
    result = socket.gethostbyname('example.com')
    print(f"Success: {result}")
except socket.gaierror as e:
    print(f"DNS Error: {e}")
except Exception as e:
    print(f"Other Error: {e}")

NETWORK ANALYSIS:
- Wireshark: Packet capture and analysis
- tcpdump: Command-line packet capture
- netstat: Network connection status
- ss: Modern netstat replacement

BEST PRACTICES FOR DNS IN PYTHON:
---------------------------------
1. Always use try-except for DNS operations
2. Set appropriate timeouts for your use case
3. Cache results when appropriate to reduce load
4. Use getaddrinfo() for new applications
5. Handle both IPv4 and IPv6 addresses
6. Validate input before DNS queries
7. Consider using async libraries for high load
8. Log DNS errors for debugging
9. Test with various network conditions
10. Be aware of DNS security implications

COMMON PITFALLS:
---------------
- Assuming DNS always works (network failures)
- Not handling timeouts (hanging applications)
- Ignoring IPv6 (incomplete connectivity)  
- Not validating input (security issues)
- Blocking UI threads (poor user experience)
- Not caching results (poor performance)
- Hardcoding DNS servers (portability issues)
"""