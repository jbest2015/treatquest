#!/bin/bash
export DISPLAY=:0
export SDL_VIDEODRIVER=x11
export SDL_AUDIODRIVER=dummy

# Start X if not running
if ! pgrep -x Xorg > /dev/null; then
    /usr/lib/xorg/Xorg :0 vt1 -s 0 -dpms &
    sleep 4
fi

# Wait for X
for i in {1..15}; do
    if xset -q > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

xset s off 2>/dev/null
xset s noblank 2>/dev/null
xset -dpms 2>/dev/null

cd /opt/doggame
exec python3 dog_park.py
