import socket
import struct

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

src = "192.168.50.59" 
dst = "142.250.65.238"
iphdr = bytes.fromhex("45000054962840004001e0b4")
iphdr += struct.pack("!BBBB", *[int(x) for x in src.split(".")])
iphdr += struct.pack("!BBBB", *[int(x) for x in dst.split(".")])
icmp_payload = bytes.fromhex("0800ec4b888c00013d9bec67000000009a500000000000001"
                            "01112131415161718191a1b1c1d1e1f202122232425262728"
                            "292a2b2c2d2e2f3031323334353637")

sock.sendto(iphdr + icmp_payload, (dst, 0))