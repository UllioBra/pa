import os
import sys
import requests
import time
import re

from multiprocessing import Pool
from bs4 import BeautifulSoup


def get_chapter(cookies='', url='https://www.ciweimao.com/book/100021919'):
    req = requests.get(url, cookies=cookies)
    bf = BeautifulSoup(req.text, 'lxml')
    body = bf.find('div', class_="mod-bd book-chapter-detail border-box-shadow").find_all('li')
    lis = []
    for i, j in enumerate(body, start=1):
        lis.append([i, j.a['href'], j.a.text])
    return lis


def get_text(cookies='', url='https://www.ciweimao.com/chapter/100766788'):
    req = requests.get(url, cookies=cookies)
    req.encoding='utf8'
    print(req.text)
    bf = BeautifulSoup(req.text, 'lxml')

if __name__ == "__main__":
    get_text()


header = {
    Host: www.ciweimao.com
    Connection: keep-alive
    User-Agent: Mozilla/5.0 (Windows NT 10.0
                             Win64
                             x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
    DNT: 1
    Accept: image/webp, image/apng, image/*, */*
    q = 0.8
    Referer: https: // www.ciweimao.com/chapter/100766788
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN, zh
    q = 0.9, en
    q = 0.8
    Cookie: bookReadTheme = default % 2C3 % 2C26 % 2Cundefined % 2Ctsu-right % 2C0
    Hm_lvt_1dbadbc80ffab52435c688db7b756e3a = 1549047561, 1549047997, 1549048154, 1549291671
    get_task_type_sign = 1
    ci_session = 2kn40m4tgch9t9jep3tnbngm6p2qdbos
    Hm_lpvt_1dbadbc80ffab52435c688db7b756e3a = 1549292986
    readPage_visits = 4
    user_id = 4722435
    reader_id = 4722435
    login_token = 8c88baca5ef8ce34a85ea6434b4cbfd7
}
