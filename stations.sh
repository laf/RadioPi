#!/bin/bash
set -e
filepathdir=/var/lib/mpd/playlists

declare -A radios
#radios["Default"]="http://www.bbc.co.uk/radio/listen/live/r4_aaclca.pls"
#radios["BBC Radio 1"]="http://www.bbc.co.uk/radio/listen/live/r1_aaclca.pls"
radios["BBC Radio 2"]="http://www.bbc.co.uk/radio/listen/live/r2_aaclca.pls"
#radios["BBC Radio 3"]="http://www.bbc.co.uk/radio/listen/live/r3_aaclca.pls"
#radios["BBC Radio 4"]="http://www.bbc.co.uk/radio/listen/live/r4_aaclca.pls"
#radios["BBC Radio 4 Extra"]="http://www.bbc.co.uk/radio/listen/live/r4x_aaclca.pls"
#radios["BBC 6 Music"]="http://www.bbc.co.uk/radio/listen/live/r6_aaclca.pls"

status=$(mpc status)
if [[ "$status" == *playing* ]]
then
	#Lets exit
	exit
fi

mpc clear
for k in "${!radios[@]}"
do
filepath="${filepathdir}/${k}.m3u" 
station="${k}.m3u"
rm -f "$filepath"
echo "#EXTM3U" >> "$filepath"
pls=${radios[$k]}
echo "#EXTINF:-1, BBC - $k" >> "$filepath"
curl -s $pls | grep File1 | sed 's/File1=\(.*\)/\1/' >> "$filepath"
mpc load "$station"
done
