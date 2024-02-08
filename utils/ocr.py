import re
import mimetypes
import pytesseract
from PIL import Image
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


img = cv2.imread('c:/Users/LEWIS TAY JUN HAO/downloads/test.jpg')

img = cv2.resize(img, (600, 360))
print(pytesseract.image_to_string(img))
cv2.imshow('Result', img)
cv2.waitKey(0)
