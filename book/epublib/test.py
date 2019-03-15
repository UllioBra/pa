import epublib as e

if __name__ == "__main__":
    test = e.EpubBook('1', 'G:/Pa/book/epublib', 'F:/Autobook/linovel', '你好！小丑小姐', 'Unknown')
    test.pretext('0001.txt')