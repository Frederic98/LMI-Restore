from PIL import Image, ImageDraw, ImageFont
from elaphe import barcode
from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory

TESTING = False

if not TESTING:
    # Setup label printer
    be = backend_factory("linux_kernel")
    BrotherQLBackend = be['backend_class']
    printer = BrotherQLBackend('/dev/usb/lp0')

for id in range(1,11):
    text = '{:06}'.format(id)

    # Create blank image
    img = Image.new('L', (696, 128), 255)

    # Add DataMatrix barcode
    code = barcode('datamatrix',
                   text,
                   options={'rows': 16, 'columns': 16},
                   margins=10)                              # type: Image
    img.paste(code.rotate(90).resize((128,128)), (0,0))

    # Add ID text
    txt = Image.new('L', (128,35), 255)
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype("Ubuntu-Regular.ttf", 30)
    tw,th = draw.textsize(text, font)
    draw.text(((128-tw)//2, 0), text, 0, font=font)
    draw.line((0,34,128,34))
    txt = txt.rotate(90, expand=1)
    img.paste(txt, (128,0))

    img.paste(img, (128+35+15,0))
    img.paste(img, ((128+35+15)*2,0))

    # Save image
    img.save('label.bmp')

    if not TESTING:
        # Print label
        qlr = BrotherQLRaster('QL-700')
        create_label(qlr, img, '62', threshold=70, cut=True)
        printer.write(qlr.data)
