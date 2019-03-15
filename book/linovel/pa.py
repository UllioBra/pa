import os
import sys
import requests
import time
import re

from multiprocessing import Pool
from bs4 import BeautifulSoup



bs_path = 'F:/Autobook/linovel/'
bs_url = 'https://www.linovel.net/'

lis = [
    {
        'name': '空想时钟～梦境支配者～',
        'author': '时光旅人',
        'url': 'https://www.linovel.net/book/102610.html'
    },
    {
        'name': '我的妹妹是僵尸！',
        'author': '伊东ちはや',
        'url': 'https://www.linovel.net/book/100222.html'
    },
    {
        'name': '你好！小丑小姐',
        'author': '活动人偶',
        'url': 'https://www.linovel.net/book/100009.html'
    },
    {
        'name': '道家小姐也想成为魔法少女？',
        'author': '趴在叶子上的茧',
        'url': 'https://www.linovel.net/book/101777.html'
    },
    {
        'name': '实验品少女现世生存手册',
        'author': '硝基化合物',
        'url': 'https://www.linovel.net/book/104327.html'
    },
    {
        'name': '舍管、匿于魔女学院之巅',
        'author': '三日月待宵',
        'url': 'https://www.linovel.net/book/104755.html'
    },
]


def get_chapter_lis(url='https://www.linovel.net/book/102610.html#catalog'):
    req = requests.get(url)
    print("s_code :", req.status_code)
    bf = BeautifulSoup(req.text, 'lxml')
    body = bf.find_all('div', class_='chapter')
    lis = []
    for i, j in enumerate(body, start=1):
        lis.append([bs_url + j.a['href'], i, j.a.text])
    return lis


def get_txt(outp, url='https://www.linovel.net/book/102610/71490.html', k=bs_path + 'text.txt', title = 't'):
    print(url)
    req = requests.get(url)
    print('s_code :', req.status_code)
    bf = BeautifulSoup(req.text, 'lxml')
    body = bf.find('div', class_='article-text').find_all('p')
    with open(outp, 'w', encoding='utf8') as a:
        a.writelines(title + '\n')
        for i in body:
            a.writelines(i.text + '\n')
    print(outp)
    with open(k, 'a+', encoding='utf8') as a:
        a.writelines(url + '\n')
    time.sleep(1)


def deal(name):
    return name.replace('/', '1').replace('\\', '2').replace('"', '3').replace('|', '4').replace('?', '5').replace('<', '6').replace('>', '7').replace(':', '8').replace('*', '9')


def get_book(i):
    print("---------start : %s--------------" % i['name'])
    outp = bs_path + deal(i['name']) + '/'
    if not os.path.exists(outp):
        os.makedirs(outp)
        with open(outp + 'tag', 'w', encoding='utf8'):
            pass
    with open(outp + 'tag', 'r', encoding='utf8') as a:
        lis_ = a.readlines()

    bk_lis = get_chapter_lis(i['url'])
    p = Pool(4)
    for i_ in bk_lis:
        if lis_.count(i_[0] + '\n') == 0:
            num = '0000' + str(i_[1])
            num = num[num.__len__()-4:num.__len__()]
            print(num)
            p.apply_async(get_txt, (outp + num + '.txt',
                                    i_[0], outp + 'tag', i_[2]))
    p.close()
    p.join()
    print("------------end : %s--------------" % i['name'])

if __name__ == "__main__":
    for i in lis:
        i['name'] = deal(i['name'])
        get_book(i)
else:
    print('OK')


# get_txt(bs_path + '1.txt', k=bs_path + '2.txt')
