import os

### Remove this file if you dont need it. Main.py can be executed without any bootloader. this shi is useless ###

for i in range(100):
    print("\n")

print("MicroBoot v1.1")
print("-----------------")
print(os.listdir())
file = input("Select File to boot: ")

with open(file, "r") as f:
    for i in range(100):
        print("\n")
    exec(f.read())