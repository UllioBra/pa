import io
import os
import re
import sys
import time
import urllib.request

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

bs_p = 'C:/test/muti/'
t_url = 'https://www.manhuagui.com/comic/17023/'

def headers():
    dic = {'Referer': 'https://www.manhuagui.com/comic/17023/176171.html', 'DNT': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    return dic


def MKdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def Get_Time():
    localtime = time.asctime(time.localtime(time.time()))
    return localtime


def Download_File(list_, path, cnt):
    MKdir(path)
    f = open(path + 'Download_Logs.txt', 'a+')
    f.writelines('\n'+Get_Time())
    f.writelines("Download start ---- ")
    for i in list_:
        fe = re.sub(r'\S\w+\S\w+\S\w+\S\w+$', '', os.path.basename(i))
        fe = re.search(r'\.(\w+)$', fe).group()
        res = requests.get(i, headers=headers())
        f.writelines(" HTTP Status Code : " + str(res.status_code))
        with open('%s%d%s' % (path, cnt, fe), 'wb') as file:
            file.write(res.content)
            time.sleep(1)
    f.writelines(" Download finished ----")
    f.close()


def driver_open():
    options = webdriver.ChromeOptions()
    # options.set_headless()
    options.add_extension('./adb.crx')
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument(
        "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'")
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    return driver


def Get_Img_D(num, pa_2,url):
    pa_3 = pa_2 + 'Download_tag.txt'
    if not os.path.isfile(pa_3):
        with open(pa_3, "w") as A:
            A.writelines('0')
    f = open(pa_3, "r")
    cnt = f.readline()
    f.close()
    if cnt == "Down":
        return
    cnt = int(cnt)+1
    num = int(num)

    browser = driver_open()
    browser.get(url + '#p=' + str(cnt))

    while cnt <= num:
        cnt = cnt + 1
        k = []
        try:
            bs = WebDriverWait(browser, 10, 0.1).until(
                EC.presence_of_element_located((By.ID, "mangaFile")))
        finally:
            k.append(bs.get_attribute('src'))

        Download_File(k, pa_2, cnt-1)
        f = open(pa_3, "w")
        if cnt != num:
            f.writelines(str(cnt-1))
        else:
            f.writelines('Down')
        f.close()

        if cnt < num:
            next_ = browser.find_element_by_id('next')
            act = ActionChains(browser)
            act.click(next_)
            act.perform()


def Get_Img(url, pa_1):
    req = requests.get(url, headers=headers())
    bf = BeautifulSoup(req.text, 'html.parser')
    title = bf.find('h2').text
    body = bf.find('span', id='page').parent
    num = re.search(r'\d+', body.text).group()

    pa_2 = pa_1 + title + '/'
    MKdir(pa_2)
    Get_Img_D(num, pa_2, url)


def Get_Comic(url = t_url):
    bf = BeautifulSoup(requests.get(url).text, 'html.parser')
    title = bf.find('h1').text
    cls_t = bf.find_all('h4')
    body = bf.find_all('div', class_='chapter-list cf mt10')

    path = bs_p + title + '/'
    MKdir(path)
    cnt = 0
    for i in body:
        key = cls_t[cnt].text
        pa_1 = path + key + '/'
        MKdir(pa_1)
        cnt = cnt + 1
        for j in i.find_all('ul'):
            for k in j.find_all('li'):
                u = 'https://www.manhuagui.com/'+k.a['href']
                Get_Img(u, pa_1)
