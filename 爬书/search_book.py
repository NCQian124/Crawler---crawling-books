import asyncio
import os

import aiofiles
import aiohttp
import requests
from bs4 import BeautifulSoup
from lxml import etree
headers ={
    "User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
}
def search_book(bookname):

    url = 'http://www.soduzw.com/search.html'
    data={
        "searchtype": "novelname",
        'searchkey':bookname
          }
    response = requests.post(url, headers=headers,data=data)
    content=(response.content.decode("utf-8"))
    tree=etree.HTML(content)
    bookname_list=tree.xpath('/html/body/div[2]/div/div/div[1]/span/a/text()')
    booklink_list=tree.xpath('/html/body/div[2]/div/div/div/span[1]/a/@href')
    bookwriter_list=tree.xpath('/html/body/div[2]/div/div/div[1]/span[2]/text()')
    booklink_list = ['http://www.soduzw.com/' + link for link in booklink_list]
    combined_list = list(zip(bookname_list, bookwriter_list))
    url_title_dict = {url: title for url, title in zip(booklink_list, combined_list)}

    return url_title_dict

