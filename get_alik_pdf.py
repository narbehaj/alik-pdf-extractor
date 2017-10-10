import urllib.request

from os import mknod
from datetime import datetime
from time import strftime
from lxml import html
from requests import get

cur_link = 'http://alikonline.ir/'
file_name = 'alik-{}.pdf'.format(datetime.now().strftime('%Y%m%d'))


def get_file(link, last_get):
    get_link = get(link)
    parsed_link = html.fromstring(get_link.content)
    pdf_link = parsed_link.xpath("//a[@class='moduleItemTitle']/@href")[-1]
    pdf_name = parsed_link.xpath("//a[@class='moduleItemTitle']/text()")[-1]

    if last_get == pdf_name:
        print('PDF is old: {}'.format(pdf_name))
        return
        
    get_pdf_file = get(link + pdf_link)
    parsed_pdf_link = html.fromstring(get_pdf_file.content)
    pdf_file = parsed_pdf_link.xpath("//ul[@class='itemAttachments']/li/a/@href")[0]
    pdf_to_download = cur_link + pdf_file
    
    urllib.request.urlretrieve(pdf_to_download, filename=file_name)

    with open('alik_last.log', 'w') as pdf_file:
        pdf_file.write(pdf_name)        


try:
    with open('alik_last.log', 'r') as pdf_file:
        last_get = pdf_file.readline().strip()
        print('last get is: {}'.format(last_get))

        if last_get:
            get_file(cur_link, last_get)
        else:
            print('last_get file does not exist')
except FileNotFoundError:
    mknod('alik_last.log', mode=777)
    get_file(cur_link, datetime.now().strftime('%Y%m%d'))
