1. Download Raspberry Pi Imager

2. Choose OS → Raspberry Pi OS Lite (64-bit)

3. Configure Wi-Fi (SSID, password, country).

4. Use cc and 1234

5. `sudo apt update && sudo apt upgrade -y`

6. Instalar chromium, terminal y openbox con los xorgs suficientes`sudo apt install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox chromium-browser xterm geany -y`

7. `mkdir -p ~/.config/openbox`

8. `nano ~/.config/openbox/autostart`

```nano
   xset -dpms
   xset s off
   xset s noblank

   chromium-browser --noerrdialogs --disable-infobars --kiosk http://10.0.0.2:7777/rasp/maquinas
```

9. `nano ~/.xinitrc`

   exec openbox-session

10. `sudo raspi-config`

    Enable autologin
    Set Spanish keyboard

11. `nano ~/.bash_profile`

```bash
    if [[-z $DISPLAY]] && [[$(tty) == /dev/tty1]]; then
        exec startx
    fi
```

12. Reboot and check openbox opens with the URL

13. Set keyboard shortcuts `nano ~/.config/openbox/rc.xml`

```XML
 <?xml version="1.0" encoding="UTF-8"?>

 <openbox_config>
 <keyboard>

     <!-- Ctrl+Alt+T to open terminal -->
     <keybind key="C-A-t">
     <action name="Execute">
         <command>xterm</command>
     </action>
     </keybind>

     <!-- Alt+F4 to close the focused window -->
     <keybind key="A-F4">
     <action name="Close"/>
     </keybind>

     <keybind key="A-F6">
        <action name="Execute">
            <command>bash -c "pkill chromium; sudo shutdown -h now"</command>
        </action>
    </keybind>

 </keyboard>
 </openbox_config>
```

14. Apply changes `openbox --reconfigure`

### Set up print + apache2

15. Check python is installed

16. Copy rasp content into ~/rasp/ and edit to match route URL: https://github.com/informatica-cc/rasp/blob/main/app.py

17. `python3 -m venv venv`

18. `pip install -r requirements.txt`

19. `/home/cc/rasp/venv/bin/python /home/cc/rasp/app.py`

20. Check it works in localhost:5000

21. `sudo nano /etc/systemd/system/epos-print.service`

```Nano
[Unit]
Description=EPOS Print Service
After=network.target

[Service]
User=cc
WorkingDirectory=/home/cc/rasp
ExecStart=/home/cc/rasp/venv/bin/gunicorn -w 2 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

22. Enable service

```Bash
sudo systemctl daemon-reload
sudo systemctl enable epos-print
sudo systemctl start epos-print
sudo systemctl status epos-print
```

23. Plug printer

24. `lsusb`
    Coger la dirección de la epson, parecida a esta: 0x04b8,0x0202

25. `sudo nano /lib/udev/rules.d/99-myusb.rules`
    SUBSYSTEMS=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0e15", MODE="0666"

idVendor e idProduct con lo que corresponde (sin el 0x)

Añadirlo tb al programa app.py de dentro de la carpeta /rasp

30. `sudo udevadm control --reload-rules`

31. `sudo udevadm trigger`
