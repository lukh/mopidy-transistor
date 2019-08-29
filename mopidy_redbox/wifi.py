import os

def scan_networks(interface="wlan0"):
    command = """iwlist {} scan | grep -ioE 'SSID:"(.*)"'""".format(interface)
    result = os.popen(command)
    result = list(result)
    ssid_list = []

    if "Device or resource busy" not in result:
        ssid_list = [item.lstrip('SSID:').strip('"\n') for item in result]

    return [i for i in set(ssid_list) if i != ""]

def turn_on_ap():
    # need to turn on static ip in dhcpcd.conf...
    
    os.popen("sudo systemctl start dnsmasq")
    os.popen("sudo systemctl start hostap")
    
    os.popen("sudo dhcpcd --nohook wpa_supplicant -S ip_address=192.168.4.1/24 wlan0")