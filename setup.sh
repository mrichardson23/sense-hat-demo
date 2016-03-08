# Get code
git clone https://github.com/mrichardson23/sense-hat-demo.git

# Install evdev
sudo apt-get update
sudo apt-get install -y python-dev python-pip gcc
sudo pip install evdev

# Don't boot to desktop and log in automatically
sudo raspi-config nonint do_boot_behaviour_new B2

# Set to start on boot:
sudo echo "#!/bin/sh -e" > /etc/rc.local
sudo echo "python /home/pi/sense-hat-demo/sense-hat-demo.py &" >> /etc/rc.local
sudo echo "exit 0" >> /etc/rc.local

