from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

img = Image.open('images/hero-dashboard.png')
print(f"Original size: {img.size}")
cropped = trim(img)
print(f"Cropped size: {cropped.size}")
