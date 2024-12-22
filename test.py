import PIL
import pytesseract
import config as con


pytesseract.pytesseract.tesseract_cmd = con.tesseract_cmd

image = PIL.Image.open(r"C:\Users\Hp\Desktop\bilal\files\Photos\Others\أريستون.png")
print(pytesseract.image_to_string(image, lang= con.LANG))


