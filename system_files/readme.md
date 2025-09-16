## Install python3.13 (assuming ubuntu 24.04)
Update your system packages:
```bash
sudo apt update && sudo apt upgrade
```
Install the required dependencies for managing PPAs:
```bash
sudo apt install software-properties-common
```
Add the Deadsnakes PPA to your system:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```
Update the package list to include the new repository:
```bash
sudo apt update
```
Install Python 3.13:
```bash
sudo apt install python3.13
```
Install pip for Python 3.13:
sudo apt install python3.13-distutils
```bash
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13
```
Set Python 3.13 as the default python3 version:
```bash
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.
13 1
```

## git clone this repo

## install requirements
```bash
cd ytvideo_to_epub
pip install -r requirements.txt
```

## setup nginx reverse proxy and automate serving yt2epub after boot
- See guidance at the top of yt2epub.conf re nginx, dns, etc. DO IT.
- PLACE yt2epub.sh at /usr/local/sbin/yt2epub.sh
- PLACE yt2epub.service at /etc/systemd/system/yt2epub.service
- MAKE THEM BOTH EXECUTABLE (chmod +x)

```bash
systemctl enable yt2epub.service
systemctl start yt2epub.service && journalctl --follow -u yt2epub.service
```