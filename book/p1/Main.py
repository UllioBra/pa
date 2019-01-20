from epublib import gsx, test_gsx
import os,re
from bs4 import BeautifulSoup

def main(inp, outp = 'c:/test'):
    if not os.path.isdir(inp):
        print("错误，没有目标文件夹")
        return
    lis = os.listdir(inp)
    for i in lis:
        if os.path.splitext(i)[-1] == '.txt':
           gsx.pre_txt(inp, outp, i)

def test_make(dic = {}):
    name = dic['name']
    path = dic['path']
    outp = dic['outp']
    author = dic['author']
    print('------%s start-------' % name)
    if not os.path.isdir(outp):
        os.makedirs(outp)
    test_gsx.init_epub(outp, name, author)
    test_gsx.del_same_txt(path)
    test_gsx.test_update_epub(outp + name, path)
    test_gsx.make_epub(outp, name, outp)
    print('------%s end-------' % name)

def make():
    name = '一派之长为老不尊'
    path = 'G:/Autobook/www.kuaiyankanshu.net/一派之长为老不尊！'
    outp = 'g:/Autobook/epub/'
    author = '湛蓝工房'
    if not os.path.isdir(outp):
        os.makedirs(outp)
    gsx.init_epub(outp, name, author)
    gsx.update_epub(outp + name, path)
    gsx.make_epub(outp, name)

lis = [
    {'name':'一派之长为老不尊！', 'path':'G:/Autobook/www.kuaiyankanshu.net/一派之长为老不尊！','outp':'g:/Autobook/epub/','author':'湛蓝工房'},
]

if __name__ == "__main__":
    # main(input("input path : "))
    # make()
    for i in lis:
        test_make(i)