import os
import requests
import time
import re

from bs4 import BeautifulSoup

def Geturl(dic, url):
    req = requests.get(url)
    req.encoding = 'gbk'
    bf = BeautifulSoup(req.text, 'html.parser')
    body = bf.find('ul', class_='chapter').find_all('a')
    for i in body:
        dic[i.text.strip()] = i['href']
    

def Gettex(url):
    req = requests.get(url)
    req.encoding = 'gbk'
    bf = BeautifulSoup(req.text, 'html.parser')
    body = bf.find('div', id='nr1').text.strip()
    return body.replace('\r','').replace('\n','')


def Get(url = 'https://m.hongyeshuzhai.com/wapbook2229/'):
    print("Start ")
    req = requests.get(url)
    print("S_code :" , req.status_code)
    req.encoding = 'gbk'
    bf = BeautifulSoup(req.text, 'html.parser')
    title = bf.find('h1').text
    body = bf.find('div', class_='page').find_all('a')[1]
    end = int(re.search(r'_\d+',body['href']).group().replace('_',''))
    bs = re.search(r'\d+', url).group()

    outp = './' + title + '/'
    if not os.path.exists(outp):
        os.mkdir(outp)
        with open(outp + 'tag', 'w') as a:
            a.writelines(0)
    with open(outp + 'tag', 'r') as a:
        cnt = int(a.readline())
    with open(outp + 'tag', 'w') as a:
        a.writelines(str(end))

    dic = {}
    for i in range(end-cnt):
        print(i)
        Geturl(dic, re.sub(r'\d+', bs+'_'+str(i+1+cnt), url))

    cnt1 = 0
    for i in dic.items():
        cnt1 = cnt1 + 1
        tex = Gettex('https://m.hongyeshuzhai.com' + i[1])
        tex1 = re.sub(r'\s{2,}', '\n', tex)
        num = '0000' + str(cnt1)
        le = len(num)
        with open(outp + num[le-4:le] + '.txt', 'w', encoding='utf8') as a:
            a.writelines(tex1)
        print("F :" , cnt1)
    print("Finished ")
        

if __name__ == "__main__":
    Get()
