import fitz
import json
import requests
import io

from helpers.cleanDataHelper import CleanDataHelper

class PdfScrapingInfo():
    def __init__(self):
        self.url = ''

    def getPdfWithUrl(self,url):
        response = requests.get(url)
        with io.BytesIO(response.content) as fileByte:
            document = fitz.open(stream=fileByte, filetype="pdf")
            return document

    def getGlossary(self,document,glossaryPage):
        pageContent = document.getPageText(glossaryPage, "json")
        blocks = json.loads(pageContent)["blocks"]
        glossaryContent = []

        for block in blocks:
            counterLine = 0
            textSpan = ''
            pageSpan = ''
            for line in block['lines']:
                if len(block['lines']) == 1:
                    counterSpans = 0
                    for span in line['spans']:
                        if counterSpans == len(line['spans']) - 1 or counterSpans == len(line['spans']) - 2:
                            pageSpan += CleanDataHelper.deleteMultipleWhiteSpaces(span['text'].replace('.', ''))
                        else:
                            textSpan += CleanDataHelper.deleteMultipleWhiteSpaces(span['text'].replace('.', ''))
                        counterSpans += 1
                else:
                    if counterLine == len(block['lines'])-1:
                        for span in line['spans']:
                            pageSpan += CleanDataHelper.deleteMultipleWhiteSpaces(span['text'].replace('.',''))
                    else:
                        for span in line['spans']:
                            textSpan += CleanDataHelper.deleteMultipleWhiteSpaces(span['text'].replace('.',''))
                    counterLine += 1

            glossaryObject = dict(pageSpan=pageSpan,textSpan=textSpan)
            glossaryContent.append(glossaryObject)

        return glossaryContent

pdfScrapingInfo = PdfScrapingInfo()
pdfContentBytes = pdfScrapingInfo.getPdfWithUrl('http://www.ajedrezdeataque.com/17%20Aprendizaje/Desde_cero/Desde_cero.pdf')
glossaryContent = pdfScrapingInfo.getGlossary(pdfContentBytes,1)

print(glossaryContent)

