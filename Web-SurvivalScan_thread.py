#!/usr/bin/env python
# coding=utf-8
import threading
from enum import Enum
import os
import time
from bs4 import BeautifulSoup

import Generate_Report

import requests, sys, random
from tqdm import tqdm
from typing import Optional, Tuple
from termcolor import cprint
from requests.compat import json
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()


class EServival(Enum):
    REJECT = -1
    SURVIVE = 1
    DIED = 0


reportData = []

ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36,Mozilla/5.0 (X11; NetBSD) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"]

stop_event = threading.Event()


def logo():
    logo0 = r'''
              ╦ ╦┌─┐┌┐              
              ║║║├┤ ├┴┐             
              ╚╩╝└─┘└─┘             
╔═╗┬ ┬┬─┐┬  ┬┬┬  ┬┌─┐┬  ╔═╗┌─┐┌─┐┌┐┌
╚═╗│ │├┬┘└┐┌┘│└┐┌┘├─┤│  ╚═╗│  ├─┤│││
╚═╝└─┘┴└─ └┘ ┴ └┘ ┴ ┴┴─┘╚═╝└─┘┴ ┴┘└┘
             Version: 二开0.1
二开作者: 泷羽Sec-尘宇安全
Whoami: https://github.com/dustblessnotdust
Author: 曾哥(@AabyssZG) && jingyuexing
Whoami: https://github.com/AabyssZG
'''
    print(logo0)


def file_init():
    # 新建正常目标导出TXT
    f1 = open("output.txt", "wb+")
    f1.close()
    # 新建其他报错导出TXT
    f2 = open("outerror.txt", "wb+")
    if not os.path.exists(".data"):
        os.mkdir(".data")
    report = open(".data/report.json", "w")
    report.close()


def scanLogger(result: Tuple[EServival, Optional[int], str, int, str]):
    if stop_event.is_set():
        return
    (status, code, url, length, title) = result
    if status == EServival.SURVIVE:
        cprint(f"[+] 状态码为: {code} 存活URL为: {url} 页面长度为: {length} 网页标题为: {title}", "red")
    if (status == EServival.DIED):
        cprint(f"[-] 状态码为: {code} 无法访问URL为: {url} ", "yellow")
    if (status == EServival.REJECT):
        cprint(f"[-] URL为 {url} 的目标积极拒绝请求，予以跳过！", "magenta")

    if (status == EServival.SURVIVE):
        fileName = "output.txt"
    elif (status == EServival.DIED):
        fileName = "outerror.txt"
    if (status == EServival.SURVIVE or status == EServival.DIED):
        with open(file=fileName, mode="a") as file4:
            file4.write(f"[{code}]  {url}\n")
    collectionReport(result)


def survive(url: str, proxies: dict):
    try:
        header = {"User-Agent": random.choice(ua)}
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=url, headers=header, proxies=proxies, timeout=10, verify=False)  # 设置超时10秒
        soup = BeautifulSoup(r.content, 'html.parser')
        if soup.title == None:
            title = "Null"
        else:
            title = str(soup.title.string)
    except Exception:
        title = str("error")
        cprint("[-] URL为 " + url + " 的目标积极拒绝请求，予以跳过！", "magenta")
        return (EServival.REJECT, 0, url, 0, title)
    if r.status_code == 200 or r.status_code == 403:
        return (EServival.SURVIVE, r.status_code, url, len(r.content), title)
    else:
        title = str("error")
        return (EServival.DIED, r.status_code, url, 0, title)


def collectionReport(data):
    global reportData
    if stop_event.is_set():
        return
    (status, statusCode, url, length, title) = data
    state = ""
    if status == EServival.DIED:
        state = "deaed"
        titlel = ""
    elif status == EServival.REJECT:
        state = "reject"
        titlel = ""
    elif status == EServival.SURVIVE:
        state = "servival"
        titlel = f"{title}"
    reportData.append({
        "url": url,
        "status": state,
        "statusCode": statusCode,
        "title": titlel
    })


def dumpReport():
    if stop_event.is_set():
        return
    with open(".data/report.json", encoding="utf-8", mode="w") as file:
        file.write(json.dumps(reportData))


def getTask(filename=""):
    if (filename != ""):
        try:
            with open(file=filename, mode="r") as file:
                for url in file:
                    yield url.strip()
        except Exception:
            with open(file=filename, mode="r", encoding='utf-8') as file:
                for url in file:
                    yield url.strip()


def end():
    count_out = len(open("output.txt", 'r').readlines())
    if count_out >= 1:
        print('\n')
        cprint(f"[+][+][+] 发现目标TXT有存活目标，已经导出至 output.txt ，共 {count_out} 行记录\n", "red")
    count_error = len(open("outerror.txt", 'r').readlines())
    if count_error >= 1:
        cprint(f"[+][-][-] 发现目标TXT有错误目标，已经导出至 outerror.txt ，共行{count_error}记录\n", "red")


def worker(urls, start_index, end_index, proxies):
    for i in range(start_index, end_index):
        if stop_event.is_set():
            break
        url = urls[i]
        if ((':443' in url) and ('://' not in url)):
            url = url.replace(":443", "")
            url = f"https://{url}"
        elif ('://' not in url):
            url = f"http://{url}"
        if str(url[-1]) != "/":
            url = url + "/"
        cprint(f"[.] 正在检测目标URL " + url, "cyan")
        result = survive(url, proxies)
        scanLogger(result)


def main(txt_name, proxy_text, num_threads):
    logo()
    file_init()
    if proxy_text:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy_text},
            "https": "http://%(proxy)s/" % {'proxy': proxy_text}
        }
        cprint(f"================检测代理可用性中================", "cyan")
        testurl = "https://www.baidu.com/"
        headers = {"User-Agent": "Mozilla/5.0"}  # 响应头
        try:
            requests.packages.urllib3.disable_warnings()
            res = requests.get(testurl, timeout=10, proxies=proxies, verify=False, headers=headers)
            print(res.status_code)
            # 发起请求,返回响应码
            if res.status_code == 200:
                print("GET www.baidu.com 状态码为:" + str(res.status_code))
                cprint(f"[+] 代理可用，马上执行！", "cyan")
        except KeyboardInterrupt:
            print("Ctrl + C 手动终止了进程")
            sys.exit()
        except:
            cprint(f"[-] 代理不可用，请更换代理！", "magenta")
            sys.exit()
    else:
        proxies = {}
    cprint("================开始读取目标TXT并批量测试站点存活================", "cyan")
    # 读取目标TXT
    urls = list(getTask(txt_name))
    total_urls = len(urls)
    threads = []
    step = total_urls // num_threads

    for i in range(num_threads):
        start_index = i * step
        end_index = (i + 1) * step if i != num_threads - 1 else total_urls
        thread = threading.Thread(target=worker, args=(urls, start_index, end_index, proxies))
        threads.append(thread)
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        cprint("[!] 捕获到 Ctrl+C 信号，正在终止所有线程...", "yellow")
        stop_event.set()
        for thread in threads:
            thread.join()
        cprint("[!] 所有线程已终止.", "green")

    dumpReport()
    end()
    Generate_Report.generaterReport()
    sys.exit()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Batch website scanner.")
    parser.add_argument("-f", "--file-path", required=True,
                        help="Input target TXT file path (e.g., /some/path/test.txt)")
    parser.add_argument("-p", "--proxy", default="", help="Proxy IP and port")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads to use (default: 10)")
    args = parser.parse_args()

    txt_name = args.file_path
    proxy_text = args.proxy
    num_threads = args.threads

    main(txt_name, proxy_text, num_threads)