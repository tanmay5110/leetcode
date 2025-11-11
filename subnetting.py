import ipaddress

def validate_ip(ip):
    """Validates if the IP address is properly formatted."""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def identify_class(ip):
    """Identifies the class of an IPv4 address."""
    if not validate_ip(ip):
        return 'Invalid IP'
    
    try:
        first_octet = int(ip.split('.')[0])
        if 1 <= first_octet <= 126:
            return 'A'
        elif 128 <= first_octet <= 191:
            return 'B'
        elif 192 <= first_octet <= 223:
            return 'C'
        elif 224 <= first_octet <= 239:
            return 'D (Multicast)'
        elif 240 <= first_octet <= 254:
            return 'E (Experimental)'
        else:
            return 'Invalid IP'
    except (ValueError, IndexError):
        return 'Invalid IP'

def default_subnet_mask(ip_class):
    """Returns the default subnet mask and CIDR prefix for a given IP class."""
    if ip_class == 'A':
        return '255.0.0.0', 8
    elif ip_class == 'B':
        return '255.255.0.0', 16
    elif ip_class == 'C':
        return '255.255.255.0', 24
    else:
        return None, None

def calculate_network_address(ip, prefix):
    """Calculate the network address for given IP and prefix."""
    try:
        network = ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)
        return str(network.network_address)
    except:
        return ip

def display_subnet_ranges(network_ip, new_prefix, total_subnets, ips_per_subnet):
    """Display the first few subnet ranges."""
    try:
        base_network = ipaddress.IPv4Network(f"{network_ip}/{new_prefix}", strict=False)
        print(f"First few subnet ranges:")
        print("-" * 50)
        
        # Show first 5 subnets or all if less than 5
        subnets_to_show = min(5, total_subnets)
        
        for i in range(subnets_to_show):
            subnet_start = int(base_network.network_address) + (i * ips_per_subnet)
            subnet_end = subnet_start + ips_per_subnet - 1
            
            start_ip = ipaddress.IPv4Address(subnet_start)
            end_ip = ipaddress.IPv4Address(subnet_end)
            network_addr = start_ip
            broadcast_addr = end_ip
            first_host = ipaddress.IPv4Address(subnet_start + 1)
            last_host = ipaddress.IPv4Address(subnet_end - 1)
            
            print(f"Subnet {i+1}: {network_addr}/{new_prefix}")
            print(f"  Range: {start_ip} - {end_ip}")
            print(f"  Network: {network_addr}")
            print(f"  Broadcast: {broadcast_addr}")
            print(f"  Host range: {first_host} - {last_host}")
            print()
        
        if total_subnets > 5:
            print(f"... and {total_subnets - 5} more subnets")
            
    except Exception as e:
        print(f"Could not calculate subnet ranges: {e}")

def subnetting(ip, new_prefix):
    """Performs subnetting calculations based on a target CIDR prefix."""
    ip_class = identify_class(ip)
    if ip_class not in ['A', 'B', 'C']:
        print(f"Subnetting is not applicable for IP Class {ip_class}.")
        return
    
    default_mask, default_prefix = default_subnet_mask(ip_class)
    if not (default_prefix < new_prefix <= 30):
        print(f"\nError: Invalid CIDR prefix /{new_prefix} for a Class {ip_class} network (default /{default_prefix}).")
        print(f"The new prefix must be between /{default_prefix + 1} and /30.")
        return
    
    n_borrowed_bits = new_prefix - default_prefix
    mask_binary = '1' * new_prefix + '0' * (32 - new_prefix)
    mask_octets = [int(mask_binary[i:i+8], 2) for i in range(0, 32, 8)]
    new_subnet_mask_str = ".".join(map(str, mask_octets))
    
    total_subnets = 2 ** n_borrowed_bits
    ips_per_subnet = 2 ** (32 - new_prefix)
    assignable_hosts = ips_per_subnet - 2
    
    # Calculate actual network address
    network_ip = calculate_network_address(ip, new_prefix)
    
    print(f"\n{'='*60}")
    print(f"SUBNETTING CALCULATION RESULTS")
    print(f"{'='*60}")
    print(f"Original IP Address: {ip}")
    print(f"Network Address: {network_ip}")
    print(f"IP Class: {ip_class}")
    print(f"Default Subnet Mask: {default_mask} (/{default_prefix})")
    print(f"New CIDR Prefix: /{new_prefix}")
    print(f"New Subnet Mask: {new_subnet_mask_str}")
    print(f"Subnet Mask (Binary): {mask_binary[:8]}.{mask_binary[8:16]}.{mask_binary[16:24]}.{mask_binary[24:32]}")
    print(f"Bits Borrowed from Host: {n_borrowed_bits}")
    print(f"Total Subnets Created: {total_subnets}")
    print(f"Total IP Addresses per Subnet: {ips_per_subnet}")
    print(f"Assignable Hosts per Subnet: {assignable_hosts}")
    print(f"{'='*60}\n")
    
    # Display subnet ranges
    if total_subnets <= 20:  # Only show ranges for reasonable number of subnets
        display_subnet_ranges(network_ip, new_prefix, total_subnets, ips_per_subnet)

def interactive_menu():
    """Interactive menu for subnetting operations."""
    while True:
        print("\n" + "="*50)
        print("SUBNET CALCULATOR")
        print("="*50)
        print("1. Calculate Subnetting")
        print("2. Show IP Class Information") 
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            ip_address = input("Enter an IP address (e.g., 192.168.1.0): ").strip()
            cidr_input = input("Enter the new CIDR prefix (e.g., /26): ").strip()
            
            try:
                if not cidr_input.startswith('/'):
                    raise ValueError("CIDR prefix must start with '/'.")
                new_prefix_val = int(cidr_input[1:])
                if not (0 <= new_prefix_val <= 32):
                    raise ValueError("CIDR prefix value must be between 0 and 32.")
                
                subnetting(ip_address, new_prefix_val)
            except ValueError as e:
                print(f"\nInvalid input: {e}")
            except Exception as e:
                print(f"\nAn unexpected error occurred: {e}")
                
        elif choice == "2":
            ip_address = input("Enter an IP address: ").strip()
            ip_class = identify_class(ip_address)
            if ip_class in ['A', 'B', 'C']:
                mask, prefix = default_subnet_mask(ip_class)
                print(f"\nIP Address: {ip_address}")
                print(f"Class: {ip_class}")
                print(f"Default Subnet Mask: {mask} (/{prefix})")
            else:
                print(f"IP Class: {ip_class}")
                
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    # Check if user wants interactive mode or single calculation
    print("Welcome to the Subnet Calculator!")
    mode = input("Choose mode - (1) Single calculation (2) Interactive menu: ").strip()
    
    if mode == "2":
        interactive_menu()
    else:
        # Original single calculation mode
        ip_address = input("Enter an IP address (e.g., 172.16.0.0): ")
        cidr_input = input("Enter the new CIDR prefix (e.g., /22): ")
        
        try:
            if not cidr_input.startswith('/'):
                raise ValueError("CIDR prefix must start with '/'.")
            new_prefix_val = int(cidr_input[1:])
            if not (0 <= new_prefix_val <= 32):
                raise ValueError("CIDR prefix value must be between 0 and 32.")
            
            subnetting(ip_address, new_prefix_val)
        except ValueError as e:
            print(f"\nInvalid input: {e}")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

"""
================================================================================
                        ORIGINAL CODE (UNTOUCHED)
================================================================================
"""

def identify_class_original(ip):
    """Identifies the class of an IPv4 address."""
    try:
        first_octet = int(ip.split('.')[0])
        if 1 <= first_octet <= 126:
            return 'A'
        elif 128 <= first_octet <= 191:
            return 'B'
        elif 192 <= first_octet <= 223:
            return 'C'
        elif 224 <= first_octet <= 239:
            return 'D (Multicast)'
        elif 240 <= first_octet <= 254:
            return 'E (Experimental)'
        else:
            return 'Invalid IP'
    except (ValueError, IndexError):
        return 'Invalid IP'

def default_subnet_mask_original(ip_class):
    """Returns the default subnet mask and CIDR prefix for a given IP class."""
    if ip_class == 'A':
        return '255.0.0.0', 8
    elif ip_class == 'B':
        return '255.255.0.0', 16
    elif ip_class == 'C':
        return '255.255.255.0', 24
    else:
        return None, None

def subnetting_original(ip, new_prefix):
    """Performs subnetting calculations based on a target CIDR prefix."""
    ip_class = identify_class_original(ip)
    if ip_class not in ['A', 'B', 'C']:
        print(f"Subnetting is not applicable for IP Class {ip_class}.")
        return
    
    default_mask, default_prefix = default_subnet_mask_original(ip_class)
    if not (default_prefix < new_prefix <= 30):
        print(f"\nError: Invalid CIDR prefix /{new_prefix} for a Class {ip_class} network (default /{default_prefix}).")
        print(f"The new prefix must be between /{default_prefix + 1} and /30.")
        return
    
    n_borrowed_bits = new_prefix - default_prefix
    mask_binary = '1' * new_prefix + '0' * (32 - new_prefix)
    mask_octets = [int(mask_binary[i:i+8], 2) for i in range(0, 32, 8)]
    new_subnet_mask_str = ".".join(map(str, mask_octets))
    
    total_subnets = 2 ** n_borrowed_bits
    ips_per_subnet = 2 ** (32 - new_prefix)
    assignable_hosts = ips_per_subnet - 2
    
    print(f"\nIP Address: {ip}")
    print(f"Class: {ip_class}")
    print(f"Default Subnet Mask: {default_mask} (/{default_prefix})")
    print(f"Target CIDR Prefix: /{new_prefix}")
    print(f"New Subnet Mask: {new_subnet_mask_str}")
    print(f"Bits Borrowed: {n_borrowed_bits}")
    print(f"Total Subnets Created: {total_subnets}")
    print(f"Total IP Addresses per Subnet: {ips_per_subnet}")
    print(f"Assignable Hosts per Subnet: {assignable_hosts}\n")

"""
================================================================================
                    LINE-BY-LINE EXPLANATION WITH THEORY
================================================================================

NETWORKING THEORY AND CONCEPTS USED:
-----------------------------------

1. IPv4 ADDRESSING CONCEPTS:
   - IPv4 uses 32-bit addresses written in dotted decimal notation (x.x.x.x)
   - Each octet represents 8 bits, ranging from 0-255
   - IP addresses are divided into Network and Host portions

2. IP ADDRESS CLASSES (Classful Addressing):
   - Class A: 1.0.0.0 to 126.255.255.255 (Default mask: /8 or 255.0.0.0)
   - Class B: 128.0.0.0 to 191.255.255.255 (Default mask: /16 or 255.255.0.0)
   - Class C: 192.0.0.0 to 223.255.255.255 (Default mask: /24 or 255.255.255.0)
   - Class D: 224.0.0.0 to 239.255.255.255 (Multicast)
   - Class E: 240.0.0.0 to 254.255.255.255 (Experimental)

3. SUBNET MASKING:
   - Subnet masks determine which portion is network vs host
   - Binary representation: 1s for network bits, 0s for host bits
   - CIDR notation: /n where n is the number of network bits

4. SUBNETTING MATHEMATICS:
   - Borrowed bits from host portion create subnets
   - Number of subnets = 2^(borrowed bits)
   - Hosts per subnet = 2^(remaining host bits) - 2
   - Subtract 2 for network and broadcast addresses

LINE-BY-LINE EXPLANATION:
========================

def identify_class_original(ip):
    # PURPOSE: Determines the class of an IPv4 address based on first octet
    # THEORY: Uses classful addressing scheme defined by RFC 791
    
    try:
        # EXPLANATION: Exception handling for invalid input
        # WHY: Prevents program crashes from malformed IP addresses
        
        first_octet = int(ip.split('.')[0])
        # LINE BREAKDOWN:
        # - ip.split('.') → Splits IP string by dots into list ['192', '168', '1', '0']
        # - [0] → Gets first element (first octet as string)
        # - int() → Converts string to integer for numerical comparison
        # THEORY: First octet determines class in classful addressing
        
        if 1 <= first_octet <= 126:
            return 'A'
        # EXPLANATION: Class A range check
        # THEORY: Class A networks use first 8 bits for network, 24 for hosts
        # MATH: 2^24 = 16,777,216 hosts per network (minus network/broadcast)
        # WHY: Large organizations need many hosts per network
        
        elif 128 <= first_octet <= 191:
            return 'B'
        # EXPLANATION: Class B range check  
        # THEORY: Class B uses 16 bits network, 16 bits host
        # MATH: 2^16 = 65,536 hosts per network
        # WHY: Medium organizations balancing networks vs hosts
        
        elif 192 <= first_octet <= 223:
            return 'C'
        # EXPLANATION: Class C range check
        # THEORY: Class C uses 24 bits network, 8 bits host  
        # MATH: 2^8 = 256 addresses (254 usable hosts)
        # WHY: Small networks, most common for LANs
        
        elif 224 <= first_octet <= 239:
            return 'D (Multicast)'
        # EXPLANATION: Multicast address range
        # THEORY: Used for one-to-many communication
        # WHY: Efficient distribution to multiple receivers
        
        elif 240 <= first_octet <= 254:
            return 'E (Experimental)'
        # EXPLANATION: Reserved for future use/research
        # THEORY: RFC 1112 reserves this range
        # WHY: Allows protocol evolution without conflicts
        
        else:
            return 'Invalid IP'
        # EXPLANATION: Catches addresses outside valid ranges (0, 127, 255)
        # THEORY: 0.x.x.x is "this network", 127.x.x.x is loopback
        
    except (ValueError, IndexError):
        return 'Invalid IP'
        # EXPLANATION: Handles conversion errors and malformed IPs
        # ValueError: Non-numeric octets
        # IndexError: Missing octets (e.g., "192.168")

def default_subnet_mask_original(ip_class):
    # PURPOSE: Returns default subnet mask for each IP class
    # THEORY: Based on classful addressing standards
    
    if ip_class == 'A':
        return '255.0.0.0', 8
        # EXPLANATION: Class A default mask
        # BINARY: 11111111.00000000.00000000.00000000
        # THEORY: 8 network bits, 24 host bits
        # MATH: Network portion = first octet only
        
    elif ip_class == 'B':
        return '255.255.0.0', 16
        # EXPLANATION: Class B default mask
        # BINARY: 11111111.11111111.00000000.00000000  
        # THEORY: 16 network bits, 16 host bits
        # MATH: Network portion = first two octets
        
    elif ip_class == 'C':
        return '255.255.255.0', 24
        # EXPLANATION: Class C default mask
        # BINARY: 11111111.11111111.11111111.00000000
        # THEORY: 24 network bits, 8 host bits
        # MATH: Network portion = first three octets
        
    else:
        return None, None
        # EXPLANATION: No default masks for Class D/E or invalid IPs
        # WHY: These classes don't use traditional subnetting

def subnetting_original(ip, new_prefix):
    # PURPOSE: Main subnetting calculation function
    # THEORY: Implements Variable Length Subnet Masking (VLSM)
    
    ip_class = identify_class_original(ip)
    # EXPLANATION: Determine IP class first
    # WHY: Needed for default mask and validation
    
    if ip_class not in ['A', 'B', 'C']:
        print(f"Subnetting is not applicable for IP Class {ip_class}.")
        return
    # EXPLANATION: Only unicast classes support subnetting
    # THEORY: Multicast/experimental don't use subnet masks
    
    default_mask, default_prefix = default_subnet_mask_original(ip_class)
    # EXPLANATION: Get the natural/default subnet information
    # WHY: Needed as baseline for subnet calculations
    
    if not (default_prefix < new_prefix <= 30):
        # EXPLANATION: Validate new prefix is logical
        # THEORY: Must borrow at least 1 bit, leave at least 2 for hosts
        # MATH: /30 leaves 2 host bits = 4 addresses (2 usable)
        # WHY: /31 and /32 are special cases not covered here
        
        print(f"\nError: Invalid CIDR prefix /{new_prefix} for a Class {ip_class} network (default /{default_prefix}).")
        print(f"The new prefix must be between /{default_prefix + 1} and /30.")
        return
    
    n_borrowed_bits = new_prefix - default_prefix
    # EXPLANATION: Calculate how many host bits we're borrowing
    # THEORY: Borrowed bits become subnet bits
    # EXAMPLE: Class C (/24) to /26 borrows 2 bits
    # MATH: 26 - 24 = 2 borrowed bits
    
    mask_binary = '1' * new_prefix + '0' * (32 - new_prefix)
    # EXPLANATION: Create binary representation of new subnet mask
    # THEORY: Subnet mask is continuous 1s followed by continuous 0s
    # EXAMPLE: /26 = 11111111111111111111111111000000 (26 ones, 6 zeros)
    # WHY: 1s identify network portion, 0s identify host portion
    
    mask_octets = [int(mask_binary[i:i+8], 2) for i in range(0, 32, 8)]
    # LINE BREAKDOWN:
    # - range(0, 32, 8) → Creates [0, 8, 16, 24] for octet positions
    # - mask_binary[i:i+8] → Extracts 8-bit chunks
    # - int(..., 2) → Converts binary string to decimal
    # - List comprehension creates 4 decimal values
    # EXAMPLE: '11111111111111111111111111000000' becomes [255, 255, 255, 192]
    
    new_subnet_mask_str = ".".join(map(str, mask_octets))
    # EXPLANATION: Convert decimal octets to dotted decimal notation
    # THEORY: Standard IPv4 address representation
    # EXAMPLE: [255, 255, 255, 192] becomes "255.255.255.192"
    
    total_subnets = 2 ** n_borrowed_bits
    # EXPLANATION: Calculate number of subnets created
    # THEORY: Each borrowed bit doubles the number of subnets
    # MATH: 2^n where n = borrowed bits
    # EXAMPLE: 2 borrowed bits = 2^2 = 4 subnets
    
    ips_per_subnet = 2 ** (32 - new_prefix)
    # EXPLANATION: Calculate total IP addresses in each subnet
    # THEORY: Host bits determine subnet size
    # MATH: 2^h where h = host bits remaining
    # EXAMPLE: /26 has 6 host bits = 2^6 = 64 addresses
    
    assignable_hosts = ips_per_subnet - 2
    # EXPLANATION: Subtract network and broadcast addresses
    # THEORY: First IP is network address, last IP is broadcast
    # WHY: These addresses cannot be assigned to hosts
    # EXAMPLE: 64 total - 2 reserved = 62 assignable hosts

MATHEMATICAL FORMULAS USED:
==========================

1. SUBNETS CALCULATION:
   Number of Subnets = 2^(Borrowed Bits)
   Where: Borrowed Bits = New Prefix - Default Prefix

2. HOSTS PER SUBNET:
   Total IPs per Subnet = 2^(Host Bits)
   Assignable Hosts = 2^(Host Bits) - 2
   Where: Host Bits = 32 - New Prefix

3. SUBNET MASK CONVERSION:
   Binary: '1' * Prefix Length + '0' * (32 - Prefix Length)
   Decimal: Convert each 8-bit group to decimal

4. ADDRESS RANGES:
   Network Address = IP AND Subnet Mask
   Broadcast Address = Network Address + (2^Host Bits - 1)
   First Host = Network Address + 1
   Last Host = Broadcast Address - 1

NETWORKING CONCEPTS DEMONSTRATED:
===============================

1. CLASSFUL vs CLASSLESS ADDRESSING:
   - Original classful system (Classes A, B, C)
   - Modern CIDR (Classless Inter-Domain Routing)
   - Variable Length Subnet Masking (VLSM)

2. BINARY MATHEMATICS:
   - Base-2 number system for network calculations
   - Bitwise operations (AND, OR)
   - Powers of 2 for subnet/host calculations

3. NETWORK HIERARCHY:
   - Network portion (identifies subnet)
   - Host portion (identifies device within subnet)
   - Subnet boundaries and broadcast domains

4. ADDRESS CONSERVATION:
   - Efficient use of IP address space
   - Subnetting prevents address waste
   - Allows logical network segmentation

PRACTICAL APPLICATIONS:
======================

1. NETWORK DESIGN:
   - Dividing large networks into manageable subnets
   - Separating departments/functions
   - Implementing security boundaries

2. ROUTING EFFICIENCY:
   - Reducing routing table size
   - Implementing route summarization
   - Optimizing network performance

3. TROUBLESHOOTING:
   - Understanding network boundaries
   - Identifying connectivity issues
   - Validating network configurations

CROSS-EXAMINATION QUESTIONS:
===========================

Q1: Why do we subtract 2 from total IPs to get assignable hosts?
A1: Because the first IP is the network address (identifies the subnet itself) 
    and the last IP is the broadcast address (used for broadcast communication).
    Neither can be assigned to individual hosts.

Q2: What happens if we try to subnet a Class D or E address?
A2: The program correctly rejects this because Class D is for multicast 
    (one-to-many communication) and Class E is experimental. These don't 
    use traditional subnet masks.

Q3: Why is the maximum prefix limited to /30?
A3: A /30 network has only 2 host bits (2^2 = 4 addresses). After subtracting
    network and broadcast addresses, only 2 addresses remain for hosts.
    This is the minimum practical subnet size for point-to-point links.

Q4: How does borrowing bits affect network capacity?
A4: Each borrowed bit doubles the number of subnets but halves the number
    of hosts per subnet. It's a trade-off between network segmentation
    and host capacity.

Q5: What's the difference between /24 and 255.255.255.0?
A5: They represent the same subnet mask in different notations:
    - /24 is CIDR notation (24 network bits)
    - 255.255.255.0 is dotted decimal notation
    - Both mean 24 ones followed by 8 zeros in binary

ADVANCED CONCEPTS:
=================

1. SUBNETTING STRATEGIES:
   - Fixed Length Subnet Masking (FLSM)
   - Variable Length Subnet Masking (VLSM)
   - Supernetting (route aggregation)

2. MODERN IMPLEMENTATIONS:
   - IPv6 addressing (128-bit addresses)
   - Network Address Translation (NAT)
   - Dynamic Host Configuration Protocol (DHCP)

3. SECURITY IMPLICATIONS:
   - Broadcast domain isolation
   - Network segmentation for security
   - VLAN implementation support
"""


