import os
import shutil
import re
import time
import socks
import math
import zipfile
from bs4 import BeautifulSoup
from multiprocessing import Pool


def proxy(http=None, https=None):
    proxies = {'http': http, 'https': https}
    return proxies


def get_digit(k='Unknown'):
    return k


def make_epub(path, name='Unknown', outp='G:/Autobook/epub/'):
    path, outp = init_path(path, outp)
    epub = zipfile.ZipFile(outp + name + '.epub', 'w')
    os.chdir(path + name)
    epub.write('mimetype', compress_type=zipfile.ZIP_STORED)
    for i in os.listdir('.'):
        if os.path.isdir(i):
            for j in os.listdir(i):
                epub.write(i + '/' + j, compress_type=zipfile.ZIP_DEFLATED)
    epub.close()


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
    with open(op + 'mimetype', "w", encoding='utf8') as a:
        a.writelines("application/epub+zip")
    print("Init epub Done ! ")


def add_content(name, epub_path):
    epub_path = init_path(epub_path)[0]
    with open(epub_path + 'OEBPS/content.opf', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('manifest')
    new_tag = bf.new_tag('item', href=name, id='id'+get_digit(
        re.search(r'\d+', name).group()), media_type="application/xhtml+xml")
    tag.append(new_tag)
    with open(epub_path + 'OEBPS/content.opf', "w", encoding='utf8') as a:
        a.writelines(str(bf).replace('media_type', 'media-type'))


def conc_con_toc(name, epub_path):
    epub_path = init_path(epub_path)[0]
    with open(epub_path + 'OEBPS/content.opf', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('spine')
    new_tag = bf.new_tag('itemref', idref='id' +
                         get_digit(re.search(r'\d+', name).group()))
    tag.append(new_tag)
    with open(epub_path + 'OEBPS/content.opf', "w", encoding='utf8') as a:
        a.writelines(str(bf))


def cnm(tx):
    return tx.replace('navmap', 'navMap').replace('doctitle', 'docTitle').replace('_class', 'class').replace('navpoint', 'navPoint').replace('navlabel', 'navLabel').replace('playorder', 'playOrder')


def add_toc(name, epub_path, title):
    epub_path = init_path(epub_path)[0]
    add_content(name, epub_path)
    conc_con_toc(name, epub_path)
    with open(epub_path + 'OEBPS/toc.ncx', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('navmap')
    new_tag1 = bf.new_tag('navPoint', _class='chapter', id='id'+get_digit(re.search(r'\d+', name).group()), playOrder=re.search(r'\d+', name).group().lstrip('0'))
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


def update_epub(epub_path, file_path):
    print("Update start ! ")
    epub_path, file_path = init_path(epub_path, file_path)
    lis_ = os.listdir(epub_path + 'OEBPS')
    for i in os.listdir(file_path):
        if os.path.splitext(i)[-1] == '.txt':
            if not lis_.count(i.replace('txt','html')):
                title = pre_txt(file_path , epub_path + 'OEBPS', i)
                add_toc(i.replace('txt','html'), epub_path, title)
    print("Update done ! ")

def mutip_update_epub_text(epub_path, file_path, i):
    title = pre_txt(file_path , epub_path + 'OEBPS', i)
    add_toc(i.replace('txt','html'), epub_path, title)

def mutip_update_epub(epub_path, file_path, process = 3):
    print("Update start ! ")
    epub_path, file_path = init_path(epub_path, file_path)
    lis_ = os.listdir(epub_path + 'OEBPS')
    lis = []
    p = Pool(process)
    for i in os.listdir(file_path):
        if os.path.splitext(i)[-1] == '.txt':
            if not lis_.count(i.replace('txt','html')):
                lis.append(i)
    for i in lis:
        p.apply_async(mutip_update_epub_text, (epub_path, file_path, i))
    p.close()
    p.join()
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
    <item href="toc.ncx" media-type="application/x-dtbncx+xml" id="ncx"/>
    </manifest>
    <spine toc="ncx">
    </spine>
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
