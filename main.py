import requests
import pymongo
import threading
import time
import proxies_web
from estimate_ip import updateMongo,addMongo



if __name__=="__main__":
    start = time.time()
    script_start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
    lock = threading.Lock()
    client=pymongo.MongoClient(host='127.0.0.1',port=27017)  #连接远程mongo数据库
    db=client.para_data #选择数据库
    db.authenticate('para','2415')  #输入mongo账号密码
    collection=db.ip  #选择table名"ip"
    threads=[]  #多线程集合建立
    LSS = proxies_web.Proxies()
    LL = LSS.prox_list
    all_ip_count = LSS.count
    print('开始对ip进行验证')
    for i in LL:  #每隔0.1秒开启一个线程，分别传入addMongo的参数为i
        thread=threading.Thread(target=addMongo,args=[i,collection])
        threads.append(thread)
        thread.start()
        time.sleep(0.1)
    for thread in threads:
        thread.join()
    end = time.time()
    print('执行脚本时间：%s，获取ip并导入mongo脚本执行完毕，共计验证%s个ip。'%(script_start,all_ip_count) + "总耗时:" + str(end - start) + "秒")
#-------------------------------------------------------------------------------------------------------------------

    print('目前库存ip，开始执行库存ip验证情况：')
    start_all_count = collection.count_documents({})
    time.sleep(10)
    start2 = time.time()
    script_start2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start))
    html = requests.get('https://www.baidu.com/s?wd=ip')
    threads = []  # 多线程集合建立
    now = time.time()
    threedays_interval = now - 259200
    LL = collection.find({'timestamp': {'$lt': threedays_interval}})
    check_count = collection.count_documents({'timestamp': {'$lt': threedays_interval}})
    for i in LL:  # 每隔0.1秒开启一个线程，分别传入updateMongo的参数为i
        thread = threading.Thread(target=updateMongo, args=[i,collection])
        threads.append(thread)
        thread.start()
        time.sleep(0.1)
    for thread in threads:
        thread.join()
    end_all_count = collection.count_documents({})
    client.close()  # 断开数据库
    end2 = time.time()
    print('执行脚本时间：%s，验证mongo库存ip有效性脚本执行完毕，共计验证%s个库存ip，删除%s个无效ip，剩余IP总数%s个。' % (
    script_start2, check_count,start_all_count-end_all_count,end_all_count) + "总耗时:" + str(end2 - start2) + "秒")
