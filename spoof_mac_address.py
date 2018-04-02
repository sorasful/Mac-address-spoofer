from scapy.config import conf
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp

import netifaces  # retrieves network interfaces easily

import subprocess

class Spoofer:
    """ Class used to perform actions like getting all the interfaces, find hosts, change mac address ..."""
    def __init__(self):
        interfaces = netifaces.interfaces()
        choosen_interface_num = eval(input(" On which interface would you like to find hosts ?\n {0} \n choose : "
                                 .format("\n".join([f"{i} - {iface}" for i, iface in enumerate(interfaces)]))))

        choosen_interface = interfaces[choosen_interface_num]
        self.interface = choosen_interface
        iface_infos = netifaces.ifaddresses(choosen_interface)
        self.ips = "{0}/24".format(iface_infos[2][0]['addr'])  # scan all network

    def get_hosts_macs_and_ips(self):
        conf.verb = 0
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ips), timeout=2, iface=self.interface, inter=0.1)

        hosts = []
        for snd, rcv in ans:
            mac, ip = str(rcv.sprintf(r'%Ether.src%-%ARP.psrc%')).split('-')
            hosts.append((mac, ip))

        return hosts

    def alter_mac_address(self, interface, mac_address):
        subprocess.run(f'ifconfig {interface} down', shell=True)
        subprocess.run(f'ifconfig {interface} hw ether {mac_address}', shell=True)
        subprocess.run(f'ifconfig {interface} up', shell=True)

        return True

    def change_current_mac_address(self):
        """ Show all availables mac addresses and ip and let user select which mac address he wants to use from now. """
        hosts = self.get_hosts_macs_and_ips()
        host_mac, _ = hosts[eval(input("Choose which mac address you want to use : \n{0}\n choose : "
                          .format("\n".join([f"{i} - {h[0]} - {h[1]}" for i, h in enumerate(hosts)]))))]

        self.alter_mac_address(self.interface, host_mac)

        print(f"Successfuly changed mac address to {host_mac}")

if __name__ == "__main__":
    spoofer = Spoofer()
    spoofer.change_current_mac_address()