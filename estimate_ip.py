import requests
import pymongo
import threading
import time

def proxyisOK(proxy):  #判断ip是否可用
    try:
        requests.get('https://www.baidu.com/s?wd=ip',headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'},timeout=20)
    except:
        return True
    proxies={
        'http':proxy,
        'https':proxy
    }
    try:
        html=requests.get('https://www.baidu.com/s?wd=ip',proxies=proxies,timeout=20,headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'})
        if html.status_code==200:
            return True
    except:
        return False

def updateMongo(i):  # 判断ip否可用，如果不可用则删除该ip。
    global unuseful_count
    host = i['host']
    port = i['port']
    proxy = host + ":" + str(port)
    if not proxyisOK(proxy):
        result = collection.delete_many({'host': host, 'port': port})
        print('%s该IP不可用，将移除出数据库' % proxy)
        unuseful_count += 1
        return result
    else:
        result = collection.update_many({'host': host, 'port': port}, {'$set': {'timestamp': now}})
        return result


if __name__ == "__main__":
    unuseful_count = 0
    start = time.time()
    script_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
    html = requests.get('https://www.baidu.com/s?wd=ip')
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)  # 连接远程数据库
    db = client.paradata
    db.authenticate('****', '****')  # 输入账号密码
    collection = db.ip  # 选择table名"ip"
    threads = []  # 多线程集合建立
    now = time.time()
    threedays_interval = now #- 259200
    LL = collection.find({'timestamp': {'$lt': threedays_interval}})
    check_count = collection.count_documents({'timestamp': {'$lt': threedays_interval}})

    for i in LL:  # 每隔0.1秒开启一个线程，分别传入updateMongo的参数为i
        thread = threading.Thread(target=updateMongo, args=[i])
        threads.append(thread)
        thread.start()
        time.sleep(0.1)
    client.close()  # 断开数据库

    for thread in threads:
        thread.join()
    end = time.time()
    print('执行脚本时间：%s，验证mongo库存ip有效性脚本执行完毕，共计验证%s个库存ip，已清除不可用ip地址%s个。' % (
    script_start, check_count, unuseful_count) + "总耗时:" + str(end - start) + "秒")