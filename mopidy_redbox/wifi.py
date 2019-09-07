
import os

def scan_networks(interface="wlan0"):
    command = """iwlist {} scan | grep -ioE 'SSID:"(.*)"'""".format(interface)
    result = os.popen(command)
    result = list(result)
    ssid_list = []

    if "Device or resource busy" not in result:
        ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]

    return [i for i in set(ssid_list) if i != ""]


# pi@raspberrypi:~$ sudo systemctl start dhcpcd
# pi@raspberrypi:~$ sudo systemctl start dnsmasq
# pi@raspberrypi:~$ sudo systemctl start hostapd
#interface wlan0
#    static ip_address=192.168.4.1/24
#    nohook wpa_supplicant

def turn_on_ap():
    os.popen("sudo systemctl stop dhcpcd")

    os.popen("sudo cp /etc/dhcpcd.conf.source /etc/dhcpcd.conf")
    os.popen('sudo echo "interface wlan0" >> /etc/dhcpcd.conf')
    os.popen('sudo echo "    static ip_address=192.168.4.1/24" >> /etc/dhcpcd.conf')
    os.popen('sudo echo "    nohook wpa_supplicant" >> /etc/dhcpcd.conf')
    os.popen("sudo systemctl start dhcpcd")
    
    os.popen("sudo systemctl start dnsmasq")
    os.popen("sudo systemctl start hostapd")




def turn_off_ap():
    os.popen("sudo systemctl stop hostapd")
    os.popen("sudo systemctl stop dnsmasq")

    os.popen("ip addr flush dev wlan0")
    os.popen("ip link set dev wlan0 up")


    # dhcpcd  -n "$wifidev"
    os.popen("sudo systemctl stop dhcpcd")
    os.popen("sudo cp /etc/dhcpcd.conf.source /etc/dhcpcd.conf")
    # edit file dhcpcd remove wlan0 stuff
    os.popen("sudo systemctl start dhcpcd")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2):
        if sys.argv[1] == "on":
            turn_on_ap()

        else:
            turn_off_ap()
