# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     proxyFetcher
   Description :
   Author :        JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25: proxyFetcher
-------------------------------------------------
"""
__author__ = 'JHao'

import re
import json
from time import sleep

from util.webRequest import WebRequest
# todo
# https://www.beesproxy.com/free
# https://smallseotools.com/zh/free-proxy-list/
# https://cn.proxy-tools.com/proxy/cn#

class ProxyFetcher(object):
    """
    proxy getter
    """

    @staticmethod
    def freeProxy01():
        """
        站大爷 https://www.zdaye.com/dayProxy.html
        """
        start_url = "https://www.zdaye.com/dayProxy.html"
        html_tree = WebRequest().get(start_url, verify=False).tree
        latest_page_time = html_tree.xpath("//span[@class='thread_time_info']/text()")[0].strip()
        from datetime import datetime
        interval = datetime.now() - datetime.strptime(latest_page_time, "%Y/%m/%d %H:%M:%S")
        if interval.seconds < 60*60*12:  # 只采集12小时内的更新
            target_url = "https://www.zdaye.com/" + html_tree.xpath("//h3[@class='thread_title']/a/@href")[0].strip()
            while target_url:
                _tree = WebRequest().get(target_url, verify=False).tree
                for tr in _tree.xpath("//table//tr"):
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield "%s:%s" % (ip, port)
                next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
                target_url = "https://www.zdaye.com/" + next_page[0].strip() if next_page else False
                sleep(5)

    @staticmethod
    def freeProxy02(page_count=50): #max=2934
        """
        代理66 http://www.66ip.cn/
        """
        for i in range(1, page_count + 1):
            url = "http://www.66ip.cn/{}.html".format(i)
            resp = WebRequest().get(url, timeout=10).tree
            for i, tr in enumerate(resp.xpath("(//table)[3]//tr")):
                if i > 0:
                    ip = "".join(tr.xpath("./td[1]/text()")).strip()
                    port = "".join(tr.xpath("./td[2]/text()")).strip()
                    yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy03(page_count=10): #max=10
        """ 开心代理 """
        for i in range(1, page_count + 1):
            target_urls = ["http://www.kxdaili.com/dailiip/1/{}.html".format(i), "http://www.kxdaili.com/dailiip/2/{}.html".format(i)]
            for url in target_urls:
                tree = WebRequest().get(url).tree
                for tr in tree.xpath("//table[@class='active']//tr")[1:]:
                    ip = "".join(tr.xpath('./td[1]/text()')).strip()
                    port = "".join(tr.xpath('./td[2]/text()')).strip()
                    yield "%s:%s" % (ip, port)

    # @staticmethod
    # def freeProxy04():
    #     """ FreeProxyList https://www.freeproxylists.net/zh/ """
    #     url = "https://www.freeproxylists.net/zh/?c=CN&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=50"
    #     tree = WebRequest().get(url, verify=False).tree
    #     from urllib import parse
    #
    #     def parse_ip(input_str):
    #         html_str = parse.unquote(input_str)
    #         ips = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', html_str)
    #         return ips[0] if ips else None
    #
    #     for tr in tree.xpath("//tr[@class='Odd']") + tree.xpath("//tr[@class='Even']"):
    #         ip = parse_ip("".join(tr.xpath('./td[1]/script/text()')).strip())
    #         port = "".join(tr.xpath('./td[2]/text()')).strip()
    #         if ip:
    #             yield "%s:%s" % (ip, port)

    @staticmethod
    def freeProxy05(page_count=50): #max=4939
        """ 快代理 https://www.kuaidaili.com """
        url_pattern = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]
        url_list = []
        for page_index in range(1, page_count + 1):
            for pattern in url_pattern:
                url_list.append(pattern.format(page_index))

        for url in url_list:
            tree = WebRequest().get(url).tree
            proxy_list = tree.xpath('.//table//tr')
            sleep(1)  # 必须sleep 不然第二条请求不到数据
            for tr in proxy_list[1:]:
                yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def freeProxy06(): #max=0
        """ FateZero http://proxylist.fatezero.org/ """
        url = "http://proxylist.fatezero.org/proxy.list"
        try:
            resp_text = WebRequest().get(url).text
            for each in resp_text.split("\n"):
                json_info = json.loads(each)
                if json_info.get("country") == "CN":
                    yield "%s:%s" % (json_info.get("host", ""), json_info.get("port", ""))
        except Exception as e:
            print(e)

    @staticmethod
    def freeProxy07(page_count=7): #max=7
        """ 云代理 """
        for i in range(1,page_count+1):
            urls = ['http://www.ip3366.net/free/?stype=1&page={}'.format(i), "http://www.ip3366.net/free/?stype=2?page={}".format(i)]
            for url in urls:
                r = WebRequest().get(url, timeout=10)
                proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
                for proxy in proxies:
                    yield ":".join(proxy)

    # @staticmethod
    # def freeProxy08():
    #     """ 小幻代理 """
    #     urls = ['https://ip.ihuan.me/address/5Lit5Zu9.html']
    #     for url in urls:
    #         r = WebRequest().get(url, timeout=10)
    #         proxies = re.findall(r'>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</a></td><td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ":".join(proxy)

    @staticmethod
    def freeProxy09(page_count=2):#max=2
        """ 免费代理库 """
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?country=中国&page={}'.format(i)
            html_tree = WebRequest().get(url).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()

    @staticmethod
    def freeProxy10(page_count=10): #max=18
        """ 89免费代理 """
        for i in range(1, page_count + 1):
            r = WebRequest().get("https://www.89ip.cn/index_{}.html".format(i), timeout=10)
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)

    # @staticmethod
    # def wallProxy01():
    #     """
    #     PzzQz https://pzzqz.com/
    #     """
    #     from requests import Session
    #     from lxml import etree
    #     session = Session()
    #     try:
    #         index_resp = session.get("https://pzzqz.com/", timeout=20, verify=False).text
    #         x_csrf_token = re.findall('X-CSRFToken": "(.*?)"', index_resp)
    #         if x_csrf_token:
    #             data = {"http": "on", "ping": "3000", "country": "cn", "ports": ""}
    #             proxy_resp = session.post("https://pzzqz.com/", verify=False,
    #                                       headers={"X-CSRFToken": x_csrf_token[0]}, json=data).json()
    #             tree = etree.HTML(proxy_resp["proxy_html"])
    #             for tr in tree.xpath("//tr"):
    #                 ip = "".join(tr.xpath("./td[1]/text()"))
    #                 port = "".join(tr.xpath("./td[2]/text()"))
    #                 yield "%s:%s" % (ip, port)
    #     except Exception as e:
    #         print(e)

    # @staticmethod
    # def freeProxy10():
    #     """
    #     墙外网站 cn-proxy
    #     :return:
    #     """
    #     urls = ['http://cn-proxy.com/', 'http://cn-proxy.com/archives/218']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)

    # @staticmethod
    # def freeProxy11():
    #     """
    #     https://proxy-list.org/english/index.php
    #     :return:
    #     """
    #     urls = ['https://proxy-list.org/english/index.php?p=%s' % n for n in range(1, 10)]
    #     request = WebRequest()
    #     import base64
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r"Proxy\('(.*?)'\)", r.text)
    #         for proxy in proxies:
    #             yield base64.b64decode(proxy).decode()

    # @staticmethod
    # def freeProxy12():
    #     urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1']
    #     request = WebRequest()
    #     for url in urls:
    #         r = request.get(url, timeout=10)
    #         proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
    #         for proxy in proxies:
    #             yield ':'.join(proxy)


if __name__ == '__main__':
    p = ProxyFetcher()
    for _ in p.freeProxy07():
        print(_)

# http://nntime.com/proxy-list-01.htm
