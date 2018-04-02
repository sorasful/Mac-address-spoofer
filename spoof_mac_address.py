from scapy.config import conf
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp

import netifaces  # retrieves network interfaces easily


class Spoofer:
    """ Class used to perform actions like getting all the interfaces, find hosts, change mac address ..."""
    def __init__(self):
        interfaces = netifaces.interfaces()
        choosen_interface_num = eval(input(" On which interface would you like to find hosts ?\n {0} \n choose : "
                                 .format("\n".join([f"{i} - {iface}" for i, iface in enumerate(interfaces)]))))

        choosen_interface = interfaces[choosen_interface_num]
        self.interface = choosen_interface
        print(netifaces.ifaddresses(choosen_interface))
        iface_infos = netifaces.ifaddresses(choosen_interface)
        self.ips = "{0}/24".format(iface_infos[2][0]['addr'])  # scan all network

    def get_macs_and_ips(self):
        conf.verb = 0
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ips), timeout=2, iface=self.interface, inter=0.1)

        hosts = []
        for snd, rcv in ans:
            mac, ip = str(rcv.sprintf(r'%Ether.src%-%ARP.psrc%')).split('-')
            hosts.append((mac, ip))

        return hosts


if __name__ == "__main__":
    spoofer = Spoofer()
    print(spoofer.get_macs_and_ips())
