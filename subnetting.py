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












"""""


  Range: 192.168.1.0 - 192.168.1.63
  Network: 192.168.1.0
  Broadcast: 192.168.1.63
  Host range: 192.168.1.1 - 192.168.1.62

Subnet 2: 192.168.1.64/26
  Range: 192.168.1.64 - 192.168.1.127
  Network: 192.168.1.64
  Broadcast: 192.168.1.127
  Host range: 192.168.1.65 - 192.168.1.126

Subnet 3: 192.168.1.128/26
  Range: 192.168.1.128 - 192.168.1.191
  Network: 192.168.1.128
  Broadcast: 192.168.1.191
  Host range: 192.168.1.129 - 192.168.1.190

Subnet 4: 192.168.1.192/26
  Range: 192.168.1.192 - 192.168.1.255
  Network: 192.168.1.192
  Broadcast: 192.168.1.255
  Host range: 192.168.1.193 - 192.168.1.254

"""


            