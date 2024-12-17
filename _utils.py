from PyPDF2 import PdfReader


path = 'book.pdf'

def loader(PDFpath: str) -> PdfReader:
    # validat 
    if not PDFpath.endswith('.pdf'):
        raise Exception

    return PdfReader(PDFpath)


def getText(reader: PdfReader, Range: tuple[int]) -> str:
    text = ''
    for i in range(*Range):
        page = reader.pages[i]
        for j in page.extract_text():
            text += j
        return text
 

def store(txt: str, fileName: str='PDFText.txt' ):
    with open(f"{fileName}", 'wb') as file:
        file.write(txt.encode('utf-8'))


def optim(txt: str) -> str:
    newTxt = '\u202e'

    for i in txt:
        if i == '\n':
            i = '\n' + '\u202e'

        newTxt += i
    return newTxt


def main():
     reader = loader(path) 
     text = getText(reader, (5, 16))
     text = optim(text)
     store(text)
    # pass

if __name__ == '__main__':
    main()