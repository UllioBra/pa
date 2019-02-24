import pretext as p
import linecache as li
import os,sys

sys.path.append('../epublib')
import gsx

def deal(name):
    return name.replace('/', '1').replace('\\', '2').replace('"', '3').replace('|', '4').replace('?', '5').replace('<', '6').replace('>', '7').replace(':', '8').replace('*', '9')


def make(name, epub_path, file_path):
    gsx.init_epub(epub_path, name)
    gsx.update_epub(epub_path + name, file_path + name)
    gsx.make_epub(epub_path, name, 'E:/book/made by ulo/')


if __name__ == "__main__":
    path = 'F:/Autobook/wenku8/'
    epub_path = 'F:/Autobook/epub/'

    print('----------列表-------------')
    lis_ = os.listdir(path)
    dic = {}
    for i in lis_:
        if '.txt' in i:
            k = li.getline(path + i, 3)
            dic[i.strip('.txt')] = k
            sys.stdout.writelines(i.strip('.txt') + ':' + k)
    s = input('-----------请输入更新书目(,间隔 all全部)------------\n')
    if s == 'all':
        for i in dic.keys():
            print('Now ' + "%s" % i)
            p.Main(i, deal(dic[i].strip()), path)
            make(deal(dic[i].strip()), epub_path, path + 'make/')
    else:
        lis = s.split(',')
        for i in lis:
            if i in dic:
                print('Now ' + "%s" % i)
                p.Main(i, deal(dic[i].strip()), path)
            else:
                print('Not exist ' + "%s" % i)
    print('--------------更新完毕--------------')
