import asyncio
import json
import multiprocessing
import os
import tkinter

import aiofiles
import aiohttp
import requests
import re

from bs4 import BeautifulSoup
from lxml import etree
import threading

headers ={
    "User-Agent":
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
}




#获取书本
def get_book_page_num(url,p1):
    response = requests.get(url, headers=headers)
    content = (response.content.decode("utf-8"))
    tree = etree.HTML(content)
    page_num = tree.xpath("//div[@class='pagination']/span/text()")
    page_num_string = ''.join(page_num)
    result = re.search(r'共(\d+)页', page_num_string)


    if result:
        total_pages = int(result.group(1))
        index = url.rfind(".html")  # 获取最后一个 ".html" 的索引
        # 在找到的位置插入文本
        modified_urls = [url[:index] + f"_{i}" + url[index:] for i in range(1, total_pages + 1)]
        return modified_urls
def get_page_details(url):

        response = requests.get(url, headers=headers)
        content = (response.content.decode("utf-8"))
        tree = etree.HTML(content)
        name = tree.xpath('//ul[@class="Look_list"]/li/span[@class="chapterlist1"]/a/text()')
        links = tree.xpath('//ul[@class="Look_list"]/li/span[@class="chapterlist1"]/a/@href')
        combined_dict = dict(zip(name, links))
        return combined_dict




#获取章节名称和链接
def get_detail_name_and_link(url,p1):
    page_link = []
    page_name=[]

    for i in (get_book_page_num(url,p1)):
        res = requests.get(url=i, headers=headers)
        content = res.content.decode('utf-8')
        tree = etree.HTML(content)
        name = tree.xpath('//ul[@class="Look_list"]/li/span[@class="chapterlist1"]/a/text()')

        page_name.append(name)

        links = tree.xpath('//ul[@class="Look_list"]/li/span[@class="chapterlist1"]/a/@href')
        modified_links = ['http://www.soduzw.com/' + link for link in links]
        page_link.append(modified_links)


        # 使用列表推导式将二维列表展开成一维列表

    flattened_names = [name for sublist in page_name for name in sublist]
    flattened_links = [link for sublist in page_link for link in sublist]

        # 将展开后的一维列表合并成一个字典
    combined_dict = dict(zip(flattened_names, flattened_links))

    return combined_dict





async  def get_text(name,book_number,page_number,book_name,semaphore,progress_bar,download_dialog,download_label):

        data = {
            'bid': f'{book_number}',
            'cid': f'{page_number}',
            'siteid': 0,
        }

        def doestory():
            download_dialog.destroy()
        for c in range(16):
            try:
                async with semaphore:
                 async  with aiohttp.ClientSession() as session:
                    async with session.post(url='http://www.soduzw.com/novelsearch/chapter/transcode.html', data=data,
                                headers=headers) as resp:
                        # 解析 JSON

                        parsed_json = json.loads(await resp.text())

                         # 提取 Unicode 编码内容
                        unicode_content = parsed_json['info']
                        soup = BeautifulSoup(unicode_content, 'html.parser')
                        content = [p.text for p in soup]

                        chapter_content = ''.join(content)

                        async with aiofiles.open(f'{book_name}/{name}.txt', mode="w",
                                                 encoding='utf-8') as f:
                            await f.write(chapter_content)
                        print(name, "下载完毕!")
                        progress_bar['value'] +=1
                        progress_bar.update()
                        if progress_bar['value'] == progress_bar['maximum']:
                            progress_bar.destroy()
                            download_label['text']=f'{book_name}下载完成'
                            button1=tkinter.Button(download_dialog,text='确定',command=doestory)
                            button1.pack()
                        return ""
            except Exception as e:
                print(e)
                print(name, "下载失败!, 重新下载. ")
        return name







async def get_link(url,book_name,p1,progress_bar,download_dialog,download_label):
    if not os.path.exists(book_name):
        os.makedirs(book_name)
    name_link=get_detail_name_and_link(url,p1)
    tasks = []
    semaphore = asyncio.Semaphore(16)
    progress_bar['value'] = 0 #进度条初始值
    progress_bar['maximum'] = len(name_link) #进度条总长度
    for name,link in name_link.items():
        pattern = r"mulu_(\d+)/(\d+)\.html"
        match = re.search(pattern, link)
        if match:
            book_number = match.group(1)  # 提取2530
            page_number = match.group(2)  # 提取15174076
        tasks.append(asyncio.create_task(get_text(name,book_number,page_number,book_name,semaphore,progress_bar,download_dialog,download_label)))
    await asyncio.wait(tasks)


def get_noe_text(book_number,page_number):
    data = {
        'bid': f'{book_number}',
        'cid': f'{page_number}',
        'siteid': 0,
    }
    response = requests.post(url='http://www.soduzw.com/novelsearch/chapter/transcode.html', data=data,
                                headers=headers)
    parsed_json = json.loads(response.text)

    # 提取 Unicode 编码内容
    unicode_content = parsed_json['info']
    soup = BeautifulSoup(unicode_content, 'html.parser')
    content = [p.text for p in soup]

    chapter_content = ''.join(content)

    return chapter_content
