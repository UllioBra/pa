import os,requests,sys

def Get_ip():
    url = 'http://ip.42.pl/raw'
    ip = requests.get(url).text
    print(ip)

Get_ip()