import os
import shutil
import re
import time
import socks
import math
import zipfile
import base64
from bs4 import BeautifulSoup
from multiprocessing import Pool


def proxy(http=None, https=None):
    proxies = {'http': http, 'https': https}
    return proxies


def get_digit(k='Unknown'):
    return k


def make_epub(path, name='Unknown', outp='G:/Autobook/epub/'):
    print("Epub Maker start ! ")
    path, outp = init_path(path, outp)
    epub = zipfile.ZipFile(outp + name + '.epub', 'w')
    os.chdir(path + name)
    epub.write('mimetype', compress_type=zipfile.ZIP_STORED)
    for i in os.listdir('.'):
        if os.path.isdir(i):
            for j in os.listdir(i):
                epub.write(i + '/' + j, compress_type=zipfile.ZIP_DEFLATED)
    epub.close()
    print("Epub Maker finished ! ")


def init_path(*args):
    k = []
    for path in args:
        path.replace("\\", "/")
        path = path + '/'
        for i in range(3):
            path = re.sub(r'//', '/', path)
        k.append(path)
    return k


def pre_txt(inp, outp, filen):
    inp, outp = init_path(inp, outp)
    k = 0
    if os.path.splitext(filen)[-1] != '.txt':
        print("Is not '.txt'")
        return
    print(inp + filen)
    print(outp + os.path.splitext(filen)[0] + '.html')
    with open(inp + filen, 'r', encoding='utf8') as lines, open(outp + os.path.splitext(filen)[0] + '.html', 'w', encoding='utf8') as ex:
        ex.writelines(
            '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">')
        ex.writelines(
            '<head><title></title><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head>')
        ex.writelines('<body>')
        for i, line in enumerate(lines):
            if i == 0:
                k = line
                ex.writelines("<h2>%s</h2>" % line)
            else:
                ex.writelines("<p>%s</p>" % line)
        ex.writelines('</body></html>')
    return k


def del_same_txt(file_path):
    print("Delete same txt file ! ")
    file_path = init_path(file_path)[0]
    dic = {}
    for i in os.listdir(file_path):
        with open(file_path + i, 'r', encoding='utf8') as a:
            title = a.readline().strip().replace(' ', '')
            patt = r'[\u4e00-\u9fa5 | \d | a-z | A-Z]+'
            key = ''
            for j in re.compile(patt).findall(title):
                key = key + j
            if key in dic:
                dic[key].append(i)
            else:
                dic[key] = [i, ]
    lis = []
    for i, j in dic.items():
        for cnt, k in enumerate(j, start=0):
            if cnt >= 1:
                lis.append(k)
                os.remove(file_path + k)
    print("Finished ! ")
    print("List : \n", lis)
    return lis


def init_epub(outp, name, author='Unknown'):
    outp = init_path(outp)[0]
    op = outp + name + '/'
    if os.path.isdir(op):
        print("Existed ! Whether to overwrite the file 0->No 1->Yes : ")
        k = input()
        if k == '0':
            print('Interrupt')
            return
        elif k == '1':
            shutil.rmtree(op)
        else:
            print("Input is illegal")
            return
    os.makedirs(op)
    os.makedirs(op + 'META-INF/')
    os.makedirs(op + 'OEBPS/')
    with open(op + 'META-INF/container.xml', "w", encoding='utf8') as a:
        a.writelines(container)
    with open(op + 'OEBPS/content.opf', "w", encoding='utf8') as a:
        a.writelines(content % (name, author))
    with open(op + 'OEBPS/toc.ncx', "w", encoding='utf8') as a:
        a.writelines(toc % (name))
    with open(op + 'OEBPS/titlepage.xhtml', 'w', encoding='utf8') as a:
        a.writelines(titlepage)
    with open(op + 'OEBPS/cover.jpg', 'wb') as a:
        a.write(base64.b64decode(cover))
    with open(op + 'mimetype', "w", encoding='utf8') as a:
        a.writelines("application/epub+zip")
    print("Init epub Done ! ")


def add_content(epub_path, dic):
    epub_path = init_path(epub_path)[0]
    with open(epub_path + 'OEBPS/content.opf', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('manifest')
    for name, nouse in dic.items():
        new_tag = bf.new_tag('item', href=name, id='id'+get_digit(
            re.search(r'\d+', name).group()), media_type="application/xhtml+xml")
        tag.append(new_tag)
    with open(epub_path + 'OEBPS/content.opf', "w", encoding='utf8') as a:
        a.writelines(str(bf).replace('media_type', 'media-type'))


def conc_con_toc(epub_path, dic):
    epub_path = init_path(epub_path)[0]
    with open(epub_path + 'OEBPS/content.opf', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('spine')
    for name, nouse in dic.items():
        new_tag = bf.new_tag('itemref', idref='id' +
                             get_digit(re.search(r'\d+', name).group()))
        tag.append(new_tag)
    with open(epub_path + 'OEBPS/content.opf', "w", encoding='utf8') as a:
        a.writelines(str(bf))


def cnm(tx):
    return tx.replace('navmap', 'navMap').replace('doctitle', 'docTitle').replace('_class', 'class').replace('navpoint', 'navPoint').replace('navlabel', 'navLabel').replace('playorder', 'playOrder')


def add_toc(epub_path, dic):
    epub_path = init_path(epub_path)[0]
    add_content(epub_path, dic)
    conc_con_toc(epub_path, dic)
    with open(epub_path + 'OEBPS/toc.ncx', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('navmap')
    for name, title in dic.items():
        new_tag1 = bf.new_tag('navPoint', _class='chapter', id='id'+get_digit(re.search(
            r'\d+', name).group()), playOrder=re.search(r'\d+', name).group().lstrip('0'))
        new_tag2 = bf.new_tag('navLabel')
        new_tag3 = bf.new_tag('content', src=name)
        new_tag4 = bf.new_tag('text')
        new_tag4.string = title
        new_tag2.append(new_tag4)
        new_tag1.append(new_tag2)
        new_tag1.append(new_tag3)
        tag.append(new_tag1)
    with open(epub_path + 'OEBPS/toc.ncx', "w", encoding='utf8') as a:
        a.writelines(cnm(str(bf)))


def test_update_epub(epub_path, file_path):
    print("Update start ! ")
    epub_path, file_path = init_path(epub_path, file_path)
    lis_ = os.listdir(epub_path + 'OEBPS')
    dic_ = {}
    for i in os.listdir(file_path):
        if os.path.splitext(i)[-1] == '.txt':
            if not lis_.count(i.replace('txt', 'html')):
                dic_[i.replace('txt', 'html')] = pre_txt(
                    file_path, epub_path + 'OEBPS', i)
    add_toc(epub_path, dic_)
    print("Update done ! ")


container = """<?xml version="1.0"?> 
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"> 
  <rootfiles> 
    <rootfile full-path="OEBPS/content.opf" 
     media-type="application/oebps-package+xml" /> 
  </rootfiles> 
</container>
"""

content = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf"
            unique-identifier="uuid_id" version="2.0">
    <metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xmlns:opf="http://www.idpf.org/2007/opf" 
        xmlns:dcterms="http://purl.org/dc/terms/" 
        xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" 
        xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>%s</dc:title>
	<dc:creator>%s</dc:creator>
    <dc:identifier>Unknown</dc:identifier>
    <dc:language>zh-cn</dc:language>
    <dc:identifier id="uuid_id" opf:scheme="uuid">66666</dc:identifier>
    </metadata>
    <manifest>
    <item href="cover.jpg" id="cover" media-type="image/jpeg"/>
    <item href="titlepage.xhtml" id="titlepage" media-type="application/xhtml+xml"/>
    <item href="toc.ncx" media-type="application/x-dtbncx+xml" id="ncx"/>
    </manifest>
    <spine toc="ncx">
    <itemref idref="titlepage"/>
    </spine>
    <guide>
  	<reference href="titlepage.xhtml" type="cover" title="封面"/>
  </guide>
</package>"""

toc = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" 
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta content="2" name="dtb:depth" />
        <meta content="0" name="dtb:totalPageCount" />
        <meta content="0" name="dtb:maxPageNumber" />
    </head>
    <docTitle>
        <text>%s</text>
    </docTitle>
    <navMap>
    </navMap>
</ncx>"""

titlepage = '''<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="zh-CN">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
        <title>Cover</title>
        <style type="text/css" title="override_css">
            @page {padding: 0pt; margin:0pt}
            body { text-align: center; padding:0pt; margin: 0pt; }
            div { margin: 0pt; padding: 0pt; }
        </style>
    </head>
    <body>
        <div>
            <img src="cover.jpg" alt="cover" style="height: 100%"/>
        </div>
    </body>
</html>
'''

cover = '''/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcG
BwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwM
DAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAGpAgMDASIA
AhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA
AAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3
ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm
p6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA
AwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx
BhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK
U1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3
uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD+f+ii
igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKK
ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA
KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAo
oooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACii
igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKK
ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA
KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAo
oooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACii
igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKK
ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA
KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAo
oooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACii
igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKK
ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA
KKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA/SD9mT/g1p/aa/ay/Z+8IfErwrdf
DNfDnjbTItW04XuuTQ3AhkGV8xBbsFb1AJ+teaf8FIf+CCXx3/4JafBzSfHfxL/4Q248P6vq6aLF
JomqPdyRXDxSyqHVokwpWGTkE8iv6e/+CGv/ACiC/Z2/7Eiw/wDRdcd/wcW/s4/8NMf8EePjJpsU
Xmah4a0xfFVkcZKNp8i3MmOR1gSZf+BdD0pZv/s0qns9oS/8lUtfny3HlP8AtEaaqbzS/wDAmtPl
e3yP5SP2Bv2DPHv/AAUh/aLsvhh8OItMfxHe2dxf+ZqU7QWkEMCbneSRUcqOijjlmUd6+8v+IOP9
rr/n7+En/hRT/wDyNX0F/wAGR/7Nn9q/FL4z/Fy6tspo2nWnhXTpmTjzLiQ3FxtOOoWC3zg9JORy
K/ogrqxFKNNQS3au/m3b/wAls/mctCrKcpt7J2XySv8A+TXXyP4Mv2gPgnrP7Nnxz8YfD3xEbNtf
8Eazd6HqJtJTLAbi2laKQxsQCy7kOCQMjsK5Cvov/gr1/wApU/2jf+yka9/6cJq+f9B0C+8U6zba
dplld6jqF7IIre1tYWmmnc9FRFBLE+gFedgqkq1CnUlvJJ/ej0cdTjRr1Ka2i2vkmVKK+u/hL/wQ
T/bF+Nemfa9F/Z9+IFvAeh1q2j0NmHPIW9eFiOOoGOR6jON+0J/wRU/at/Zb0OfVPGnwK8e2WlWk
Rnub+ws11a0tIwCS8stm0qRqMclyAOM9RXRP3Pj0MIpydo6ny7RRRQIKK779nn9lj4kfta+Nf+Ed
+GXgbxR461kBWkttF06S7NuhOA8rKCsSZ/jcqvvXvPxu/wCCD/7Xn7O/gOTxN4p+BHjKHRYEMk8+
nfZ9Wa2QDJeWO0klkjUDks6gDByRiiXurmlogj70uSOrP2n/AOCXH/Btj+yZ+1B/wTv+DvxC8YeC
tevvFHjDwvaanqdxD4lvoEmnkTLMI0kCqCewGK+Nv+Dn7/gjp8B/+CZHwV+FetfCHw5qmh3/AIp1
u8stRe71m5vhLFHAjoAJXYKQxPIr9s/+CEWq2+sf8Eef2eJbaVJo08G2kDMvQPHujdfqHVgfcGvz
u/4Pff8Ak2r4Ff8AYzaj/wCksdRn96VSap6fvIrTt7RK33aBkv7ylBz19xvXvyN3+/U/nIoorq/g
18CvG37RXjeLw14A8I+JfG3iGdGlTTdC0ybULoouNz+XErMFGRlsYGeTWiTbshNpK7OUor7bt/8A
g3H/AG2Lnw2NVX4B+JBbNH5oR9S05LnH/XA3Alz/ALOzPtXyx8c/2cPiD+zF4v8A7A+I3gjxX4F1
oqZEste0qfT5pUBxvRZVXehPRlyp7GpbSfK9xq7V1scXRRRTAKKKKACiiigAooooAKKKKACiiigA
ooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACi
iigAooooAKKKKACiiigD+1D/AIIa/wDKIL9nb/sSLD/0XXY/sveN7P8AaG8B/GHwTrLfbj4X8ba/
4S1SNmzut53+1xIfQfZL6FevQdug47/ghr/yiC/Z2/7Eiw/9F14D+wb+0VF4F/4OEv2yfgteXMUY
8UWmheNtLh5+eaLS7KC6wT/EUmtzt9ImI6GunH0o1swrYepqpRq6ealFv/yTn/4exzYGUoYGlWho
4+zbfWzTj/6XKD+V+hs/8ECP2XLX/gmL/wAEsPEcnihTZzWniPxLr2tXDRgO0FjczWiyYGTg29ir
gEk/P15r6+/Yg8Yal8R/2Pfhn4m1rf8A2x4q8N2Ou3wck7Z7uFbmRRnnAaUgDsAB2r5H/wCDnz9p
v/hmD/gj18Qbewm+yat8RZ7fwhZCNghYXUhe646nNtHcA45y9fan7M/h8eE/2b/h/pYTyxpvhrTr
QKI/L2+Xaxrjb/D06dqxp1ZVlVnPXkdOC+UZX/DkN6kFSlTjHTn9pN/+BRtbsruat5I/jF/4K9f8
pU/2jf8AspGvf+nCav6Tv+DYiD4A+Ov+Cb/hbxb8Jvh94a8I+L7eP+w/G08MHnapNqkKq0pkupC8
7QybxNGjOVRZtqgbSK/mx/4K9f8AKVP9o3/spGvf+nCavrb/AIIrf8Edf2uP24vgvrp8D/EDW/gj
8CvG1zGNY1SW9ubdPFHkiaPEFrCVa7RC7q2944WJI3M0e1csllP+zVCK3hDXbWy3fZpvTq7djbOV
H+0ZSk/ty03vq9l3Ttr0V+5/S18Sv+ChnwB+DPiy50Hxh8cfg/4U1yzYrcadrPjPTrG7gI6h4pZl
dT9RXqHhLxfpPj7w1Z6zoWqadrWj6jEJrS+sLlLm2uoz0eORCVZT6gkV+P3wU/4Mq/2fPCWkWp8d
fEb4peM9VjUee1hJaaPYTHuRD5U0qj2889a/Rr9gL/gnD8MP+CZ/wx1Lwf8ACmz13TtB1a9Go3Fv
qGsXGoL9o8tY2kQSsVjLBV3bAoO0ZHAxtywUXeV30t1+/wDrTbW6xcm5LlWnW/8AwPP/AIfTX8jP
+Dtj/gjV4Q0D4QN+078NtBsPD2q6VfQ2vjiysIhDbajDcSLFDfCNF2iZZnjSRhjeJQx+ZSW/EP8A
Yi/ZK8Rft2ftX+B/hL4VaKLWfGupLZJcSgmOyiCtJPcOByVihSSQgckJgcmv6/f+C4ug2viT/gkJ
+0Vb3cSTRR+BtRulVlDASQxGWNuQeQ6KQeoxkYPNfhT/AMGYPwstPGH/AAUy8X+JLlYnl8IeBrqW
0DLlo5ri6toS6nsfLMq/SQ+9YZRRisXOg17sVzpfKT5fRuL/APAtNjTM6r+qxrJ2k3yX+cUn5tc3
zsf0K/sD/sAfDX/gm9+z3pfw7+GeiQ6dYWkaPqGoSKGv9dutuHu7qXGZJGOeOFQYRFVFVR3njz9o
LwF8K/E2m6L4n8b+EfDms6yM6fYaprFvZ3N9zt/dRyOrSc8fKDzXWyyeVEzf3QTX8Kf7aH7Q2vft
X/tYfEL4ieJL27v9W8Wa9d3ztcSmRoI2lYRQLknEcUYSNFBwqoqjgCiri51MTyy1bV2/uSXz6drW
sVTwyjh5TjpZpffd3f3fO5/c54S8I6T4H0NdP0TT7LS9OEs1wtvZwrFCHmleaVwqgDLySO59SxPe
vxM/4Pff+TavgV/2M2o/+ksdfo//AMEQ9Qn1T/gkZ+zxPczTXE7+CNP3SSuXdsR4GSeegFfnB/we
+/8AJtXwK/7GbUf/AEljrHPKXsr0r35akF91SI8oqe0SqWteEn98GfjD/wAElP8Agmx4i/4Koftn
aB8MtHml0zR9ral4k1hEDf2PpkRUSygHgyMWSONe7yLn5QxH9g37Ff7C/wAL/wDgnz8FLHwF8K/C
1j4c0a2VWuZlUPe6tOBg3F3PjfNKf7zcKMKoVFVR+S3/AAZF/B7TtN/Zu+NXj7yo21fWPElpoHmk
fPHBa2wnCj0DPdknHXYM9BX7N/HT4XN8bvgz4o8Hr4g17wp/wk+mT6WdY0SVIdR05ZkKNLbu6OqS
AMdrbSVPIwQCPUxrlRpKlTV3ypvpdtcyXpZpet2cOFSq1XUqOyvZeSTs3bu3frtbbU8t1f8A4Kp/
s0aB8TW8G3vx7+EVt4njujYyafJ4qshJFcBipgc+ZhZQwK7GIbdxjJxXQftr/sM/DP8A4KDfA3Uf
h/8AFHw3a69ot4rNbTlQt5pNwVKrc2s2C0Uy54I4IyrBlJU/mX/xBP8A7OH/AEUz42/+B2l//IVf
rB+z18H4/wBnz4F+EfAsOt634kg8H6TbaPDqesSpLf3scEaxo87oqq0m1Rlgoz1PNckqVOpRcamr
/B+flbT89LHSqk4Vb09F/Wnnf+tz+J3/AIKF/sUeIf8Agnh+2H42+EfiWVLy88KXuy2vo0KR6laS
KJbe5Ufw74nRiuTtYsuTtzXi1fsh/wAHqvg+w0f/AIKI/DrV7eFYr3WfAcS3bqAPOMV9dKjHjJO1
sfRV9K/G+uTA1JTo3k7tNq/flbjf52udWMhGNX3dmk/TmSdvlcKKKK6zlCiiigAooooAKKKKACii
igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKK
ACiiigAooooAKKKKACiiigD+1D/ghr/yiC/Z2/7Eiw/9F1+L/wDwWe/bp1T/AIJf/wDBzkfjHoul
v4hOleH9O/tDR2vvsaapbzaeYJIPNEb7BjawJRsMgODX6bf8Ebv+Ck37Ovww/wCCWPwH8PeJfj58
FfD2v6P4PsrW/wBM1PxvplpeWUqpho5YpJg6OO6sARX4Vf8AB0V8bPBn7QP/AAVm1/xH4D8XeGPG
3h6bw9pUEeqaBqkGpWTyJAQ6CaFmQsp4Izkd6M3qSjmUatL/AJ+T+5xn+DJyuEZYB06n/PuP/pUP
xD/gtp/wXz1P/gszp3w40Vfhz/wrXRfBF5dXktqPER1j+07icRIkhP2aAJ5aJIBwxPnNyK/rc8K2
qWPhjToYl2xQ2sSIuc4AQACv4GLBgl9CScASKST25r+23RP+Cr37LcWjWit+0p8AVZYUBB+IWkAg
7R/08V1qEIYJKO7nJv7o/wBL7kZVJzliIc2yi1+KP5PP+CiXgqD4lf8ABbX4w+HLmWSC21/4w6np
s0kf340m1Z42YZ4yAxIr+zL4cfDzRvhH8PdD8K+HbCDStA8N2EGl6bZQriO1toY1jijUeiooH4V/
E1/wVB8dab40/wCCmXx38R+GtYsdX0nU/iFrWoaZqmm3SXFtdxPfSvFNDLGSrowIZWUkEEEGv6Xv
+CL3/Bwn8I/29/gR4b0Hxv4w0DwP8Z9LtIdP1bSdZvI7FNbuFXb9psXlYLMJApYxAmSMlgVK7Xbl
yzXKqVNaNWbXf3Ul/wCA6+nN6nRmrUczq1ZfC3JJ9F7z/wDStP8AwH0PkP8A4OL/ANrv9v3Tv2xr
z4a/BDwx8XtE+FUVjZnTNW8B+G7q4uPEM8kKyTMb+3ieWN45DJH5MTocIGZTuU19af8ABtX+zz+1
J8HP2e/G2vftP69431HVvG19ZXegaf4u8R3OratpttHC4cypM7m2Ll4/3ZYP+7O9EIAP3P8AGH9r
T4W/s+eGG1nx18RvA/g/SgMi61jXLazjk9ApkcbmPZVySeACa+GvhN/wdH/s0/Gz9t+H4W6P4ist
J8GDS7u6m+IPiW9TQtHku4ihjtohc7Dh08w+ZKY8siqqtuBpYR+zUqEfelJO997J83y2sunRLVIW
L/eOFWXuxjay7u3L873u/PXofRP/AAWo/wCUSP7Rv/ZPtX/9JXr+f7/gzu+PWn/Cn/gqteeGtRn8
j/hY3hG90ixy2BJdwyQ3iqeccx28+OOuMda/ZX/grn/wUr/Zy+JX/BL/AOPmgeHfj98E9f17WPA2
qWlhpum+ONMuru+me2cJFFFHOXd2JACqCSegr+Tf4HfGnxH+zn8YfDXjvwhqM2k+JvCWow6ppt3G
SDFNEwYZwRlTjDL0ZSQeDU4CoqeYSlP4XBJ/P2if3J3HjabqYGMY7qTa9VyNfe0f3osu9SD0PBr+
Rn9u3/g3N/af+Ff7afirw34J+EviTxt4U1fW7ifw3rWiwLJp81nNMzQiaTcEtnVWCusxUKVJBKYY
/vV/wSv/AODh74Ff8FFfhppEOseKfDvw1+KZRYNS8K63qMdp59xjlrGWUqtzGxyVVSZVAO5eNx+r
Pj7+238IP2WvAj+JfiH8SvBfhLRhGZI59Q1aFGusKW2wR7i87lQSEiVmbHANKth1TrKtN7XXk07d
flp210HQxDqUpUoLez801fp83/mc5/wTK/Z88Qfso/8ABPz4QfDjxX9iHiXwb4Xs9M1JbObzoEnS
Mb1V8DcAeMgYOOMjmvyu/wCD33/k2r4Ff9jNqP8A6Sx19x/sb/8ABwx+zB+174e8W6q/xN8FfDaz
8P8AiCXR9Pj8a+JLHRbzXbZIYXW/it55UdYXeSRVBG791821iUX81f8Ag8N/bF+Ef7Tf7PvwYsvh
t8U/hx8QbzS/EN9PeweGvEtlq0tnG1siq8iwSOUUkEAtgEisc5lOrH2klrKdOX3zjL5aPZ6rqaZX
CNJ+zi9IxnH7oyX9W36Fz/gyN/ac021Pxo+Dt3LDDqt09p4u0xC4DXUaqbW6AHU7P9FP/Az6V+6P
x90Pxj4l+Cniix+Hut2HhvxzcabMug6lf2wubS0vdpMLTRkNui3gBsAnaTjnFfw5fsuftO+NP2Nv
j34a+JXw/wBXl0TxX4Vu1urO4XlJB0eGVc4eKRCyOh4ZWI71/UL/AME2P+Dpr9nf9s3wjpun/EXX
tN+CfxF8vbe2PiG5EGi3DqDmS21B8QhCMEJOY3BJUCQDe3qYiH1qmuT4rWdt9FZNfK3o1c4MO3h6
rTXu3uuq11afzu/nbofn38dv+Csf/BWz9nL4gX3hzxL8OdZ+1WUxiF3pvw1GpafeYAO6C6gjeGVc
MPuMcZwQCCBtfDf/AIKSf8Ff/il8NPEXjCw+G93YeHvC9hNqN7cax4GtdJklhjjaRjbw3PlzXRwp
AECSHPFfv14b+Nfg3xl4eTV9I8W+GdV0qVPNS9s9Ugnt3TGdwkVipGO+a+c/2qv+C5P7Kf7H+kXk
niz40eDL/UbQtG2jeHr1dc1MygZ8poLUuYmPGDNsXnlgK8+blTpuMn79vx9N9+h2xtOacV7v9den
q7n8lP7fv/BRT4n/APBTD4v6d44+K2p6fqev6XpMei2z2VilnElskssqjYnGd8z5P0rwyvTv20PH
nw++KP7Vnj3xJ8KdB1jwv8Pde1ibUNE0jVDF9p06GU7zERESiorlwigttTYpZiCx8xoofw0+Xlvr
bs3q/wAR1/4jXNzJaJ90tF+AUUUVqZBRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFF
FABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUU
AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQA
UUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABR
RRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFF
FABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUU
AFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB/Qj/AMEE/wDg36/Zj/bv/wCCY/gj4mfE
nwjrereLtcu9Siu7m38QXlpG6w3s0MYEcbhRhEXoOa5D/g43/wCCFX7OH/BOn/gnvD8QPhX4U1fR
/E8nimx0o3F1rt3ep5Esc7ONkrlckxrzjIr9A/8Ag1P/AOUJPwx/7CGtf+nO5rzb/g8au/N/4JXe
H9KhhnutQ1v4h6XaWdvAm+SaT7PeMFVR8xJ24AAJyRxzRn6cKnLS096nt5yjf7wyf94n7TXSpv5K
Vvusfyx0V9jfD/8A4N+v2y/ib4JXxBpn7P8A41i0903qupG20y7YeotrmWOf6fJzXzR8bfgB45/Z
r8cy+GfiF4P8S+CPEMCiRtO1zTZrC4KEkCQJIqlkODhhlT2Jol7r5ZbjinKPNHY5Ciul+EvwZ8Yf
HzxrB4a8C+FPEvjTxHdI8sOlaDpk+o3syIpZ2WGFWchVBJIHAGTXrf8Aw6d/am/6Np+P/wD4bzV/
/kenZrcm6ex8/wBFXPEXh3UPCHiC+0nVrG80vVdLuJLS8s7uFoLi0mjYpJFJGwDI6sCpVgCCCCKu
eAPh7r/xX8Zaf4c8LaHrHiXxDq8ogsdL0qykvLy9kOSEihjDO7YB4UE8Uo+9bl1uOXu/FpYx6K+g
P+HTv7U3/RtPx/8A/Deav/8AI9eHeKfC2p+BvEuoaLrWnX+j6xpNzJZ31hfW729zZTxsVkiljcBk
dWBBVgCCCCKV1ew7O1yhRRRTEFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFF
FABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUU
AFFFFABRRRQAUUUUAf1y/wDBqf8A8oSfhj/2ENa/9OdzX354t8HeH9fvNL1bXdN0m7l8LzvqWn3d
9Cj/ANlTeU8bXEbOP3T+VJIm8YISRxnDHPwH/wAGp/8AyhJ+GP8A2ENa/wDTnc1xn/B394s1Xwv/
AMEhpotN1LUNOj1fxhpljfJa3DxLe25S4cwyhSN8ZZEYq2RlFOMgVvnlf2NZzSu7wXzfKl917meU
0vaRcW9PffyTk396P0e+Ffx78DfHS2vJvBHjTwn4xh05xFdvoer2+oLauRkLIYXYKSAcA4rw/wD4
Kt/8Ev8AwL/wVP8A2W9X8EeJ7Gyg8SW0Es/hbxCYc3OgX235HVhhjCxAEkedrr23KrL/ADL/APBs
18fNd+B3/BY/4T2+lX11b6d42uZ/DmsWsTYjv7eeCQqsg7hJkhkHcGMfQ/2CVlisHGeHi29JXXmm
u3pdNP8AyKw+KlCu4rdWfqnff7mmtmvWx/DL+z58YfGn/BNv9uDw/wCLYbSfT/Gfwl8Tg3mnyu0R
eS2mMdzZyEchZFEsTf7LtX9uXwU+L2ifH/4PeF/HPhu5F54f8X6Vbaxp04GPMgniWRCR2OGGR2Oa
/j4/4OFvCFn4H/4LQftAWVhDFBBL4hS/ZIk2KZLm0guJWx6mSVyT3JJ71+y3/Bm7+30PjN+yH4k+
BetXrS6/8Krs6ho6yEkyaPdOW2gknPlXJlB6ALPEAKvLqssVl8ef4klNfNLmS/B+SUmTmEI4fHNw
+Ftx+5vl/Vebkj8yP+Dq/wDYo/4ZQ/4Kpa94ksIPL8OfGK1XxZabY9qR3bHyr2PPdjOhmPT/AI+Q
Pc+k/wDBnB+yjH8Zf+Cjev8AxGv7Rp9O+Evh957aQrlI9QvSbeHJ9fIF2R7r7V+kv/B39+xhH+0B
/wAE2Lf4k2Fn53iH4NatHqBlRSZDpl2y290mPQSG2lJ7CBvU1rf8Giv7J/8AwoD/AIJXweML2yNv
rPxb1u41xpHH7x7KH/RbVen3f3c0i9f9eT3rLJP3UKqf/LtNL0lpH7ot27uDNM3/AHrpNf8ALxpv
/t3WV/VpX7c6+f2z/wAFK/2w7H9gj9hf4lfFa8a38/wro8smmwzSBBd38mIrWHn+9O8Y6HjNfw/6
zrF14h1i61C+uJbu9vpnuLieVtzzSOxZnY9ySSSfev6BP+D1f9uFbHw78NP2etJu186+kPjPxFGh
O5Yk8y3sY2PQhnNy5XrmKI8cZ/nyrhw/7ytOt0+FfLf/AMmun35Udlf93ShS6v3n89vw1X+JhRRR
XccYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFF
FABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB/XL/
AMGp/wDyhJ+GP/YQ1r/053NX/wDg5l/Yw+JH7c//AATQm8JfCzw5J4r8Tad4lsdZbTYbiKGaa3iS
dZDH5jKrMPMU7AdxAOATgHxT/g2l/wCCgPwG+BH/AASA+Hfhnxx8bfhH4N8SWV9q73Ola74w07Tr
63V9RuHQvDNMrqGVgwyOQQRwa9o+M/8Awcs/s0/BH9tjwz8Lrzxp4d17wn4k0VL1vHnh7WbfV9G0
i9e4kiS0umt2fyxtQO0mTs3puAUl16M3oxxGJ9knq3G3rFKX/tvz2WrRjl1SVGlKr25r+kpOP/t3
yWuyPzB/4NqP+CFnxw8Gf8FBNA+MPxY+H/iD4eeEvhstzcWseuxNY3mq6hJbtDEkcDfvDGgmMjSE
BCUCgsdwH9JBbaMngDqa4bSv2oPhrrvw5TxhZfELwPd+EpIjOutw67avpzRgZL+eH8vGO+6vxx/4
L/f8HOfgjQ/g94h+DP7OPiSHxX4p8RwSabrXjLSpt2naNbOCssdlOpxPO65USxkxorZV2fG3lxmM
lGCoxXvR2Xm3u+3ZvskuhvhcKpTdVvR7vyXRd+9u7Z+K3/BXD9oyy/ay/wCCl/xr8f6ZIk+k654p
uk06ZCStxaQEW0EgyT9+KFG64+bjA4rf/wCCLP7d7/8ABOn/AIKOfDz4i3NzNB4a+2f2P4lRMlZd
Muv3UxZQRu8slJgP70C18q0VWXf7IqcVqopL1VrNfNaBj7YqU29OZt+mt1810P7uf2n/AIIaX+1p
+y744+H961vLpfj7w9d6T5rjfGouIGRJeOu0srjHoMVP+zp8HdK/Za/Zr8FeBLF0h0fwD4es9Hjl
d+BHa26Rl2Y467CxJx1Jr5E/4NpP2rPEP7Wf/BIr4d6j4ntrpdU8IGbwit7KmF1W3sSscEyHJLYh
McTMeskMhqv/AMHLn7bqfsWf8Ep/G4s7lYfE3xLH/CGaOqy7JB9qR/tMq9/ktlm5HRmTkZFLMr4N
VfZa83Lbz39n6X59fXXYWX/7V7P2mnLzXt025/W3Jp6abn8x3/BWf9tGT/goB/wUK+JvxPSe5m0f
WdWe30NZicw6bABDaqB/DmNFcgfxO3rXznRRWWHoqjTjSj0X3+b831Na9V1ajqPr+Hl8tgooorYy
CiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAK
KKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoo
ooAK/pZ/4JF/8Gzv7Mvxs/4J4fBzx78VvA2peIPGvizRI9e1GRPEWoWkF1Hcu81upjhlQLi3eFTs
25xnJJyf5pq/Vv4Q/wDB4X+078GvhjoXhSx8HfA6+0/w7YQabZyXehaiJRBDGscanyr+NOFUdFFd
EJwVGS+1dW9EpX/GxjKM3Vi18Nnf10t+p/T18Mvhh4T/AGdvhXpnhfwpo+j+EvCHhi08mzsLKJba
0sIFyxwBgAfeZmPJJZiSSTX8pv8Awcwf8FaLD/gpZ+2ZBongnUft3wp+FqS6ZotzE5MOtXbkfar9
R0KMUSOM85SIOCPMIHmv7e//AAcH/tP/APBRDwlfeF/GHjO00DwVqShLvw54Yshp1jdgc7ZXJe4l
Q8ZSSZk4Hy18TV584TrVVUq7J39X3f4233u9bW7YShRpunT6q3kl2X9eWwUUUV0GAUUUUAFFFFAB
RRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFF
FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUU
UAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQ
AUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAB
RRRQAUUUUAFFe0eAP+CcH7Q/xX8G6f4j8LfAX4z+JfD2rxCex1TSvBOp3lnexkkB4po4WR1yDypI
4rD+Nv7Fvxj/AGaPD9rq3xH+E3xM+H+lX9x9ktrzxJ4XvtKt7ibaz+Ukk8SKz7VZtoOcKTjiiXu6
S0CPvaxPM6K6/wCC37Pnj39pLxTNofw78EeL/Hut21s17Np/hzRrjVLqKBWVGlaKBHYIGdAWIwC6
jPIr1A/8En/2plGT+zV8fwB1P/CvNX/+R6HorsL32LX/AASX/Z68L/tX/wDBR/4Q/DnxrZzah4V8
Xa8lhqdtDcPbvLEUckCRCGU5A5Br+k//AIhOP2J/+if+JP8AwrNR/wDjtfy4/skftN+If2Jf2nPC
HxQ8NWOk3niTwLqI1CztdXhlktJJVDLtlSN43I+Y8K6n3r9N4f8Ag9T/AGppJlU+AfgByQP+QHq/
/wAs66Vyzpwpw+K7+58tvxuY8tSNaTltZfem7/ofqv8A8QnH7E//AET/AMSf+FZqP/x2vxT/AODm
/wD4JufCb/gmf+1N8P8Awt8I9EvtE0fX/Cx1W9jutSnvmkn+1zRZDSsxA2ovA4r+r/whq8mv+E9L
v5gizXtpFcOEBChnQMcZycZPrX82/wDwe0f8n1/Cb/sRT/6X3FeXjuenXpQv9tp/+AT/AFR3YJwq
0KlRfypr5yj+jPxcooorrOcKK0/BngrWfiN4psdD8PaTqeu63qcogs9P061e6uruQ9EjiQFnb2AJ
r698Ef8ABvB+2l8QPC0WsWHwA8XwWk0fmrHqVxZ6ZdAc9be5mjmVuPulAenHIp8r5ea2guZX5ep8
X0V6T+0V+x18V/2RdahsPih8OfGngK4umZbY65pE9nFebfvGGR1CSgZGShYe9ebVEZxkrxdymmtG
FFFFUIKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAC
iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP7PP+CA//ACht
/Z7/AOxVi/8ARslfEX/B7N/yYB8Kv+ygr/6bbyvt3/ggP/yht/Z7/wCxVi/9GyV8Rf8AB7N/yYB8
Kv8AsoK/+m28o4h/j1P+vi/9OInIv4FP/r2//SGfDX/Blv8A8pSfGf8A2TW//wDTjptf0/Xf/HrJ
/uH+VfzA/wDBlv8A8pSfGf8A2TW//wDTjptf0/Xf/HrJ/uH+VbZx/uVP/r3L/wBLmYYX+LU/xL/0
mJ/At4q/5GfUf+vqX/0M1Utf+PmP/eH86t+Kv+Rn1H/r6l/9DNVLX/j5j/3h/Ooy/wCOl/27+h6m
Zf71V/xS/Nn97vw0/wCScaB/2Dbf/wBFLX84P/B7R/yfX8Jv+xFP/pfcV/R98NP+ScaB/wBg23/9
FLX84P8Awe0f8n1/Cb/sRT/6X3Fcmbf75T/6+S/9Imc+T/7lL/r3H/0qB+Lld7+y9+zb4q/bB/aD
8JfDPwTZC/8AFHjLUY9OsY3bbGhblpZGwdscaBndsHCoxxxXBV+u/wDwZk/B/T/Hf/BTbxT4mvYo
Zp/BHgm6ubAOuWiuLi4t7cyL7iJ5l/7aV6WCpRqVbT2Sb9eVN2+drHHi6rp0rx3bSXq2lf5XP3a/
4JXf8Eg/hR/wSi+DdvongzSrbUvGF7bqviHxfd26/wBp63L8pYbjkw24ZRsgQ7FwCdzlnb234i/t
W/C74P8AjzTPC3i34k+AfC/ifWgrafpGr+IbSyv78MSqmKCWRZJMlSBtByQfSu8lk8qJm/ugmv4U
v2zP2gtc/aq/au+IXxD8RXd1eap4s1+81B2nkLmGNpW8uFck4SOPZGqg4VUUDgVw1MVKeIVN66Xf
krqyXrrbtbY7KGEjDDSnHo0u9209W+u3z7n9wfxu+BPg39pT4aal4N8f+GNF8X+F9XTZd6Zqtolz
by45VtrD5XU8q64ZSAVIIBr+Sv8A4OCf+CN8v/BJf9qS1Xw2b6/+Evj5Jb3wxd3DeZLYOhHn6fK/
Vni3oVc/fjkTksr4/oF/4Nlf2itf/aR/4I7/AA1v/E2oS6pqvhuS88NfapmLSyQWk7Jbh2PUrAYk
zzkKMnOa82/4O9vhdp/jr/gj1qutXUSteeCvFGlanZScBkeWU2bjoTgpctkZHQHtgxmdH6tVU4Pr
Ff4oyslf5NPuturLy6t9YpuE10l8pRve3ra3nva6Vv5R6KKK3MQooooAKKKKACiiigAooooAKKKK
ACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA
KKKKACiiigAooooAKKKKACiiigAooooA/sm/4N0/FMXi7/gix8BLiKSGX7Pok9i5jzhWgvbiEg+4
2c++a8w/4Ogf+CdfxL/4KLfsH+HdG+FGiDxN4q8IeK4dbbSheQ2sl3a/ZbmCQxtMyozqZUbbuBYB
sZbCn88/+DUr/gt54B/Ze8D6t+z58YvEVl4Q0a81OTWfCniHVLhYNNtpJVUXFlcTMQkClk81HchC
zyhmUlA39Alz8ffAtl4M/wCEjm8a+EovD3lef/aj6xbrZeXjO/zi+zbjnOcV0ZvSjVk6zfuyanfs
7qTXyej2uteqMMrlKjFUV8STjburOKfzWvr6WPxp/wCDWr/giJ8c/wBg79onxj8XPjDodv4Hhv8A
w5J4b0vQ5byC7vr3zri3ne5YwSOkKJ9nChWO9i5O1QoLft/d/wDHrJ/uH+Vfl3+1H/wdNfAz4bft
g/Dj4VfDzXNA8Z2Gs+J7TTPGHjOS6Efh3w9YySeXI8V1uVJ3XcrGVWMCICS7HIX7Fuv+CsH7LLW0
gH7SvwAJKnA/4WFpHp/18Vy46rKtguZfClKK+Wv4uWj2fTQ0p01SquD3dpP56W/8l23XU/iV8Vf8
jPqP/X1L/wChmqUT+XKrddpBq34klWfxFfujK6PcyMrKchgWOCDVKjDycIxkt1Y7swaeKqtfzS/N
n94v7NHj/T/it+zn4B8T6VKk+meIvDun6laSIwYPFNbRyKQRweGFfjX/AMHcn/BK74z/ALXPxC+H
XxU+FfgvV/H+n+HNCm0TWdO0WP7VqVoRcGaKRLVf3syt5rg+UHIKcgA5riv+Daf/AIOJ/APwi+A+
lfs+/HzxFF4U/wCEbkMHhDxRflv7PezdiwsruXkQGJi3lyviLyyEJQxjzP3X8IfHHwV8QfDUWs6D
4w8L63o86eZFfafqsFzbSL/eWRGKke4NdGZ4eNWv7eHw83Mvmno/NJ2fnr2Z52W1ZUqPsJb25X52
tqvmk19z6o/id+PP/BNT49/st/Bix+IPxI+FPjHwJ4T1HUo9It7vXbI2Mj3TxPMkZgkImXKRSHLI
FypGc8V9n/8ABpF+1FYfs+f8FY7HQNWuVtbH4p6DdeGIWdwkYvN8V1bg57s1u0aju0wHev2C/wCD
kf8AaR/Z5+LH/BMf4pfDjW/jH8N7bxxHaw6pomjxa1b3epvf20qzRRi2iLyp5oR4t5UKBIckDNfy
kaBr994V12y1TTLy50/UtNnS6tLq2lMU1tMjBkkR1IKsrAEEHIIBrLAYvkxMlNe7tp/LKNn5X+L8
DbGYXmw8Wnq/zi7r5beuux/fgy71IPQ8Gv5Dv+Cg/wDwb3/tK/Bb9uDxX4Y8FfB/xp428Ja1rdxc
+GNZ0HTXvdPksZpnaBZ50Hl20iIQrrMUAKkjKlWP6t/8Ee/+Dsf4b/HbwJpPgr9pLVbX4efEazRL
QeJpoiuheIsYAlkdFxZTHkuJAIPl3LIu4RL+tHgj9oPwF8TPC0WueHPG/hDxBok8fnR6hpus293a
yJz8wljcqRwec44NKrhOWqq17pJq62adn9+ml9rvTUKOL5qLpNWbs7PdNX+9av16M8C/4Io/sK6t
/wAE5v8Agm58PPhh4ilil8UWMM2pa2sMgkit726meeSBGGQwi3iPcDhihI4NfF//AAeU/tQ6V8M/
+Ccug/DL7VCfEXxN8SW8iWm4+YLGx/fzTYB6CY2qc5B8w45XI+mf2+v+Dhv9mL9gzwZeTXHj/Rfi
L4tRWS08MeD7+HU7yWYcbZ5I2MVqoJBYysG25Ko5G0/yxf8ABSb/AIKJeOv+Cn37U2r/ABQ8dvFB
PcotlpOlWzE2uh2CMxitYs8kAszMx5d3dsDOBzY2s8ZUXLtdNtbLlaaS+aS8knd3tfbB044aDvvZ
pd25Xu397frayte3gdFFFdJiFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFF
ABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUA
FFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAU
UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRR
RQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFF
ABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUA
FFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAU
UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRR
RQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFF
ABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUA
FFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAU
UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRR
RQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFF
ABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUA
FFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAU
UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRR
RQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFF
ABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUA
FFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAU
UUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB//9k=
'''
