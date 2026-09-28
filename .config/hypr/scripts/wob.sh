#!/bin/bash
killall wob 2>/dev/null || true
rm -f /tmp/wobpipe
mkfifo /tmp/wobpipe
exec 3<> /tmp/wobpipe
wob -c ~/.config/wob/wob.ini < /tmp/wobpipe
