# coding: utf-8
import os
import re
import sys
from time import sleep
from StringIO import StringIO 

import requests
import Image

reload(sys)
sys.setdefaultencoding('utf-8')

def get_html(url):
    HEADERS = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}
    html = requests.get(url, headers=HEADERS)
    html.encoding = 'GBK'
    return html.text

def get_title(html):
    title = re.search(r'<h1>(.*?)</h1>', html, re.S).group(1)
    return title

def get_allpages(url, html):
    pages_section = re.search(r'<div class="page page_c">.*?<div class="updown">', html, re.S).group(0)
    all_links = re.findall(r'<a href=".*?">(\d+)</a>', pages_section, re.S)
    MAXNUM = all_links[len(all_links)-1]
    print u'一共：%s 页' % MAXNUM
    urls = []
    urls.append(url)
    urlshort = re.search(r'(.*?).htm', url, re.S).group(1)
    for i in range(2, int(MAXNUM)+1):
        num = '_%d.htm' % i
        urls.append(urlshort + num)
    return urls

def get_imgs(html):
    imgs_section = re.search(r'<div class="content">.*?</p>', html, re.S).group(0)
    imgsrc = re.findall(r'src="(.*?)"', imgs_section, re.S)
    imgname = [src.split('/')[-1] for src in imgsrc]
    imgs = dict(zip(imgname, imgsrc))
    return imgs

def save_imgs(imgs):
    for imgname, imgsrc in imgs.items():
        HEADERS = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0"}
        bin_content = requests.get(imgsrc, headers=HEADERS).content
        img = Image.open(StringIO(bin_content))
        img.save(imgname)
        print imgname + ' saved.'
        sleep(0.25)

def main(url):
    DIR = 'G:\\Download\\QQDownload\\PIC'

    html = get_html(url)
    title = get_title(html)

    SAVE_DIR = DIR + '\\' + title
    os.mkdir(SAVE_DIR)
    os.chdir(SAVE_DIR)
    urls = get_allpages(url, html)

    all_imgs = {}
    for link in urls:
        print u'正在处理页面：' + link 
        html = get_html(link)
        imgs = get_imgs(html)
        all_imgs.update(imgs)
        sleep(0.25)

    print u'正在保存图片：'
    all_imgs
    save_imgs(all_imgs)

if __name__ == '__main__':
    url = "http://www.rosmm.com/rosimm/2013/11/28/728.htm"
    main(url)
