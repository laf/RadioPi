#!/usr/bin/python3

import RPi.GPIO as io
import string, cgi, time, os
import mpd
import json
io.setmode(io.BCM)
io.setwarnings(False)
# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
switch1 = 17
switch2 = 22

# ok, lets write the pid of this script
pidfile = open("/tmp/music.pid", "w")
pidfile.write("%s" % os.getpid())
pidfile.close()

io.setup(switch1, io.IN)
io.setup(switch2, io.IN)
io.setup(LCD_E, io.OUT)  # E
io.setup(LCD_RS, io.OUT) # RS
io.setup(LCD_D4, io.OUT) # DB4
io.setup(LCD_D5, io.OUT) # DB5
io.setup(LCD_D6, io.OUT) # DB6
io.setup(LCD_D7, io.OUT) # DB7

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

client = mpd.MPDClient()
client.connect("localhost", 6600)

client.repeat

currentstatus = 'stop'
previousstatus = 'stop'

def connectMPD():
	print('Connecting to MPD')
	client.connect("localhost", 6600)
	

def main():
	global previousstatus
	# Initialise display
	lcd_init()
	lcd_byte(LCD_LINE_1, LCD_CMD)
	lcd_string("")
	lcd_byte(LCD_LINE_2, LCD_CMD)
	lcd_string("")
	lcd_byte(LCD_LINE_1, LCD_CMD)
	lcd_string("Hi Alan....")
	lcd_byte(LCD_LINE_2, LCD_CMD)
	print("Starting radio...")
	lcd_string("Starting radio.")
	time.sleep(2)
	lcd_byte(LCD_LINE_1, LCD_CMD)
	lcd_string("Radio ready.")
	lcd_byte(LCD_LINE_2, LCD_CMD)
	lcd_string("Volume 50%")
	client.setvol(50)
	while True:
		powerswitch = io.input(switch1)
		nextswitch = io.input(switch2)
		if (powerswitch == 0):
			print (previousstatus)
			if previousstatus == 'stop':
				try:
					client.play()
				except:
					connectMPD()
					client.play()

				Current = client.currentsong()
				lcd_byte(LCD_LINE_1, LCD_CMD)
				lcd_string(Current['name'])
				lcd_byte(LCD_LINE_2, LCD_CMD)
				lcd_string("Playing...")
				previousstatus = 'play'
			elif previousstatus == 'play':
				try:
					client.stop()
				except:
					connectMPD()
					client.stop()

				lcd_byte(LCD_LINE_2, LCD_CMD)
				lcd_string("Stopped...")
				previousstatus = 'stop'
			time.sleep(1)

		if(nextswitch == 0):
			if previousstatus == 'stop':
				jdata = client.status()
				curvol = int(jdata['volume'])
				if curvol > 90:
					newvol = 10
				else:
					newvol = curvol+10
					
				print("Setting new volume %s" % newvol)
				client.setvol(newvol)
				lcd_byte(LCD_LINE_2, LCD_CMD)
				lcd_string("Volume %s%%" % newvol)

			else:
				try:
					client.next()
				except:
					connectMPD()
					client.next()
				Current = client.currentsong()
				print(Current['name'])
				lcd_byte(LCD_LINE_1, LCD_CMD)
				lcd_string(Current['name'])
			time.sleep(1)

	io.cleanup()

def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)

def lcd_string(message):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  io.output(LCD_RS, mode) # RS

  # High bits
  io.output(LCD_D4, False)
  io.output(LCD_D5, False)
  io.output(LCD_D6, False)
  io.output(LCD_D7, False)
  if bits&0x10==0x10:
    io.output(LCD_D4, True)
  if bits&0x20==0x20:
    io.output(LCD_D5, True)
  if bits&0x40==0x40:
    io.output(LCD_D6, True)
  if bits&0x80==0x80:
    io.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  io.output(LCD_E, True)
  time.sleep(E_PULSE)
  io.output(LCD_E, False)
  time.sleep(E_DELAY)

  # Low bits
  io.output(LCD_D4, False)
  io.output(LCD_D5, False)
  io.output(LCD_D6, False)
  io.output(LCD_D7, False)
  if bits&0x01==0x01:
    io.output(LCD_D4, True)
  if bits&0x02==0x02:
    io.output(LCD_D5, True)
  if bits&0x04==0x04:
    io.output(LCD_D6, True)
  if bits&0x08==0x08:
    io.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  io.output(LCD_E, True)
  time.sleep(E_PULSE)
  io.output(LCD_E, False)
  time.sleep(E_DELAY)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		lcd_byte(LCD_LINE_1, LCD_CMD)
		lcd_string("Shutting down")
		lcd_byte(LCD_LINE_2, LCD_CMD)
		lcd_string("radio.")
		client.stop()
		time.sleep(2)
		lcd_byte(LCD_LINE_1, LCD_CMD)
		lcd_string("Radio shut down.")
		lcd_byte(LCD_LINE_2, LCD_CMD)
		lcd_string("")
		io.cleanup
		os.remove('/tmp/music.pid')
