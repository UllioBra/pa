import os,sys,time
import regex as re
import os


def get_chapter(cnt, a):
    num = '0000' + str(cnt)
    num = num[num.__len__()-4:num.__len__()]
    return num

def Main(a, b, path):
    '''
        a: key
        
        b: value
    '''
    with open(path + a + '.txt', 'r', encoding='utf8') as a:
        text = a.readlines()
    cnt = 1
    bs_path = 'F:/Autobook/wenku8/make/%s/' % b
    if not os.path.isdir(bs_path):
        os.makedirs(bs_path)
    f = None
    for i in text:
        tx = i.strip()
        patt = re.compile(r'(?<=^(第.卷)).+')
        k = re.search(patt, tx)
        if k != None:
            tex = re.sub(r'第.章', '', k.group()).strip()
            if tex != '插图':
                path = bs_path + get_chapter(cnt, a) + '.txt'
                cnt = cnt + 1
                if type(f) == 'TextIOWrapper':
                    f.close()
                if os.path.isfile(path):
                    if f is not None:
                        f.close()
                    f = open(bs_path + 'bin.txt', 'w', encoding='utf8')
                else:
                    if f is not None:
                        f.close()
                    f = open(path, 'a', encoding='utf8')
                f.write(tex + '\n')
        elif tx != '' and f is not None :
            f.write(tx + '\n')

    if f is not None:
        f.close()
    if os.path.isfile(bs_path + 'bin.txt'):
        os.remove(bs_path + 'bin.txt')
