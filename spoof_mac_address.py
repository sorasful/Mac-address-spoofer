from scapy.config import conf
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp


class Spoofer:

    def __init__(self, interface, ips):
        self.interface = interface
        self.ips = ips

    def get_macs_and_ips(self):
        conf.verb = 0
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ips), timeout=2, iface=self.interface, inter=0.1)

        hosts = []
        for snd, rcv in ans:
            mac, ip = str(rcv.sprintf(r'%Ether.src%-%ARP.psrc%')).split('-')
            hosts.append((mac, ip))

        return hosts

if __name__ == "__main__":
    spoofer = Spoofer(interface='wlan0', ips='192.168.1.0/24')
    spoofer.get_macs_and_ips()