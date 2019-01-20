import os,re,requests
from bs4 import BeautifulSoup

def proxy(http = None, https = None):
    proxy = {
        'http' : http,
        'https' : https
    }
    return proxy

def get_list(url):
    req = requests.get(url, proxies=proxy())
    req.encoding = 'utf8'
    print('s_code :', req.status_code)
    bf = BeautifulSoup(req.text, 'html.parser')
    body = bf.find('ul', class_="dirlist clearfix").find_all('li')
    lis = []
    title = bf.find('nav', class_='mt20').find_all('a')[2].text
    for i in body:
        lis.append(i.a['href'])
    return title, lis

def gettex(i, f, outpa):
    bs_url = 'https://www.kuaiyankanshu.net'
    req = requests.get(bs_url + i, proxies=proxy())
    req.encoding='utf8'
    print('s_code :', req.status_code)
    bf = BeautifulSoup(req.text, 'html.parser')
    title = bf.find('div', class_='title').h1.a['title']
    num = re.search(r'(?<=read_)\d+', bf.find('div', class_='title').h1.a['href']).group()
    for j in bf.find_all('a'):
        j.decompose()
    body = bf.find('div', class_='content', id='chaptercontent').text
    text = re.sub(r'<a.+</a>', '', body)
    tex = re.sub(r'\s+', '\n', text)
    num = '0000' + str(num)
    num = num[num.__len__()-4:num.__len__()]
    print(num)
    f.writelines(i + '\n')
    with open(outpa + num + '.txt', 'w', encoding='utf8') as a:
        a.writelines(title + '\n')
        a.writelines(tex)


def get(url = 'https://www.kuaiyankanshu.net/683920/dir.html'):
    title, lis = get_list(url)
    outpa = 'G:/Autobook/www.kuaiyankanshu.net/' + title + '/'
    if not os.path.isdir(outpa): 
        os.makedirs(outpa)
        with open(outpa + 'Download.log', 'w'): pass
    with open(outpa + 'Download.log', 'r', encoding='utf8') as a:
        lis_ = a.readlines()
    f = open(outpa + 'Download.log', 'a', encoding='utf8')
    for i in lis:
        if not lis_.count(i + '\n'):
            gettex(i, f, outpa)
    f.close()

dic = {
    '一派之长为老不尊！' : 'https://www.kuaiyankanshu.net/683920/dir.html',

}
if __name__ == "__main__":
    for i, j in dic.items():
        print("----------Update %s--------------" % i )
        get(j)
        print("----------Update %s finished-----" % i )
