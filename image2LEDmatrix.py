import serial
import sys
from PIL import Image

if len(sys.argv)==1:
    print "python image2LEDmatrix.py imagefile mode"
    print " mode 0:whole(default), 1:crop"
    sys.exit()

filename = sys.argv[1]
mode=0
if len(sys.argv)>=3:
    mode = int(sys.argv[2])

w_led = 32
h_led = 16
 
try:
    im = Image.open(filename, 'r')
    w, h = im.size

    if mode==0:  # whole mode
        if float(w)/h < float(w_led)/h_led:
            im_resized = im.resize((w*h_led//h, h_led))
            im_rgb = Image.new('RGB', (w_led, h_led))
            im_rgb.paste(im_resized, ((w_led-w*h_led//h)//2, 0))
        else:
            im_resized = im.resize((w_led, h*w_led//w))
            im_rgb = Image.new('RGB', (w_led, h_led))
            im_rgb.paste(im_resized, (0, (h_led-h*w_led//w)//2))

    else:  # crop mode
        if float(w)/h < float(w_led)/h_led:
            im_cropped = im.crop((0, (h-h_led*w//w_led)//2, w, (h+h_led*w//w_led)//2))
        else:
            im_cropped = im.crop(((w-w_led*h//h_led)//2, 0, (w+w_led*h//h_led)//2, h))
        im_resized = im_cropped.resize((w_led, h_led))
        im_rgb = im_resized.convert('RGB')

    con=serial.Serial('/dev/ttyUSB0', 115200, timeout=10)

    for j in range(0, h_led):
        for i in range(0, w_led):
            r, g, b = im_rgb.getpixel((i, j))
            r = r>>4
            g = g>>4
            b = b>>4
            str = "{0:x}{1:x}{2:x}".format(r,g,b)
            con.write(str)
    con.write('.')

except IOError, TypeError:
    print "Error while processing"
    sys.exit()
