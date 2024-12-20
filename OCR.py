from pdf2image import convert_from_path
import pytesseract
import os
import config as con

# commends:
# - tesseract --list-langs
# - tesseract image.png output -l ara        || on output.txt
# - tesseract image.png stdout -l ara        || on the termenal

def main():
    w_to_txt(imgs_to_text(pdf_to_images()))


def pdf_to_images(path= None):

    path = os.path.join(os.path.dirname(__file__), path)

    if not os.path.exists(path):
        print("path Not exist")
        exit()

    pytesseract.pytesseract.tesseract_cmd = con.tesseract_cmd

    if path is None:
        pdf_path  = os.path.join(os.path.dirname(__file__), con.FILE)
    else:
        pdf_path = path


    images = convert_from_path(pdf_path, dpi= 200, poppler_path= con.poppler_path)
    return images




def imgs_to_text(images):
    extracted_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang= con.LANG)

        extracted_text += f"\n\n {'*' * 30} ( Page {i + 1} ) {'*' * 30}\n\n\n" + text

    return extracted_text




def w_to_txt(extracted_text, out_path= None):

    if out_path is None:
        out_path =(os.path.splitext(con.FILE)[0] + '.txt')

    with open(out_path, 'wb') as file:
        file.write(extracted_text.encode())






if __name__ == '__main__':
    main()