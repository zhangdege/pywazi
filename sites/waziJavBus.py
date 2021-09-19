import re
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from mods.waziURL import waziURL
from mods.waziRequest import waziRequest

class waziJavBus:
    # JavBus is a website that collects adult video's magnet url schemes. (Almost from Japan)
    # JavBus 是一个收集成人视频的种子网站。（大部分来自日本）
    # [1]
    def __init__(self):
        super(waziJavBus, self).__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.164 Safari/537.36",
            "Host": "www.javbus.com",
            "Connection": "close",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.proxies = {
            "proxyAddress": "127.0.0.1",
            "proxyPort": "7890"
        }
        self.URL = waziURL()
        self.request = waziRequest()
        self.url = "https://www.javbus.com/"
        self.apiUrl = "https://www.javbus.com/"
        self.useDomain = True
        self.params = {}

    def giveParams(self, params):
        self.params = params
        return self.params

    def customUrl(self, url):
        self.url = url
        return self.url

    def useDomainApi(self, boolean):
        self.useDomain = boolean
        return self.useDomain

    def getAjax(self, avId):
        url = urllib.parse.urljoin(self.url, avId)
        tempHeaders = self.headers
        tempHeaders["Referer"] = url
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "get", url, tempHeaders, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams).data.decode("utf-8"), "lxml")
        html = soup.prettify()
        imgPattern = re.compile(r"var img = '.*?'")
        match = imgPattern.findall(html)
        img = match[0].replace("var img = '", "").replace("'", "")
        ucPattern = re.compile(r"var uc = .*?;")
        match = ucPattern.findall(html)
        uc = match[0].replace("var uc = ", "").replace(";", "")
        gidPattern = re.compile(r"var gid = .*?;")
        match = gidPattern.findall(html)
        gid = match[0].replace("var gid = ", "").replace(";", "")
        params = {
            "gid": gid,
            "lang": "zh",
            "img": img,
            "uc": uc
        }
        if self.useDomain:
            return self.URL.getFullURL(self.apiUrl, params)
        else:
            return self.URL.getFullURL(self.url, params)

    def getMagnet(self, avId):
        ajaxUrl = waziJavBus.getAjax(self, avId)
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "get", ajaxUrl, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams).data.decode("utf-8"), "lxml")
        avLists = []
        avDist = {"title": "", "magnet": "", "size": "", "date": ""}
        for tr in soup.find_all("tr"):
            i = 0
            for td in tr:
                if td.string:
                    continue
                i += 1
                avDist["magnet"] = td.a["href"]
                if i % 3 == 1:
                    avDist["title"] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
                if i % 3 == 2:
                    avDist["size"] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
                if i % 3 == 0:
                    avDist["date"] = td.a.text.replace(" ", "").replace("\t", "").replace("\r\n", "")
                    avLists.append(avDist)
        return avLists
