## Install miniconda
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh

source ~/miniconda3/bin/activate
conda init --all
```

## Create the conda environment
```bash
conda create -n yt2epub python=3.10.18 -y \
    && conda activate yt2epub
```
## git clone this repo

## install requirements
```bash
# txt2epub system dependency
sudo apt update && sudo apt install libegl1
# python requirements
pip install -r ytvideo_to_epub/requirements.txt
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