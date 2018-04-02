#!/usr/bin/env python
from scapy.config import conf
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp

import netifaces  # retrieves network interfaces easily

import subprocess
import sys

class Spoofer:
    """ Class used to perform actions like getting all the interfaces, find hosts, change mac address ..."""
    def __init__(self):
        """ Show interfaces and set interface to work on. """
        interfaces = netifaces.interfaces()  # Get all interfaces as a list of str
        choosen_interface_num = eval(input("On which interface would you like to find hosts ?\n"
                                            " {0} \n"
                                            " choose : "
                                            .format("\n".join([f"{i} - {iface}" for i, iface in enumerate(interfaces)]))))

        while not 0 <= choosen_interface_num < len(interfaces):
            choosen_interface_num = eval(input("Wrong selection !\n"
                                               "On which interface would you like to find hosts ?\n"
                                               " {0} \n"
                                               " choose : "
                                               .format("\n".join([f"{i} - {iface}" for i, iface in enumerate(interfaces)]))))

        choosen_interface = interfaces[choosen_interface_num]
        iface_infos = netifaces.ifaddresses(choosen_interface)

        try:
            self.interface = choosen_interface
            self.ips = "{0}/24".format(iface_infos[2][0]['addr'])  # scan all network
        except KeyError:
            print("Can't find network ip. Program will now exit.")
            sys.exit()

    def get_hosts_macs_and_ips(self):
        """
        Method used to get a list of tuple containing mac addresses and ips of each host present on the network in a specific interface.
        """
        conf.verb = 0
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.ips), timeout=2, iface=self.interface, inter=0.1)

        hosts = []
        for snd, rcv in ans:
            mac, ip = str(rcv.sprintf(r'%Ether.src%-%ARP.psrc%')).split('-')  # mac-ip
            hosts.append((mac, ip))

        return hosts

    def alter_mac_address(self, interface, mac_address):  # TODO : See how to make this work on windows
        """ Change mac address using. """
        subprocess.run(f'ifconfig {interface} down', shell=True)
        subprocess.run(f'ifconfig {interface} hw ether {mac_address}', shell=True)
        subprocess.run(f'ifconfig {interface} up', shell=True)

    def change_current_mac_address(self):
        """ Show all availables mac addresses and ip and let user select which mac address he wants to use from now. """
        hosts = self.get_hosts_macs_and_ips()
        host_mac, _ = hosts[eval(input("Choose which mac address you want to use :\n"
                                       "mac-address - ip on network\n"
                                       "----------------- \n"
                                       "{0}\n"
                                       " choose : "
                          .format("\n".join([f"{i} - {h[0]} - {h[1]}" for i, h in enumerate(hosts)]))))]

        self.alter_mac_address(self.interface, host_mac)

        print(f"Successfuly changed mac address to {host_mac}")


if __name__ == "__main__":
    spoofer = Spoofer()
    spoofer.change_current_mac_address()