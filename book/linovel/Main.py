import sys
import pa

sys.path.append('../epublib')
import gsx

ep_url = 'F:/Autobook/epub/'
bs_path, lis = pa.to()
for i in lis:
    inp = bs_path + i['name'] + '/'
    gsx.init_epub(ep_url, i['name'], i['author'])
    gsx.update_epub(ep_url + i['name'], inp)
    gsx.make_epub(ep_url, i['name'], 'E:/book/made by ulo/')
