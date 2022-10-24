from PIL import Image
im = Image.open("test_fotos/battle.png")
width, height = im.size
left = 50
top = height/4 +200
right = width/3
bottom = height/2 +10
im1 = im.crop((left, top, right, bottom))

for i in range(im1.height):
    print(im1.getpixel((0,i)))
im1.show()