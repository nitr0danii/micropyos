import os # i use dis for 99% of this entire code
import network # crucial for wifi

def clear():
    for i in range(100):
        print(RESET+"\n")

def open(filename, mode):
    with open(filename, mode) as f:
        f.read()

def wifi_auto_connect():                                     ### I cant code so i let deepseek write this. Im stupid.
    if "wifi.dat" in os.listdir():
        with open("wifi.dat", "r") as f:
            for line in f:
                ssid, pw = line.strip().split(":")
                sta = network.WLAN(network.STA_IF)
                sta.active(1)
                sta.connect(ssid, pw)
                if sta.isconnected():  # Cancel on success
                    print("Connected with:", ssid)
                    break # break

try:
    wifi_auto_connect
except NameError:
    pass

### NOTES ###

# Maximal Size for OS is one full Megabyte
# MicroBoot.py is useless, main.py works without bootloader


### COLORS ###

BLUE = "\033[34m"
RESET = "\033[0m"
RED = "\033[31m"

### Minimised to save storage ###

ram_vars = {

}

clear()
print(BLUE+"Micro PyOS v1.1"+RESET)

### Commands ###

def ls():
    print(os.listdir())

def cd(path):
    os.chdir(path)

def rmdir(dirname):
    os.removedirs(dirname)

def mkdir(dirname):
    os.makedirs(dirname)

def rm(filename):
    os.remove(filename)

def cwd():
    print(os.getcwd())

def shutdown():
    exit()

def run(filename):
    with open(filename, "r") as f:
        exec(f.read())

def ramvars():
    print(ram_vars)

def addramvar(name, value):
    ram_vars[name] = value

def rmramvar(name):
    del ram_vars[name]

def readramvar(name):
    try:
        return ram_vars[name]
    except KeyError:
        print("RamVar not found")

def reboot():
    with open("main.py", "r") as f:
        exec(f.read())

def wifi_connect(ssid, pw):
    sta = network.WLAN(network.STA_IF)
    sta.active(1)
    sta.connect(ssid, pw)
    return sta.isconnected()

def wifi_ap_on(ssid="pyos-ap", pw=""):
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=pw)
    ap.active(1)

def save_networks(networks):  # Format: {"SSID1":"PW1", "SSID2":"PW2"}
    with open("wifi.dat", "w") as f:
        f.write("\n".join([f"{k}:{v}" for k,v in networks.items()]))

def load_networks():
    if "wifi.dat" in os.listdir():
        with open("wifi.dat", "r") as f:
            return dict(l.strip().split(":") for l in f.readlines())
    return {}

def install_update():
    print("THIS PIECE OF ABSOLUTE SHI TOOK ME 3 FRICKING HOURS AND IT STILL WONT WORK, FUCK UPDATES, YOU CAN INSTALL THEM MANUALLY IF YOU WANT, I FUCKING GIVE UP")
    print("edit: EVEN FRICKIN CHATGPT WONT MAKE IT WORK")

commands={"ls": ls,
    "cd": cd,
    "rmdir": rmdir,
    "mkdir": mkdir,
    "rm": rm,
    "clear": clear,
    "cwd": cwd,
    "shutdown" and "exit": shutdown,
    "run": run,
    "ramvars": ramvars,
    "setramvar": addramvar,
    "rmramvar": rmramvar,
    "readramvar": readramvar,
    "reboot": reboot,
    "wifi_connect": wifi_connect,
    "wifi_ap_on": wifi_ap_on,
    "save_networks": save_networks,
    "load_networks": load_networks,
    "update": install_update
    }

### shel ###

while True:
    user_input = input("# ").strip().split()
    if not user_input:
        continue
    command = user_input[0]
    args = user_input[1:]

    if command in commands:
            result = commands[command](*args)
            if result is not None:
                print(result)