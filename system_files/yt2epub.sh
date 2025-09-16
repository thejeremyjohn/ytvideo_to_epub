#!/bin/bash

# This script is used to start the yt2epub server
# Save it to /usr/local/sbin/yt2epub.sh
# Make it executable with chmod +x /usr/local/sbin/yt2epub.sh

cd /home/ubuntu/ytvideo_to_epub
python3 -m gunicorn app:app \
	--bind 0.0.0.0:5100 \
	--workers $(nproc --all | awk '{print $1*2+1}') \
	--log-file "-" \
	--access-logfile "-"
