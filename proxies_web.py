import requests
from bs4 import BeautifulSoup
import time


class Proxies(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        self.prox_list = []
        self.prox_list.extend(self.px_git())
        self.prox_list.extend(self.px_kuai())
        self.count = len(self.prox_list)
        print('总计获取%s个ip地址' % self.count)


    def px_kuai(self,page=5):  #https://www.kuaidaili.com/free/inha/
        proxies_list = []
        print('开始获取www.kuaidaili.com免费高匿ip')
        for i in range(1,page+1):
            url='https://www.kuaidaili.com/free/inha/{}/'.format(i)
            try:
                html = requests.get(url,timeout=20,headers=self.headers)
                if html.status_code == 200:
                    soup = BeautifulSoup(html.text, 'lxml').find_all('td')
                    for i in range(15):
                        ip_dict = {}
                        ip_dict['host'] = soup[i * 7].get_text()
                        ip_dict['port'] = soup[i * 7 + 1].get_text()
                        ip_dict['anonymity'] = soup[i * 7 + 2].get_text()
                        ip_dict['type'] = soup[i * 7 + 3].get_text()
                        ip_dict['country'] = soup[i * 7 + 4].get_text()
                        proxies_list.append(ip_dict)
                    time.sleep(0.8)
                else:
                    pass
            except Exception as E:
                f = open('error.txt','a')
                now = time.time()
                times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
                f.write('px_kuai发生错误,时间：' + times + str(E) + ':   \n')
        print('获取到%s个ip地址' % len(proxies_list))
        return proxies_list

    def px_git(self):   #https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list
        proxies_list = []
        print('开始获取https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list免费高匿ip')
        url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
        try:
            html = requests.get(url,timeout=20,headers=self.headers)
            if html.status_code == 200:
                proxies_list = html.text.split('\n')[:-1]
            else:
                pass
        except Exception as E:
            f = open('error.txt', 'a')
            now = time.time()
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
            f.write('px_git发生错误,时间：' + times + ' 错误原因：' + str(E) + ':   \n')
            f.close()
        print('获取到%s个ip地址'%len(proxies_list))
        return proxies_list


if __name__ == "__main__":
    #test
    a = Proxies()
    print(a.prox_list)
    print(a.count)