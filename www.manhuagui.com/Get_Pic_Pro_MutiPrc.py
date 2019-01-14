import io
import os
import random
import re
import sys
import time
import queue
from multiprocessing import Pool, Manager

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gbk')

def headers(ref):
    dic = {'Referer': ref, 'DNT': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    return dic


def Get_Name(key):
    j = '000' + str(key)
    le = len(j)
    return j[le-4:le]


def MKdir(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def Get_Time():
    localtime = time.asctime(time.localtime(time.time()))
    return localtime


def Download_File(list_, path, cnt, res):
    MKdir(path)
    f = open(path + 'Download_Logs.txt', 'a+')
    f.writelines('\n The %d th file based on : %s Time :' % (cnt , list_[0]) + Get_Time())
    f.writelines("Download start ---- ")
    for i in list_:
        fe = re.sub(r'\?\S+', '', os.path.basename(i))
        fe = re.search(r'\.(\w+)$', fe).group()
        res = requests.get(i, headers=headers(res))
        f.writelines(" HTTP Status Code : " + str(res.status_code))
        with open('%s%s%s' % (path, Get_Name(cnt), fe), 'wb') as file:
            file.write(res.content)
            time.sleep(1)
    f.writelines(" Download finished ----")
    f.close()


def driver_open():
    options = webdriver.ChromeOptions()
    # options.set_headless()
    # options.add_argument('--disable-gpu')
    options.add_extension('./adb1.crx')
    options.add_argument("--window-position=0,0")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument("--window-size=1,1")
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument(
        "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'")
    driver = webdriver.Chrome('./chromedriver.exe', options=options)
    return driver


def Get_Img_D(num, pa_2, url):
    pa_3 = pa_2 + 'Download_tag.txt'
    if not os.path.isfile(pa_3):
        with open(pa_3, "w") as A:
            A.writelines('0')
    f = open(pa_3, "r")
    cnt = f.readline()
    f.close()
    if cnt == "Down":
        return
    cnt = int(cnt)
    num = int(num)
    if cnt == num:
        return 
    
    browser = driver_open()
    browser.get(url + '#p=' + str(cnt+1))
    browser.refresh()

    check_key = browser.find_element_by_id('page').text
    if int(check_key) != cnt + 1:
        with open(pa_2 + 'error.log' , 'w') as a:
            a.writelines(Get_Time() + "check_key : %s  cnt : %d \n" %(check_key, cnt))
        return

    while cnt < num:
        cnt = cnt + 1
        k = []
        try:
            bs = WebDriverWait(browser, 100, 0.1).until(
                EC.presence_of_element_located((By.ID, "mangaFile")))
        finally:
            k.append(bs.get_attribute('src'))

        Download_File(k, pa_2, cnt, url)
        with open(pa_3, 'w') as a:
            a.writelines(str(cnt))

        if cnt < num:
            next_ = browser.find_element_by_id('next')
            act = ActionChains(browser)
            act.click(next_)
            act.perform()
        time.sleep(2) # 多进程,别浪死(^_^)
    browser.quit()


def Get_Img(url, pa_1):
    req = requests.get(url, headers=headers(url))
    bf = BeautifulSoup(req.text, 'html.parser')
    title = bf.find('h2').text
    # title : 单回题目
    body = bf.find('span', id='page').parent
    pa_2 = pa_1 + title + '/'
    MKdir(pa_2)

    if not os.path.isfile(pa_2 + 'Num.txt'):
        with open(pa_2+'Num.txt','x') as a:
            a.writelines(re.search(r'\d+', body.text).group())

    with open(pa_2+'num.txt', 'r') as a:
        num = a.readline()
    Get_Img_D(num, pa_2, url)



# 根据获取的目录url download comic
def Get_Comic(url):
    # url : 待获取comic的目录页
    bf = BeautifulSoup(requests.get(url).text, 'html.parser')
    title = bf.find('h1').text
    # title : comic name
    cls_t = bf.find_all('h4')
    # cls_t : 创建单行本等目录所需
    body = bf.find_all('div', class_='chapter-list cf mt10')
    # body : 获取整体目录列表
    path = bs_p + title + '/'
    # path : 存储目录
    MKdir(path)
    global p_path
    p_path = path

    with open(path + 'Download_logs.txt', "a") as A:
        A.writelines('\n' + "Process starts on %s " %Get_Time() + '\n')

    cnt = 0
    p = Pool(4)
    for i in body:
        key = cls_t[cnt].text
        # key : dxb,dh,fw
        pa_1 = path + key + '/'
        # pa_1 : 针对key值的存储目录
        MKdir(pa_1)
        cnt = cnt + 1
        for j in i.find_all('ul'):
            for k in j.find_all('li'):
                u = 'https://www.manhuagui.com/'+k.a['href']
                # u : 单篇首页
                p.apply_async(Get_Img, (u, pa_1)) 
    p.close()
    p.join()


bs_p = 'G:/AutoComic/'

def Main():
    t_url = 'https://www.manhuagui.com/comic/19573/'
    try:
        Get_Comic(t_url)
    except KeyboardInterrupt:
        with open(p_path + 'Download_logs.txt', "a") as a:
            a.writelines("Process finished on %s by KeyboardInterrupt \n" % Get_Time())
    except IOError:
        with open(bs_p + 'logs.txt', 'a') as a:
            a.writelines('IOError causes the process finished unnormally on %s \n' % Get_Time())
    except:
        with open(bs_p + 'logs.txt', 'a') as a:
            a.writelines(
                "Fatal unknown error on %s causes process to end \n" % Get_Time())
    else:
        with open(p_path + 'Download_logs.txt', 'a') as a:
            a.writelines('Process finished on %s normally' % Get_Time())

def Test():
    Get_Img('https://www.manhuagui.com/comic/17023/176171.html','c:/test/')


if __name__ == "__main__":
    Main()
    # Test()

