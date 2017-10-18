import json

import time

import re
from lxml import etree
from proxypool.setting import TESTER_CYCLE

from .utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = get_page(start_url)
        ip_adress = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        # \s* 匹配空格，起到换行作用
        re_ip_adress = ip_adress.findall(html)
        for adress, port in re_ip_adress:
            result = adress + ':' + port
            yield result.replace(' ', '')

    def crawl_xicidaili(self):
        for page in range(1, 4):
            start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile(
                '<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_ip3366(self):
        for page in range(1, 4):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_proxy360(self):
        start_url = 'http://www.proxy360.cn/Region/China'
        print('Crawling', start_url)
        html = get_page(start_url)
        if html:
            doc = pq(html)
            lines = doc('div[name="list_proxy_ip"]').items()
            for line in lines:
                ip = line.find('.tbBottomLine:nth-child(1)').text()
                port = line.find('.tbBottomLine:nth-child(2)').text()
                yield ':'.join([ip, port])

    def crawl_goubanjia(self):
        start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '')

    def crawl_data5u(self):
        for i in ['gngn', 'gnpt']:
            start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile(
                ' <ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_kxdaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kxdaili.com/ipList/{}.html#ip'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_premproxy(self):
        for i in ['China-01', 'China-02', 'China-03', 'China-04', 'Taiwan-01']:
            start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(i)
            html = get_page(start_url)
            if html:
                ip_adress = re.compile('<td data-label="IP:port ">(.*?)</td>')
                re_ip_adress = ip_adress.findall(html)
                for adress_port in re_ip_adress:
                    yield adress_port.replace(' ', '')

    def crawl_xroxy(self):
        for i in ['CN', 'TW']:
            start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(i)
            html = get_page(start_url)
            if html:
                ip_adress1 = re.compile("title='View this Proxy details'>\s*(.*).*")
                re_ip_adress1 = ip_adress1.findall(html)
                ip_adress2 = re.compile("title='Select proxies with port number .*'>(.*)</a>")
                re_ip_adress2 = ip_adress2.findall(html)
                for adress, port in zip(re_ip_adress1, re_ip_adress2):
                    adress_port = adress + ':' + port
                    yield adress_port.replace(' ', '')

    # def crawl_xicidaili(self):
    #     """
    #     获取xicidaili
    #     :return:
    #     """
    #     start_url = 'http://www.xicidaili.com/nn/'
    #     html = get_page(start_url)
    #     if html:
    #         selector = etree.HTML(html)
    #         tds = selector.xpath('//table[@id="ip_list"]')[0]  # .xpath('/*')
    #         for index in range(1, len(tds)):
    #            # print('{0}   {1}'.format(tds[index], type(tds[index])))
    #             # print(etree.tostring(tds[index]))
    #             yield  '{0}:{1}'.format(tds[index].xpath('./td')[1].xpath('./text()')[0],tds[index].xpath('./td')[2].xpath('./text()')[0])
    #
    #
    # def crawl_xicidaili(self):
    #     """
    #     获取xicidaili
    #     :return:
    #     """
    #     for i in range(2,3):
    #         start_url = 'http://www.xicidaili.com/nt/{0}'.format(i)
    #         html = get_page(start_url)
    #         if html:
    #             selector = etree.HTML(html)
    #             tds = selector.xpath('//table[@id="ip_list"]')[0]  # .xpath('/*')
    #             for index in range(1, len(tds)):
    #                # print('{0}   {1}'.format(tds[index], type(tds[index])))
    #                 # print(etree.tostring(tds[index]))
    #                 yield  '{0}:{1}'.format(tds[index].xpath('./td')[1].xpath('./text()')[0],tds[index].xpath('./td')[2].xpath('./text()')[0])