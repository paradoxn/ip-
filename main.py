import requests
import json
import pymongo
import threading
import time
import proxies_web

def proxyisOK(proxy):  #判断ip是否可用
    try:
        requests.get('https://www.baidu.com/s?wd=ip',headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'})
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


def addMongo(i):  #判断ip否可用，如果可用则上传至数据库储存。i为代理的字典格式
    global useful_count
    if isinstance(i,str):
        i=json.loads(i)
   # print('正在验证ip:%s'%i)
    host=i['host']
    port=i['port']
    proxy=host+":"+str(port)
    now=time.time()
    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
    if collection.find_one({'host':host,'port':port}) is None and proxyisOK(proxy):  #如果ip可用且未重复，则将host和port加入数据库内
        lock.acquire()
        result=collection.insert_one({'host':i['host'],'port':i['port'],'country':i['country'],'type':i['type'],'anonymity':i['anonymity'],'check_time':times,'timestamp':now})
        useful_count += 1
        lock.release()
        return result


if __name__=="__main__":
    start = time.time()
    script_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
    lock = threading.Lock()
    client=pymongo.MongoClient(host='127.0.0.1',port=27017)  #连接远程mongo数据库
    db=client.paradata #选择数据库
    db.authenticate('****','****')  #输入账号密码
    collection=db.ip  #选择table名"ip"
    threads=[]  #多线程集合建立
    LSS = proxies_web.Proxies()
    LL = LSS.prox_list
    all_ip_count = LSS.count
    useful_count = 0
    print('开始对ip进行验证')
    for i in LL:  #每隔0.1秒开启一个线程，分别传入addMongo的参数为i
        thread=threading.Thread(target=addMongo,args=[i])
        threads.append(thread)
        thread.start()
        time.sleep(0.1)

    client.close()  #断开数据库

    for thread in threads:
        thread.join()

    end = time.time()
    print('执行脚本时间：%s，获取ip并导入mongo脚本执行完毕，共计验证%s个ip，实际新增可用ip地址%s个。'%(script_start,all_ip_count,useful_count) + "总耗时:" + str(end - start) + "秒")