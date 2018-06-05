from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random

ua = UserAgent()
proxies = []
def main():
    proxies_req = Request('http://www.cn-proxy.com/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')
    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.findAll(class_='sortable')[1]
    
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip':   row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
            })

    proxy_index = random_proxy()
    proxy = proxies[proxy_index]

    for n in range(1, 100):
        req = Request('http://2018.ip138.com/ic.asp')
        req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')
        if n % 10 == 0:
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

        try:
            my_ip = urlopen(req).read().decode('gb2312')
            my_ip_soup = BeautifulSoup(my_ip, 'html.parser')
            my_ip_value = my_ip_soup.body.center.string
            print('No.' + str(n) + ': ' + str(my_ip_value))
        except:
            del proxies[proxy_index]
            print('Proxy ' + proxy['ip'] + ': ' + proxy['port'] + ' deleted.')
            proxy_index = random_proxy()
            proxy = proxies[proxy_index]

def random_proxy():
    return random.randint(0, len(proxies) -1)

if __name__ == '__main__':
    main()
    ran = random_proxy()
    print(str(proxies[ran]))
