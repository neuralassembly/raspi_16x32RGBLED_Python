import io
import picamera
import serial
from PIL import Image

con=serial.Serial('/dev/ttyUSB0', 115200, timeout=10)
w_led = 32
h_led = 16

with picamera.PiCamera() as camera:
    stream = io.BytesIO()
    camera.resolution = (640, 480)
    for foo in camera.capture_continuous(stream, format='jpeg'):
        stream.truncate()
        stream.seek(0)

        im = Image.open(stream)
        w, h = im.size

        im_cropped = im.crop((0, (h-h_led*w//w_led)//2, w, (h+h_led*w//w_led)//2))
        im_resized = im_cropped.resize((w_led, h_led))
        im_rgb = im_resized.convert('RGB')

        for j in range(0, h_led):
            for i in range(0, w_led):
                r, g, b = im_rgb.getpixel((i, j))
                r = r>>4
                g = g>>4
                b = b>>4
                str = "{0:x}{1:x}{2:x}".format(r,g,b)
                con.write(str)
        con.write('.')

        stream.truncate()
        stream.seek(0)

