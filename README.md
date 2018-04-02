# Mac address spoofer

Requires Python3.6+

This tool allows you to change your mac address with one you found when scanning the network.
You can select on which interface you want to scan for hosts and then you can select which 
mac address you want to use. 


## Install dependencies

`pip install -r requirements.txt`


## Run it (preferably in virtualenv)

`python3.6 spoof_mac_address.py`

For me, I need to use sudo because I have a permission denied, but I use virtualenv, so
when I sudo I loose my virtualenv. In case you have the same trouble, I do the following :

`sudo ./venv/bin/python3.6 spoof_mac_address.py`


## N.B :

Modifying mac address is a volatile action, so it will be changed until the next reboot.

