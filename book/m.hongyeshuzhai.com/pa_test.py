import os
import requests
import time
import re

from bs4 import BeautifulSoup
    

def Gettex(url, to):
    req = requests.get(url)
    print("S_code :" , req.status_code)
    req.encoding = 'gbk'
    bf = BeautifulSoup(req.text, 'html.parser')
    title = bf.find('div', class_='nr_title').text.strip()
    body = bf.find('div', id='nr1').text.strip()
    to[0] = bf.find('a', id='pb_next')['href']
    return title + '\n' + body.replace('\r','').replace('\n','')


def Get(url = 'https://m.hongyeshuzhai.com/wapbook2229/'):
    print("Start ")
    req = requests.get(url)
    print("S_code :" , req.status_code)
    req.encoding = 'gbk'
    bf = BeautifulSoup(req.text, 'html.parser')
    title = bf.find('h1').text
    ent = bf.find('li', class_='tomcat').a['href']

    to = []
    outp = 'G:/Autobook/' + title + '/'
    if not os.path.exists(outp):
        os.makedirs(outp)
        with open(outp + 'tag', 'w') as a:
            a.writelines(ent)
        with open(outp + 'cnt', 'w') as b:
            b.writelines('0')
    with open(outp + 'tag', 'r') as a:
        to.append(a.readline())
    with open(outp + 'cnt', 'r') as b:
        cnt = int(b.readline())
    
    while True:
        cnt = cnt + 1
        print(cnt)
        num = '0000' + str(cnt)
        le = len(num)
        to_u = 'https://m.hongyeshuzhai.com' + to[0]
        b = 'https://m.hongyeshuzhai.com/wapbook' + re.search(r'\d+', url).group() + '/'
        if to_u == b:
            print(b)
            break
        with open(outp + num[le-4:le] + '.txt', 'w', encoding='utf8') as a:
            a.writelines(re.sub(r'\s{2,}', '\n', Gettex(to_u, to)))
        with open(outp + 'tag', 'w') as a:
            a.writelines(to[0])
        with open(outp + 'cnt', 'w') as b:
            b.writelines(str(cnt))

    print("Finished ")
        

if __name__ == "__main__":
    Get()
