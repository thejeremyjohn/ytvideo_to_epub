## Install miniconda
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    -O /tmp/miniconda.sh

# run the interactive installation >> yes >> init
bash /tmp/miniconda.sh

#refresh the terminal
source ~/.bashrc
```

## Create the conda environment
```bash
conda create -n yt2epub python=3.10.18 -y \
    && conda activate yt2epub
```
## Clone this repo
```bash
git clone https://github.com/thejeremyjohn/ytvideo_to_epub.git
```

## install requirements
```bash
# txt2epub system dependencies
sudo apt update && sudo apt install libegl1 libgl1 libfontconfig1
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