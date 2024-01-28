#!/bin/sh -e 
# rc.local 
_IP=$(hostname -I) || true 
if [ "$_IP" ]; then 
    printf "My IP address is %s\n" "S_IP" 
fi

sudo python /home/pi/Sscripts/proyecto.py &

exit 0
