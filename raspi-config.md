1. Download Raspberry Pi Imager

2. Choose OS → Raspberry Pi OS Lite (64-bit)

3. Configure Wi-Fi (SSID, password, country).

4. Use cc and 1234

5. `sudo apt update && sudo apt upgrade -y`

6. Instalar git, chromium, terminal y openbox con los xorgs suficientes`sudo apt install --no-install-recommends git xserver-xorg x11-xserver-utils xinit openbox chromium xterm geany cups -y`

7. `mkdir -p ~/.config/openbox`

8. `nano ~/.config/openbox/autostart`

```nano
   xset -dpms
   xset s off
   xset s noblank

   chromium --noerrdialogs --disable-infobars --kiosk http://10.0.0.2:7777/rasp/maquinas
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

15. Check python is installed (python -v)

16. `git clone https://github.com/informatica-cc/rasp.git rasp`

17. `cd rasp`
18. `python3 -m venv venv`

19. `pip install -r requirements.txt`

20. `/home/cc/rasp/venv/bin/python /home/cc/rasp/app.py`

21. Check it works in localhost:5000

22. `sudo nano /etc/systemd/system/epos-print.service`

```Nano
[Unit]
Description=EPOS Print Service
After=network.target

[Service]
User=cc
WorkingDirectory=/home/cc/rasp
ExecStart=/home/cc/rasp/venv/bin/gunicorn -w 1 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

23. Enable service

```Bash
sudo systemctl daemon-reload
sudo systemctl enable epos-print
sudo systemctl start epos-print
sudo systemctl status epos-print
```

24. Plug printer

25. `lsusb`
    Coger la dirección de la epson, parecida a esta: 0x04b8,0x0202

26. `sudo nano /lib/udev/rules.d/99-myusb.rules`
    SUBSYSTEMS=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0e15", MODE="0666"

idVendor e idProduct con lo que corresponde (sin el 0x)

Añadirlo tb al programa print.py de dentro de la carpeta /rasp

27. `sudo udevadm control --reload-rules`

28. `sudo udevadm trigger`

Example of curl for localhost POST

```
curl 'http://localhost:5000/' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: es-ES,es;q=0.9,en;q=0.8' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/json' \
  -H 'Origin: http://localhost:4200' \
  -H 'Referer: http://localhost:4200/' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Site: same-site' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  --data-raw '{"mensaje":"a13023\nVN150E-G\nEPDM-008/1\nOper: \nPedido: 961","codigo":"a13023"}'

```
