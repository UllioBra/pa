from epublib import gsx
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

def make():
    name = '一派之长为老不尊'
    path = 'G:/Autobook/一派之长为老不尊！'
    outp = 'g:/Autobook/epub/'
    if not os.path.isdir(outp):
        os.makedirs(outp)
    gsx.init_epub(outp, name, '湛蓝工房')

    # with open(outp + 'test/OEBPS/content.opf', "r", encoding='utf8') as a:
    #     text = a.read()
    # bf = BeautifulSoup(text, 'html.parser')
    # tag = bf.find('spine')
    # new_tag = bf.new_tag('itemref', idref='1')
    # tag.append(new_tag)
    # print(bf)

    lis = os.listdir(path)
    for i in lis:
        if os.path.splitext(i)[-1] == '.txt':
            title = gsx.pre_txt(path, outp+name+'/OEBPS/', i)
            gsx.add_toc(outp+name+'/OEBPS/', re.sub(r'[a-z]+', 'html', i), outp+name, title)


if __name__ == "__main__":
    # main(input("input path : "))
    make()