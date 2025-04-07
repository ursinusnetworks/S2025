import socket
import struct

def get_checksum(bs):
    """
    Compute the internet checksum for some bytes

    Parameters
    ----------
    bs: list of bytes
        Bytes on which to compute the checksum
    """
    if len(bs) % 2 == 1:
        bs += bytes([0])
    shorts = struct.unpack("!" + "H"*(len(bs)//2), bs)
    c = 0
    for s in shorts:
        c = c + s
        if ( (c >> 16) & 0xffff) > 0:
            c = (c & 0xffff) + 1
    c = (~c) & 0xffff
    return c

src = "192.168.50.59" ## Change this to your IP address, then to something that's not your IP address
dst = "142.250.65.238"
iphdr1  = bytes.fromhex("45000054962840004001")
srcdst  = struct.pack("!BBBB", *[int(x) for x in src.split(".")])
srcdst += struct.pack("!BBBB", *[int(x) for x in dst.split(".")])
cksum = get_checksum(iphdr1 + srcdst)

iphdr = iphdr1 + struct.pack("!H", cksum) + srcdst

icmp_payload = bytes.fromhex("0800ec4b888c00013d9bec67000000009a500000000000001"
                            "01112131415161718191a1b1c1d1e1f202122232425262728"
                            "292a2b2c2d2e2f3031323334353637")

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
sock.sendto(iphdr + icmp_payload, (dst, 0))