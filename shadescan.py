import socket
import requests
import socks
import os

from scapy.all import sr1,IP

PROXY = os.getenv('PROXY_IP')
PROXY_PORT = os.getenv('PROXY_PORT')
USER = os.getenv('MASQ_USER')
PASS = os.getenv('MASQ_PW')

def connect_direct(host, port, exploit, proto='TCP'):
    rx_data = ""
    full_data = ""
    buff = 1024
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) if proto == 'TCP' else socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, port))
    sock.sendall(exploit)
    while not len(rx_data) == 0:
        rx_data = sock.recv(buff)
        full_data += rx_data
    return full_data

def connect_proxy(host, port, exploit):
    rx_data = ""
    full_data = ""
    buff = 1024
    sock = socks.socksocket()
    sock.set_proxy(socks.SOCKS5, PROXY, PROXY_PORT, True, username=USER, password=PASS)
    sock.connect((host, port))
    sock.sendall(exploit)
    while not len(rx_data) == 0:
        rx_data = sock.recv(buff)
        full_data += rx_data
    return full_data

def create_payload():
    # Need to get around to this
    pass

def scap_scan(ip):
    # Add range scanning and custom layer 4 payloads
    packet = IP(dst=ip)
    ans, unans = sr1(packet)
    return ans

def proxy_check():
    print(connect_direct('https://icanhazip.com', 80, 'GET / HTTP/1.1 \r\n\r\n'))
    print(connect_proxy('https://icanhazip.com', 80, 'GET / HTTP/1.1 \r\n\r\n'))
    print(requests.get('https://icanhazip.com').raw)

if __name__ == '__main__':
    proxy_check()
