#
# from PIL import Image
# import ImageChops
# import math, operator
#
# def rmsdiff(im1, im2):
#     "Calculate the root-mean-square difference between two images"
#
#     h = ImageChops.difference(im1, im2).histogram()
#
#     # calculate rms
#     return math.sqrt(reduce(operator.add,
#         map(lambda h, i: h*(i**2), h, range(256))
#     ) / (float(im1.size[0]) * im1.size[1]))
#
# img1 = Image.open("test_fotos/1.png")
# img2 = Image.open("test_fotos/2.png")
#
# rmsdiff(img1,img2)
import ImageOps
from PIL import Image # No need for ImageChops
import math
from skimage import img_as_float
from skimage.metrics import structural_similarity

def similarity(im1, im2):
    """Calculates the root mean square error (RSME) between two images"""
    return math.sqrt(structural_similarity(img_as_float(im1), img_as_float(im2)))

img1 = Image.open("test_fotos/1.png")
img2 = Image.open("test_fotos/2.png")
img1 = ImageOps.grayscale(img1)
img2 = ImageOps.grayscale(img2)

print(similarity(img1, img2))