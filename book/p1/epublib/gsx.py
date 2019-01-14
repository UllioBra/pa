import os,shutil,re,time,socks
from bs4 import BeautifulSoup

def proxy(http = None, https = None):
    proxies = {'http': http, 'https': https}
    return proxies

def init_path(*args):
    k = []
    for path in args:
        path.replace("\\","/")
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
    print(inp  + filen)
    print(outp + os.path.splitext(filen)[0] + '.html')
    with open(inp  + filen, 'r' , encoding='utf8') as lines, open(outp + os.path.splitext(filen)[0] + '.html', 'w', encoding='utf8') as ex:
        for i,line in enumerate(lines):
            if i == 0:
                k = line
                ex.writelines("%s" % line)
            else:
                ex.writelines("%s" % line)
    return k


def init_epub(outp, name, author = 'Unknown'):
    outp = init_path(outp)[0]
    op = outp + name + '/'
    if os.path.isdir(op):
        print("Existed ! ")
        return
    os.makedirs(op)
    os.makedirs(op + 'META-INF/')
    os.makedirs(op + 'OEBPS/')
    with open(op + 'META-INF/container.xml', "w", encoding='utf8') as a:
        a.writelines(container)
    with open(op + 'OEBPS/content.opf', "w", encoding='utf8') as a:
        a.writelines(content % (name,author, time.asctime(time.localtime(time.time()))))
    with open(op + 'OEBPS/toc.ncx', "w", encoding='utf8') as a:
        a.writelines(toc % (name))
    with open(op + 'mimetype', "w", encoding='utf8') as a:
        a.writelines("application/epub+zip")


def add_content(file_path, name, epub_path):
    file_path, epub_path = init_path(file_path, epub_path)
    with open(epub_path + 'OEBPS/content.opf', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('manifest')
    new_tag = bf.new_tag('item', href=name, id=re.search(r'\d+', name).group(), media_type="application/xhtml+xml")
    tag.append(new_tag)
    with open(epub_path + 'OEBPS/content.opf', "w", encoding='utf8') as a:
        a.writelines(str(bf))

def conc_con_toc(file_path, name, epub_path):
    file_path, epub_path = init_path(file_path, epub_path)
    with open(epub_path + 'OEBPS/content.opf', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('spine')
    new_tag = bf.new_tag('itemref', idref=re.search(r'\d+', name).group())
    tag.append(new_tag)
    with open(epub_path + 'OEBPS/content.opf', "w", encoding='utf8') as a:
        a.writelines(str(bf))


def cnm(tx):
    return tx.replace('navmap','navMap').replace('doctitle', 'docTitle').replace('_class', 'class').replace('navpoint', 'navPoint').replace('navlabel', 'navLabel').replace('playorder', 'playOrder')

def add_toc(file_path, name, epub_path, title):
    file_path, epub_path = init_path(file_path, epub_path)
    add_content(file_path, name, epub_path)
    conc_con_toc(file_path, name, epub_path)
    with open(epub_path + 'OEBPS/toc.ncx', "r", encoding='utf8') as a:
        text = a.read()
    bf = BeautifulSoup(text, 'html.parser')
    tag = bf.find('navmap')
    new_tag1 = bf.new_tag('navPoint', _class='chapter', id=re.search(r'\d+', name).group(), playOrder=re.search(r'\d+', name).group().lstrip('0'))
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
            xmlns:dc="http://purl.org/dc/elements/1.1/" 
            unique-identifier="bookid" version="2.0">
    <metadata>
    <dc:title>%s</dc:title>
	<dc:creator>%s</dc:creator>
    <dc:language>zh-cn</dc:language>
    <dc:date>%s</dc:date>
    </metadata>
    <manifest>
    <item href="toc.ncx" media-type="application/x-dtbncx+xml" id="ncx"/>
    </manifest>
    <spine toc="ncx">
    </spine>
    <guide>
    </guide>
</package>"""

toc = """<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" 
                 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta content="coay_307750" name="dtb:uid" />
        <meta content="2" name="dtb:depth" />
        <meta content="COAY.COM [http://www.coay.com]" name="dtb:generator" />
        <meta content="0" name="dtb:totalPageCount" />
        <meta content="0" name="dtb:maxPageNumber" />
    </head>
    <docTitle>
        <text>%s</text>
    </docTitle>
    <navMap>
    </navMap>
</ncx>"""
