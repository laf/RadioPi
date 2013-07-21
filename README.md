RadioPi
=======

This project was done for my Dad so that he could listen to digital radio with a simple interface after the one he spent £100 on would hardly pick up a signal unless it was next to the router.

The setup is pretty simple really, you need the following prerequisites:

  1. python3
  2. RPI.GPIO for Python
  3. MPD for Python
  4. mpd (apt-get install mpd)
  
Put stations.sh wherever you like a create a cron job that looks like:
  0 * * * * /home/pi/stations.sh
  
This will run stations.sh and re-load the streaming urls into MPD, it needs to do this as the BBC run session based streams so they expire after a while.
You can edit stations.sh and uncomment or add to the section below declare -A radios.

Now put music.py somewhere and run python3 music.py &

It's better to put an init script in place but I don't currently have access to my radio to post the one I created, I'll do this as soon as I can.

I run a 16x2 LCD module on mine which will display certain information as per the python script, you don't need this but it's handy to see the radios status. Wiring diagram I followed is:

http://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python/

Next I have two push buttons connected up, the first connected to GPIO pin 17 and the second to GPIO 22. These two buttons allow you to control the radio.

Button one will start and stop the streams.
Button two will:
                If stream is playing - it will change channels
                If stream isn't playing - it will change the volume in + 10% increments.
                
Any questions then just ask.
