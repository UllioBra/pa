import os,re,requests
from bs4 import BeautifulSoup

def get(url = 'http://www.36xsw.com/201_201275/'):
    req = requests.get(url)
    req.encoding = 'gbk'
    print("s_code :" ,req.status_code)
    bf = BeautifulSoup(req.text, 'html.parser')
    title = bf.find('h1').text
    nx = bf.find_all('dd')
    lis = []
    for i in nx:
        if i.a['href'].__len__() < 20:
            lis.append(url + i.a['href'])
    return title, lis


def main():
    title, lis = get()
    outp = 'G:/Autobook/36xsw.com/'
    if not os.path.isdir(outp + title):
        os.makedirs(outp + title)
    if not os.path.isfile(outp + title + '/' + 'cnt'):
        with open(outp + title + '/' + 'cnt', 'w', encoding='utf8') as a:
            a.writelines('0')
    with open(outp + title + '/' + 'cnt', 'r') as a:
        cnt = int(a.read())
    for cnt in range(lis.__len__()):
        print(cnt)
        num = '0000' + str(cnt + 1)
        num = num[num.__len__()-4:num.__len__()]

        req = requests.get(lis[cnt])
        req.encoding = 'gbk'
        print('s_code :', req.status_code)
        bf = BeautifulSoup(req.text, 'html.parser')
        body = bf.find('div', id='content')
        with open(outp + title + '/' + num + '.txt', 'w', encoding='utf8') as a:
            a.writelines(body.text.strip())
        with open(outp + title + '/' + 'cnt', 'w') as a:
            a.writelines(str(cnt))

main()