#coding:utf-8
from config import MainConfig as m
from logger import Logger
import threading,string
from time import sleep
from crawler import feng, huanqiu, netease, sina, tencent, xinhua

list = [feng, huanqiu, netease, sina, tencent, xinhua]

def thread_main(className):
    global count, mutex

    # 取得锁
    mutex.acquire()
    count = count + 1
    # 释放锁
    mutex.release()

    try:
        className.run()
        print(str(className) + "Succeed！")
    except:
        Logger.setLogger(m.log_path, 4, className + " Spider Failed")

    sleep(1)

def main():
    global count, mutex
    threads = []

    count = 1
    # 创建一个锁
    mutex = threading.Lock()
    # 先创建线程对象
    for x in list:
        threads.append(threading.Thread(target=thread_main, args=(x,)))
    # 启动所有线程
    for t in threads:
        t.start()
    # 主线程中等待所有子线程退出
    for t in threads:
        t.join()

if __name__ == '__main__':
    main()

# def run():
#     try:
#         feng.run()
#         print("凤凰网爬虫成功")
#     except:
#         print("凤凰网爬虫失败")
#     try:
#         huanqiu.run()
#         print("环球网爬虫成功")
#     except:
#         print("环球网爬虫失败")
#     try:
#         netease.run()
#         print("网易新闻爬虫成功")
#     except:
#         print("网易新闻爬虫失败")
#     try:
#         sina.run()
#         print("新浪网爬虫成功")
#     except:
#         print("新浪网爬虫失败")
#     try:
#         tencent.run()
#         print("腾讯新闻爬虫成功")
#     except:
#         print("腾讯新闻爬虫失败")
#     try:
#         xinhua.run()
#         print("新华网爬虫成功")
#     except:
#         print("新华网爬虫失败")
#
#     print("All Finished")
#
# if __name__ == '__main__':
#     run()