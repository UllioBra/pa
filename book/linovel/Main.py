import sys
sys.path.append('G:/Pa/book')
from epublib import epublib

ep_url = 'G:/Autobook/epub/'
bs_path = 'F:/Autobook/linovel/'

lis = [
    {
        'name': '空想时钟～梦境支配者～',
        'author': '时光旅人',
        'url': 'https://www.linovel.net/book/102610.html'
    },
    {
        'name': '我的妹妹是僵尸！',
        'author': '伊东ちはや',
        'url': 'https://www.linovel.net/book/100222.html'
    },
    {
        'name': '你好！小丑小姐',
        'author': '活动人偶',
        'url': 'https://www.linovel.net/book/100009.html'
    },
    {
        'name': '道家小姐也想成为魔法少女？',
        'author': '趴在叶子上的茧',
        'url': 'https://www.linovel.net/book/101777.html'
    },
    {
        'name': '实验品少女现世生存手册',
        'author': '硝基化合物',
        'url': 'https://www.linovel.net/book/104327.html'
    },
    {
        'name': '舍管、匿于魔女学院之巅',
        'author': '三日月待宵',
        'url': 'https://www.linovel.net/book/104755.html'
    },
]
for i in lis:
    k = epublib.EpubBook(ep_url, ep_url, bs_path, i['name'], 'Unknown')
    k.Print_attr()
    k.run()
