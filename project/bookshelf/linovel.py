import re
import time
import requests
from bs4 import BeautifulSoup
from gsx.sqlite_gsx import BaseDBProject


class linovel():
    db_path = './test.db'
    name = 'linovel'
    base_url = 'https://www.linovel.net'
    login_url = 'https://www.linovel.net/auth/doLogin/'
    favorite_url = 'https://www.linovel.net/my/favorite/'
    check_in_url = 'https://www.linovel.net/my/qiandao'
    username = 'qq_5c2a8edc0fdf6'
    password = 'luoxiangyu'
    book_dic = {
        'id': 'int primary key',
        'title': 'text',
        'author': 'text',
        'tags': 'text',
        'book_data': 'text',
        'last_update': 'text',
        'sign_status': 'text',
        'update_time': 'text',
        'img_url': 'text',
        'book_url': 'text'
    }
    proxies = {
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080'
    }

    def login(self, url=login_url):
        dica = {
            '_kotori': 'a1881cd539a5b3cf20a25eb25e59407c',
            'lgt': '0',
            'redirect': '/',
            'username': self.username,
            'password': self.password
        }
        req = requests.post(url, data=dica)
        return req.cookies

    def check_in(self, url=check_in_url):
        req = requests.get(url, cookies=self.login())
        print(req)

    def Get_list(self, url=favorite_url):
        req = requests.get(url, cookies=self.login())
        bf = BeautifulSoup(req.text, 'html.parser')
        body = bf.find(
            'div', class_='works-grid row')
        img = body.find_all('img')
        book = body.find_all('div', class_='caption')
        lis = []
        patt = r'\d+(?=\.html)'
        for i, j in zip(img, book):
            book_url = self.base_url + j.a['href']
            dic = {'img_url': i['data-original'],
                   'book_url': book_url, 'id': re.search(patt, book_url).group()}
            lis.append(dic)
            print(dic['id'])
        return lis

    def Get_book_info(self, url='https://www.linovel.net/book/100009.html'):
        dic = {}
        req = requests.get(url)
        bf = BeautifulSoup(req.text, 'html.parser')
        sign = bf.find('div', class_='book-sign')
        pre_tags = bf.find('div', class_='book-cats clearfix').find_all('a')
        book_data = bf.find('div', class_='book-data')
        book_data = re.sub(r'(?=</i>)', '|', str(book_data))
        dic['tags'] = '|'.join(x.text for x in pre_tags)
        dic['title'] = bf.find('h1', class_='book-title').text
        dic['author'] = bf.find('div', class_='name').text.strip()
        dic['book_data'] = re.sub(
            r'<{1}?.+?>{1}?', '', book_data).replace('\n', '').replace(' ', '')
        dic['last_update'] = bf.find('div', class_='book-last-update').text
        dic['sign_status'] = sign.text if sign is not None else '未签约'
        dic['update_time'] = time.asctime(time.localtime(time.time()))
        return dic

    def Main(self):
        db = BaseDBProject('./test.db')
        lis = []
        for i in self.Get_list():
            dic = dict(self.Get_book_info(i['book_url']), **i)
            print(dic['title'])
            # db.create_table(self.name, self.book_dic)
            lis.append(dic['id'])
            # db.insert(self.name, dic)
        condition = ' and '.join('id!=%s' % i for i in lis)
        db_lis = db.fetchall(db.selete(['id'], self.name, condition))
        if db_lis != []:
            db.delete(self.name, ' or '.join('id=%s' % i[0] for i in db_lis))
        db.close()


test = linovel()
# test.Main()
loc = time.localtime(time.time())
print(time.strftime('time : %H', loc))
test.check_in()
