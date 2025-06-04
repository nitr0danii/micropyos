import os
if "update/" in os.listdir():
    try:
        os.rename("update/microboot.py", "microboot.py")
    except FileNotFoundError:
        try:
            os.rename("update/main.py", "main.py")
        except FileNotFoundError:
            try:
                os.rename("update/license.md", "license.md")
            except FileNotFoundError:
                try:
                    os.rename("update/bugs.md", "bugs.md")
                except FileNotFoundError:
                    input("Update finished! Press Enter to reboot...")
                    with open("main.py", "r") as f:
                        exec(f.read())