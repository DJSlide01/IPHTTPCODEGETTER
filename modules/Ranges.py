import ipaddress
import socket

class IPRange:
    def __init__(self, start_ip, end_ip):
        self.start_ip = self._resolve_ip(start_ip)
        self.end_ip = self._resolve_ip(end_ip)

    def _resolve_ip(self, ip):
        try:
            ipaddress.IPv4Address(ip)  # Check if it's a valid IP address
            return ip
        except ipaddress.AddressValueError:
            try:
                resolved_ip = socket.gethostbyname(ip)  # Resolve the domain name to an IP address
                ipaddress.IPv4Address(resolved_ip)  # Check if the resolved IP address is valid
                return resolved_ip
            except (socket.gaierror, ipaddress.AddressValueError):
                raise ValueError(f"Invalid IP address or domain name: {ip}")

    def get_ip_range(self):
        start = ipaddress.IPv4Address(self.start_ip)
        end = ipaddress.IPv4Address(self.end_ip)
        ip_range = []
        for ip in range(int(start), int(end) + 1):
            ip_range.append(str(ipaddress.IPv4Address(ip)))
        return ip_range

class PortRange:
    def __init__(self, start_port, end_port):
        self.start_port = start_port
        self.end_port = end_port

    def get_port_range(self):
        return list(range(self.start_port, self.end_port + 1))
