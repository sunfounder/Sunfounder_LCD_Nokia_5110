#######################################################
#
#	This Python Script is for LCD of Nokia 5110 module 
#	from SunFounder. Get it from www.sunfounder.com
#
#######################################################	
import math
import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

SCLK = 17
DIN  = 18
DC   = 27
RST  = 23
CS   = 22

disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)
sunfounderlogo = Image.open('pic/Sunfounder8448.png').convert('1')
font = ImageFont.truetype('font/Mario-Kart-DS.ttf', 16)

def setup():
	disp.begin(contrast=60)
	disp.clear()
	disp.display()

def bootanimation():
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)
	Cmax = 100		# Circle max 
	speed = 3		# animate speed
		
	for i in range(0, Cmax/2+10, speed):
		x1 = i - ( Cmax - 84 ) / 2
		y1 = i - ( Cmax - 48 ) / 2
		x2 = ( Cmax + 84 ) / 2 - i
		y2 = ( Cmax + 48 ) / 2 - i
		draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
		draw.ellipse((x1, y1, x2, y2), outline=0, fill=0)
		draw.text((2, 7), 'SUN', font=font)
		draw.text((10, 22), 'FOUNDER', font=font)
		disp.image(image)
		disp.display()
	time.sleep(2)
	for i in range(0, 48/2+10, 4):
		x1 = 84 / 2 - 2 * i
		y1 = 48 / 2 - i
		x2 = 84 / 2 + i * 2
		y2 = 48 / 2 + i
		draw.rectangle((x1, y1, x2, y2), outline=255, fill=255)
		disp.image(image)
		disp.display()
	time.sleep(1)

def bootimage(sec):
	disp.image(sunfounderlogo)
	disp.display()
	time.sleep(sec)
	disp.clear()

def bye():
	disp.clear()
	byeimage = {}
	byeimage[1] = Image.open('pic/byebye1.png').convert('1')
	byeimage[2] = Image.open('pic/byebye2.png').convert('1')
	byeimage[3] = Image.open('pic/byebye3.png').convert('1')
	
	for i in range(1, 4):
		draw = ImageDraw.Draw(byeimage[i])
		draw.text((8,17), 'BYE', font=font)
	act = 1
	for i in range(0, 9):
		if i == 0 or i == 4 or i == 8:
			act = 1
		if i == 1 or i == 3 or i == 5 or i == 7:
			act = 2
		if i == 2 or i == 6:
			act = 3
		disp.image(byeimage[act])
		disp.display()
		
		time.sleep(0.2)
	disp.clear()
	disp.display()

def shapes():
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	draw.ellipse((2,2,22,22), outline=0, fill=255)
	draw.rectangle((24,2,44,22), outline=0, fill=255)
	draw.polygon([(46,22), (56,2), (66,22)], outline=0, fill=255)
	draw.line((68,22,81,2), fill=0)
	draw.line((68,2,81,22), fill=0)
	disp.image(image)
	disp.display()

	time.sleep(2)

def animate():
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)
	
	text = '.......................................'
	maxwidth, height = draw.textsize(text, font=font)

	# Set starting position.
	startpos = 83
	pos = startpos

	# Animate text moving in sine wave.
	while True:
		# Clear image buffer.
		draw.rectangle((0,0,83,47), outline=255, fill=255)
		# Enumerate characters and draw them offset vertically based
		# on a sine wave.
		x = pos
		for i, c in enumerate(text):
			# Stop drawing if off the right side of	screen.
			if x > 83:
				break
			if x < -10:
				width, height = draw.textsize(c, font=font)
				x += width
				continue
			y = (24-8)+math.floor(10.0*math.sin(x/83.0*2.0*math.pi))
			draw.text((x, y), c, font=font, fill=0)
			width, height = draw.textsize(c, font=font)
			x += width
		disp.image(image)
		disp.display()
		pos -= 2
		if pos < -maxwidth:
			pos = startpos
		time.sleep(0.01)

def main():
	bootimage(2)
	bootanimation()
	shapes()
	animate()

if __name__ == "__main__":
	setup()
	try:
		main()
	except KeyboardInterrupt:
		bye()
