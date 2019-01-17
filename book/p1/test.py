import re
from bs4 import BeautifulSoup
# # a = '00001.html'
# # print(re.sub(r'[a-z]+', "txt", a))
# with open('test.txt', 'r', encoding='utf8') as a:
#     text = a.read()
# bf = BeautifulSoup(text, 'html.parser')
# body = bf.find(name='navMap')
# print(body)
# print(text)

stri = '她她她她她她她她她她她她她她她她她她她'
patt = re.compile(r'w+')
lis = patt.findall(stri)
ans = ''
for i in lis:
    ans = ans + i
dic = {}
dic[ans] = 1
print(ans)