"""
Program for crawling web resources.
See Readme.md for more details.

爬取网络资源的程序。
详情请看 Readme.md。

Because of I can't use Requests for no reason, so I use Urllib.

Sometimes my thinking is confusing and I don't follow PEP 8,
so part of the code you may not be able to read,
if you have questions you can talk to me or modify it yourself.

不知为何我用不了 Requests 库，所以只能用 Urllib。

有时候我的想法比较混乱，并且我不遵守 PEP 8，
所以部分代码你可能看不懂。
如果你有问题的话，可以找我谈谈或者自己修改一下。

The current version is for highly technical users.
being the first to engage PyWazi at the earliest point in the development cycle,
using code that has not yet been completed and tested.
will suffer from numerous shortcomings and low stability and efficiency.
The open source projects used are not yet specified and the development documentation is not yet published.
Please wait for the project to be completed before
I will announce it again, it's just a project to occupy the pit now.
Of course, do not rule out the possibility of deleting the project at any time.

目前的版本适合高度技术性用户，
率先使用尚未完成和测试的代码在开发周期中最早参与 PyWazi，
将会存在大量不足之处和低稳定性和效率，
并且还未注明使用的开源项目和公布开发文档。
请等待项目完工之后，
我再公布，现在就一占坑项目。
当然，不排除随时删除项目的可能性。
"""

import os
import re
import hmac
import json
import time
import uuid
import hashlib
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup

class waziRequest:
    # I advise you not to figure out this class I wrote,
    # because it will be very painful for you.
    # It's enough that I know exactly what I'm writing.
    # Thank you for your cooperation.
    #
    # 我劝你别搞懂我写的这个类，
    # 这会让你感到非常痛苦的。
    # 我清楚我写的是啥就足够了。
    # 谢谢你的配合。
    def __init__(self):
        super(waziRequest, self).__init__()
        self.isUseProxies = True
        self.proxies = {}
        self.isUseHeaders = False
        self.headers = {
            "User-Agent": "Use Your UA.",
        }

    def useProxies(self, isUse):
        self.isUseProxies = isUse
        return self.isUseProxies

    def editProxies(self, https, port):
        if https is None or port is None:
            self.proxies["https"] = None
        else:
            self.proxies["https"] = https + ":" + str(port)
        return self.proxies

    def useHeaders(self, isUse):
        self.isUseHeaders = isUse
        return self.isUseHeaders

    def editHeaders(self, key, value):
        self.headers[key] = value
        return self.headers

    def overWriteHeaders(self, headers):
        self.headers = headers
        return self.headers

    def delHeaders(self, key):
        self.headers.pop(key)
        return self.headers

    # If your domain has some Chinese or something else, you have to encode your url first.
    # 如果你的域名中带有中文或其他字符，你必须得先编码你的 URL。
    def get(self, url):
        if self.useProxies:
            proxy = urllib.request.ProxyHandler(self.proxies)
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
        if self.useHeaders:
            request = urllib.request.Request(url = url, headers = self.headers)
        else:
            request = urllib.request.Request(url = url)
        return urllib.request.urlopen(request)

    def post(self, url, data):
        if self.useProxies:
            proxy = urllib.request.ProxyHandler(self.proxies)
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
        if self.useHeaders:
            # Sometimes(like some JSON Data), you have to json.dumps(yourData).encode() to request.
            # 有时候（比如面对某些 JSON 数据），你必须得先 json.dumps(你数据).encode() 才能发送请求。
            request = urllib.request.Request(url = url, headers = self.headers, data = data)
        else:
            request = urllib.request.Request(url = url)
        return urllib.request.urlopen(request)

    def do(self, params):
        waziRequest.useProxies(self, params["useProxies"])
        waziRequest.useHeaders(self, params["useHeaders"])
        if params["useProxies"]:
            waziRequest.editProxies(self, params["proxyAddress"], params["proxyPort"])
        if params["useHeaders"]:
            waziRequest.overWriteHeaders(self, params["headers"])
        if params["method"].lower() == "get":
            return waziRequest.get(self, params["url"])
        elif params["method"].lower() == "post":
            return waziRequest.post(self, params["url"], params["data"])
        else:
            return "Sorry, method must be get or post. / 对不起，模式一定得是 GET 或者 POST 呜呜呜。"

    def handleParams(self, params, method, url, deHeaders, deProxies):
        temp = {}
        if "useProxies" in params:
            temp["useProxies"] = params["useProxies"]
        else:
            temp["useProxies"] = False
        if "useHeaders" in params:
            temp["useHeaders"] = params["useHeaders"]
        else:
            temp["useHeaders"] = False
        if temp["useHeaders"]:
            if "headers" in params:
                temp["headers"] = params["headers"]
            else:
                if deHeaders is None:
                    temp["headers"] = self.headers
                else:
                    temp["headers"] = deHeaders
        if temp["useProxies"]:
            if "proxyAddress" in params:
                temp["proxyAddress"] = params["proxyAddress"]
            else:
                if deProxies is None:
                    temp["proxyAddress"] = "None"
                else:
                    temp["proxyAddress"] = deProxies["proxyAddress"]
            if "proxyPort" in params:
                temp["proxyPort"] = params["proxyPort"]
            else:
                if deProxies is None:
                    temp["proxyPort"] = "None"
                else:
                    temp["proxyPort"] = deProxies["proxyPort"]

        temp.update(method = method, url = url)
        return temp

class waziCheck:
    # Separate checksum and crypto system for ExHentai search and PicAcg encryption and decryption processing.
    # 单独的校验和密码系统，针对 ExHentai 的搜索和 PicAcg 的加解密处理。
    def __init__(self):
        super(waziCheck, self).__init__()
        self.sha1 = hashlib.sha1()
        self.tags = [
            "Doujinshi",
            "Manga",
            "Artist CG",
            "Game CG",
            "Western",
            "Non-H",
            "Image Set",
            "Cosplay",
            "Asian Porn",
            "Misc"
        ]
        self.tagsNumber = {
            "Doujinshi": 2,
            "Manga": 4,
            "Artist CG": 8,
            "Game CG": 16,
            "Western": 512,
            "Non-H": 256,
            "Image Set": 32,
            "Cosplay": 64,
            "Asian Porn": 128,
            "Misc": 1
        }
        self.empty = ""

    def getFileSHA1(self, path):
        self.sha1 = hashlib.sha1()
        temp = open(path, "rb")
        while True:
            temp2 = temp.read(128000)
            self.sha1.update(temp2)
            if not temp2:
                break
        temp.close()
        return self.sha1.hexdigest()

    def getSources(self, params):
        # You can see the values corresponding to all tags in table.itc of ExHentai,
        # and the calculation method in ehg_index.c.js.
        # 在 ExHentai 的 table.itc 中可以看到所有标签对应的数值，
        # 在 ehg_index.c.js 中可以看到计算方法。
        giveTags = [item for item in self.tags if item not in set(params["cats"])]
        if len(giveTags) == 0:
            sources = 0
        else:
            calc = 0
            for i in giveTags:
                calc = calc | int(self.tagsNumber[i])
            sources = calc
        return sources

    def signature(self, url, times, method, baseUrl, uuids, apiKey, secretKey):
        self.empty = ""
        raw = url.replace(baseUrl, "") + str(times) + uuids + method + apiKey
        raw = raw.lower()
        hc = hmac.new(secretKey.encode(), digestmod = hashlib.sha256)
        hc.update(raw.encode())
        return hc.hexdigest()

    def construct(self, url, method, baseUrl, uuids, apiKey, secretKey):
        self.empty = ""
        times = int(time.time())
        sig = waziCheck.signature(self, url, times, method, baseUrl, uuids, apiKey, secretKey)
        return [sig, times]

class waziDanbooru:
    # Danbooru is a powerful image board system which uses tagging extensively.
    # like https://yande.re/ https://konachan.com/ (R-18 NSFW)
    # Danbooru 是一个非常牛逼的画廊展示系统（相册图库差不多吧），主要就是用标签多一点。
    # 像 https://yande.re/ https://konachan.com/ （R-18 不适合在公开场合或工作环境浏览）
    def __init__(self):
        super(waziDanbooru, self).__init__()
        self.request = waziRequest()
        self.api = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.164 Safari/537.36"
        }
        self.proxies = {
            "proxyAddress": "127.0.0.1",
            "proxyPort": "7890"
        }
        self.params = {}

    def giveParams(self, params):
        self.params = params
        return self.params

    def setApi(self, url):
        self.api = url
        return self.api

    def getPosts(self, page, tags):
        url = urllib.parse.urljoin(self.api, "/post.json?page" + str(page) + "&tags=" + urllib.parse.quote(tags))
        tempParams = self.request.handleParams(self.params, "get", url, self.headers, self.proxies)
        return json.loads(self.request.do(tempParams).read())

    def downloadPosts(self, page, tags, path):
        lists = waziDanbooru.getPosts(self, page, tags)
        isExists = os.path.exists(path)
        downloadFiles = []
        if not isExists:
            os.makedirs(path)
        for i in lists:
            requestParams = self.request.handleParams(self.params, "get", i["file_url"], self.headers, self.proxies)
            # os.path.split is bad here. (Can't get filename extension)
            # os.path.split 在这里是坏的。 (无法获取文件扩展名）
            fileName = os.path.join(path, str(i["id"]) + "." + i["file_url"].split(".")[-1])
            with open(fileName, "wb") as f:
                f.write(self.request.do(requestParams).read())
            downloadFiles.append(fileName)
        return downloadFiles

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
        soup = BeautifulSoup(self.request.do(requestParams), "lxml")
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
        if self.useDomain:
            return urllib.parse.urljoin(self.apiUrl,
                                        "ajax/uncledatoolsbyajax.php?gid=" + gid + "&lang=zh&img=" + img + "&uc=" + uc)
        else:
            return urllib.parse.urljoin(self.url,
                                        "ajax/uncledatoolsbyajax.php?gid=" + gid + "&lang=zh&img=" + img + "&uc=" + uc)

    def getMagnet(self, avId):
        ajaxUrl = waziJavBus.getAjax(self, avId)
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "get", ajaxUrl, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams), "lxml")
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

class waziExHentai:
    # ExHentai is the world's largest erotic homoerotic manga site.
    #
    # Before using this class,
    # you must ensure that your account's home page is displayed as Extended (perhaps other displays will work as well).
    #
    # Find some time to study the official API and rewrite my program.
    #
    # ExHentai 是全世界最大的色情同人志漫画网站。
    #
    # 在使用该类前，
    # 您必须确保您的账号的主页显示方式为 Extended（或许其他显示方式也能使程序正常运行）。
    #
    # 找个时间研究一下官方的 API，然后重写一下我的程序。
    def __init__(self):
        super(waziExHentai, self).__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.164 Safari/537.36",
            "Connection": "keep-alive",
            "Cookie": ""
        }
        self.proxies = {
            "proxyAddress": "127.0.0.1",
            "proxyPort": "7890"
        }
        self.request = waziRequest()
        self.urls = {
            "main": "https://exhentai.org/",
            "galleryTorrent": "https://exhentai.org/gallerytorrents.php?gid=",
            "api": "https://exhentai.org/api.php",
            "mpv": "https://exhentai.org/mpv/"
        }
        self.params = {}
        self.empty = ""     # Trash Code

    def giveParams(self, params):
        self.params = params
        return self.params

    def setCookies(self, cookies):
        self.headers["Cookie"] = cookies
        return self.headers["Cookie"]

    def getBooks(self, url):
        soup = waziExHentai.returnSoup(self, url)
        booksList = []
        urls = soup.find_all(class_ = "itg glte")[0].find_all(class_ = "gl2e")
        covers = soup.find_all(class_ = "itg glte")[0].find_all(class_ = "gl1e")
        coverTimes = -1
        for tempUrl in urls:
            coverTimes += 1
            tempBooks = {
                "title": tempUrl.find_all(class_ = "glink")[0].get_text(),
                "href": tempUrl.find_all("a", attrs = {"href": re.compile("/g/")})[0].attrs["href"],
                "bCats": tempUrl.find_all(class_ = "cn")[0].get_text(),
                "cover": covers[coverTimes].find_all("img")[0].attrs["src"]
            }
            booksList.append(tempBooks)
        return booksList

    def browse(self, page):
        url = self.urls["main"] + "?page=" + str(page)
        return waziExHentai.getBooks(self, url)

    def allBrowse(self, page):
        url = self.urls["main"] + "?page=" + str(page) + "&?f_cats=0&advsearch=1&f_sname=on&f_stags=on&f_sh=on&f_sdt2" \
                                                         "=on&f_sfl=on&f_sfu=on&f_sft=on&f_spf=&f_spt="
        return waziExHentai.getBooks(self, url)

    def search(self, page, text):
        url = self.urls["main"] + "?page=" + str(page) + "&f_search=" + urllib.parse.quote(text)
        return waziExHentai.getBooks(self, url)

    def allSearch(self, page, text):
        url = self.urls["main"] + "?page=" + str(
            page) + "&?f_cats=0&advsearch=1&f_sname=on&f_stags=on&f_sh=on&f_sdt2=on&f_sfl=on&f_sfu=on&f_sft=on" \
                    "&f_search=" + urllib.parse.quote(text)
        return waziExHentai.getBooks(self, url)

    def tagSearch(self, page, tag):
        url = self.urls["main"] + "tag/" + urllib.parse.quote(tag) + "/" + str(page)
        return waziExHentai.getBooks(self, url)

    def uploaderSearch(self, page, uploader):
        url = self.urls["main"] + "uploader/" + urllib.parse.quote(uploader) + "/" + str(page)
        return waziExHentai.getBooks(self, url)

    def uploaderAllSearch(self, page, uploader):
        url = self.urls["main"] + "?page=" + str(page) + "&f_cats=0&f_search=uploader%3A"
        url += urllib.parse.quote(uploader) + "&advsearch=1&f_sname=on&f_stags=on&f_sdt2=on&f_spf=&f_spt=&f_sfl=on"
        url += "&f_sfu=on&f_sft=on"
        return waziExHentai.getBooks(self, url)

    def advancedSearch(self, params):
        url = self.urls["main"]
        url += "?f_cats=" + str(waziCheck().getSources(params))
        if str(params["search"]):
            url += "&f_search=" + urllib.parse.quote(str(params["search"]))
        url += "&advsearch=1"
        if params["sgn"]:
            url += "&f_sname=on"
        if params["sgt"]:
            url += "&f_stags=on"
        if params["sgd"]:
            url += "&f_sdesc=on"
        if params["stf"]:
            url += "&f_storr=on"
        if params["osgwt"]:
            url += "&f_sto=on"
        if params["slpt"]:
            url += "&f_sdt1=on"
        if params["sdt"]:
            url += "&f_sdt2=on"
        if params["seg"]:
            url += "&f_sh=on"
        if params["mr"]:
            url += "&f_sr=on&f_srdd=" + str(params["mrs"])
        if params["b"]:
            url += "&f_sp=on&f_spf=" + str(params["b1"]) + "&f_spt=" + str(params["b2"])
        if params["dfl"]:
            url += "&f_sfl=on"
        if params["dfu"]:
            url += "&f_sfu=on"
        if params["dft"]:
            url += "&f_sft=on"
        url += "&page=" + str(params["page"])
        return waziExHentai.getBooks(self, url)

    def imageSearch(self, params):
        sha1 = ""
        if params["type"] == "sha1":
            sha1 = params["sha1"]
        if params["type"] == "file":
            sha1 = waziCheck().getFileSHA1(params["path"])
        url = self.urls["main"] + "?f_shash=" + sha1
        if params["similar"]:
            url += "&fs_similar=1"
        if params["cover"]:
            url += "&fs_covers=1"
        if params["exp"]:
            url += "&fs_exp=1"
        return waziExHentai.getBooks(self, url)

    def customSearch(self, params):
        url = self.urls["main"]
        if "cats" in params:
            url += "?f_cats=" + str(waziCheck().getSources(params))
        else:
            url += "?f_cats=0"
        url += "&f_search="
        if "uploaders" in params:
            for i in params["uploaders"]:
                url += "uploader:" + urllib.parse.quote(i) + "+"
            url = url[:-1]
        if "tags" in params:
            if "uploaders" in params:
                url += "+"
            for i in params["tags"]:
                url += urllib.parse.quote(i) + "+"
            url = url[:-1]
        if "text" in params:
            if "tags" in params:
                url += "+"
            url += urllib.parse.quote(params["text"])
        if "advanced" in params:
            url += "&advsearch=1"
            if "search" in params["advanced"]:
                if params["advanced"]["search"]["galleryName"]:
                    url += "&f_sname=on"
                elif not params["advanced"]["search"]["galleryName"]:
                    url += "&f_sname="
                else:
                    url = url
                if params["advanced"]["search"]["galleryTags"]:
                    url += "&f_stags=on"
                elif not params["advanced"]["search"]["galleryTags"]:
                    url += "&f_stags="
                else:
                    url = url
                if params["advanced"]["search"]["galleryDescription"]:
                    url += "&f_sdesc=on"
                elif not params["advanced"]["search"]["galleryDescription"]:
                    url += "&f_sdesc="
                else:
                    url = url
                if params["advanced"]["search"]["torrentFilenames"]:
                    url += "&f_storr=on"
                elif not params["advanced"]["search"]["torrentFilenames"]:
                    url += "&f_storr="
                else:
                    url = url
                if params["advanced"]["search"]["low-powerTags"]:
                    url += "&f_sdt1=on"
                elif not params["advanced"]["search"]["low-powerTags"]:
                    url += "&f_sdt1="
                else:
                    url = url
                if params["advanced"]["search"]["downvotedTags"]:
                    url += "&f_sdt2=on"
                elif not params["advanced"]["search"]["downvotedTags"]:
                    url += "&f_sdt2="
                else:
                    url = url
                if params["advanced"]["search"]["expungedGalleries"]:
                    url += "&f_sh=on"
                elif not params["advanced"]["search"]["expungedGalleries"]:
                    url += "&f_sh="
                else:
                    url = url
            if "limit" in params["advanced"]:
                if params["advanced"]["limit"]["onlyShowGalleriesWithTorrents"]:
                    url += "&f_sto=on"
                elif not params["advanced"]["limit"]["onlyShowGalleriesWithTorrents"]:
                    url += "&f_sto="
                else:
                    url = url
                if params["advanced"]["limit"]["minimumRating"]:
                    url += "&f_sr=on&f_srdd=" + str(params["advanced"]["limit"]["minimumRatingNumber"])
                elif not params["advanced"]["limit"]["minimumRating"]:
                    url += "&f_sr=&f_srdd="
                else:
                    url = url
                if params["advanced"]["limit"]["between"]:
                    url += "&f_sp=on&f_spf=" + str(params["advanced"]["limit"]["betweenPages"][0])
                    url += "&f_spt=" + str(params["advanced"]["limit"]["betweenPages"][1])
                elif not params["advanced"]["limit"]["between"]:
                    url += "&f_sp=&f_spf=&f_spt="
                else:
                    url = url
            if "disableFilters" in params["advanced"]:
                if params["advanced"]["disableFilters"]["language"]:
                    url += "&f_sfl=on"
                elif not params["advanced"]["disableFilters"]["language"]:
                    url += "&f_sfl="
                else:
                    url = url
                if params["advanced"]["disableFilters"]["uploader"]:
                    url += "&f_sfu=on"
                elif not params["advanced"]["disableFilters"]["uploader"]:
                    url += "&f_sfu="
                else:
                    url = url
                if params["advanced"]["disableFilters"]["tags"]:
                    url += "&f_sft=on"
                elif not params["advanced"]["disableFilters"]["tags"]:
                    url += "&f_sft="
                else:
                    url = url
        if "file" in params:
            if "main" in params["file"]:
                if "type" in params["file"]["main"]:
                    if params["file"]["main"]["type"] == "path":
                        url += "&f_shash=" + waziCheck().getFileSHA1(params["file"]["main"]["value"])
                    elif params["file"]["main"]["type"] == "sha1":
                        url += "&f_shash=" + params["file"]["main"]["value"]
                    else:
                        url = url
            if "options" in params["file"]:
                if params["file"]["options"]["useSimilarityScan"]:
                    url += "&fs_similar=1"
                elif not params["file"]["options"]["useSimilarityScan"]:
                    url += "&fs_similar="
                else:
                    url = url
                if params["file"]["options"]["onlySearchCovers"]:
                    url += "&fs_covers=1"
                elif not params["file"]["options"]["onlySearchCovers"]:
                    url += "&fs_covers="
                else:
                    url = url
                if params["file"]["options"]["showExpunged"]:
                    url += "&fs_exp=1"
                elif not params["file"]["options"]["showExpunged"]:
                    url += "&fs_exp="
                else:
                    url = url
        return waziExHentai.getBooks(self, url)

    def returnSoup(self, link):
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "get", link, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams).read(), "lxml")
        return soup

    def getTorrent(self, link):
        url = self.urls["galleryTorrent"] + link.split("/")[4] + "&t=" + link.split("/")[5]
        soup = waziExHentai.returnSoup(self, url)
        torrents = []
        try:
            tempNum = len(soup.find_all("a")) - 1
        except:
            return {"Error": "None"}
        else:
            for tempInfo in range(tempNum):
                tempList = {
                    "time": soup.find_all("table")[tempInfo].tr.find_all("td")[0].get_text().split("Posted: ")[1],
                    "size": soup.find_all("table")[tempInfo].tr.find_all("td")[1].get_text().split("Size: ")[1],
                    "seeds": soup.find_all("table")[tempInfo].tr.find_all("td")[3].get_text().split("Seeds: ")[1],
                    "peers": soup.find_all("table")[tempInfo].tr.find_all("td")[4].get_text().split("Peers: ")[1],
                    "total": soup.find_all("table")[tempInfo].tr.find_all("td")[5].get_text().split("Downloads: ")[1],
                    "link": soup.find_all("table")[tempInfo].find_all("tr")[2].a.attrs["href"],
                    "name": soup.find_all("table")[tempInfo].find_all("tr")[2].a.get_text()
                }
                torrents.append(tempList)
        return torrents

    def getInfo(self, link):
        soup = waziExHentai.returnSoup(self, link)
        tags = []
        for tag in soup.find_all(id = "taglist")[0].find_all("a"):
            tags.append(tag.attrs["onclick"].split("'")[1])
        info = {
            "title": soup.h1.get_text(),
            "jTitle": soup.find_all(id = "gj")[0].get_text(),
            "cats": soup.find_all(id = "gdc")[0].div.get_text(),
            "tags": tags,
            "time": soup.find_all(class_ = "gdt2")[0].get_text(),
            "father": soup.find_all(class_ = "gdt2")[1].get_text(),
            "viewable": soup.find_all(class_ = "gdt2")[2].get_text(),
            "language": soup.find_all(class_ = "gdt2")[3].get_text().split(" \xa0")[0],
            "size": soup.find_all(class_ = "gdt2")[4].get_text(),
            "pages": soup.find_all(class_ = "gdt2")[5].get_text(),
            "favTimes": soup.find_all(class_ = "gdt2")[6].get_text(),
            "uploader": soup.find_all(id = "gdn")[0].a.get_text(),
            "rate": soup.find_all(id = "rating_label")[0].get_text().split("Average: ")[1],
            "cover": soup.find_all(id = "gd1")[0].div.attrs["style"].split("(")[1].split(")")[0]
        }
        return info

    def getComments(self, link):
        soup = waziExHentai.returnSoup(self, link)
        comments = []
        for i in soup.find_all(id = "cdiv")[0].find_all(class_ = "c1"):
            htmlComments = i.find_all(class_="c6")[0].prettify()
            start = re.findall("<div.*?>", i.find_all(class_ = "c6")[0].prettify())[0]
            htmlComments = htmlComments.replace(start, "")
            htmlComments = htmlComments.replace("</div>", "")
            try:
                i.find(class_ = "c5 nosel").span.get_text()
            except:
                scores = "None / 不适用"
            else:
                scores = i.find(class_ = "c5 nosel").span.get_text()
            tempComments = {
                "time": i.find(class_ = "c3").get_text().split(" by:")[0].split("Posted on ")[1],
                "uploader": i.find(class_ = "c3").a.attrs["href"],
                "uploaderName": i.find(class_ = "c3").a.get_text(),
                "scores": scores,
                "htmlComments": htmlComments
            }
            comments.append(tempComments)
        return comments

    def apiInfo(self, link):
        headers = {
            "Content-Type": "application/json",
            "Cookie": self.headers["Cookie"]
        }
        body = {
            "method": "gdata",
            "gidlist": [
                [link.split("/")[4], link.split("/")[5]]
            ],
            "namespace": 1
        }
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "post", self.urls["api"], headers, self.proxies)
        requestParams["data"] = json.dumps(body).encode()
        return json.loads(self.request.do(requestParams).read())

    def getPages(self, link):
        soup = waziExHentai.returnSoup(self, link)
        try:
            pages = int(soup.find_all(class_ = "ptt")[0].find_all("a")[-2].get_text())
        except:
            return 0
        else:
            return pages

    def parseSoupForLargeThumbnails(self, soup):
        self.empty = ""
        thumbnails = []
        for i in soup.find(id = "gdt").find_all(class_ = "gdtl"):
            tempThumbnails = {
                "url": i.a.img.attrs["src"],
                "style": i.attrs["style"],
                "alt": i.a.img.attrs["alt"],
                "title": i.a.img.attrs["title"],
                "text": i.a.get_text()
            }
            thumbnails.append(tempThumbnails)
        return thumbnails

    def getLargeThumbnails(self, link):
        soup = waziExHentai.returnSoup(self, link)
        page = waziExHentai.getPages(self, link)
        thumbnails = []
        if page == 0:
            return waziExHentai.parseSoupForLargeThumbnails(self, soup)
        else:
            for i in range(page + 1):
                url = link + "?p=" + str(i)
                soup = waziExHentai.returnSoup(self, url)
                thumbnails.append(waziExHentai.parseSoupForLargeThumbnails(self, soup))
            return thumbnails

    def parseSoupForNormalThumbnails(self, soup):
        self.empty = ""
        thumbnails = []
        for i in soup.find_all(class_ = "gdtm"):
            tempThumbnails = {
                "style": i.attrs["style"],
                "divMargin": i.div.attrs["style"].split("margin:")[1].split(";")[0],
                "divWidth": i.div.attrs["style"].split("width:")[1].split(";")[0],
                "divHeight": i.div.attrs["style"].split("height:")[1].split(";")[0],
                "url": i.div.attrs["style"].split("url(")[1].split(")")[0],
                "transparent": i.div.attrs["style"].split(") ")[1],
                "imgAlt": i.div.a.img.attrs["alt"],
                "imgTitle": i.div.a.img.attrs["title"],
                "imgWidth": i.div.a.img.attrs["style"].split("width:")[1].split(";")[0],
                "imgHeight": i.div.a.img.attrs["style"].split("height:")[1].split(";")[0],
                "imgMargin": i.div.a.img.attrs["style"].split("margin:")[1]
            }
            thumbnails.append(tempThumbnails)
        return thumbnails

    def getNormalThumbnails(self, link):
        soup = waziExHentai.returnSoup(self, link)
        page = waziExHentai.getPages(self, link)
        thumbnails = []
        if page == 0:
            return waziExHentai.parseSoupForNormalThumbnails(self, soup)
        else:
            for i in range(page + 1):
                url = link + "?p=" + str(i)
                soup = waziExHentai.returnSoup(self, url)
                thumbnails.append(waziExHentai.parseSoupForNormalThumbnails(self, soup))
            return thumbnails

    def getTitle(self, link, params):
        if params["japanese"]:
            title = waziExHentai.getInfo(self, link)["jTitle"]
        else:
            title = waziExHentai.getInfo(self, link)["title"]
        title.strip().rstrip("\\")
        return title

    def createFolder(self, link, params):
        title = waziExHentai.getTitle(self, link, params)
        isExists = os.path.exists(os.path.join(params["path"], title))
        if not isExists:
            os.makedirs(os.path.join(params["path"], title))

    def getMPVImages(self, link, method, params = None):
        mpvUrl = self.urls["mpv"] + link.split("/")[4] + "/" + link.split("/")[5]
        post = {
            "method": "imagedispatch",
            "gid": int(link.split("/")[4]),
            "page": "",
            "imgkey": "",
            "mpvkey": ""
        }
        soup = waziExHentai.returnSoup(self, mpvUrl)
        scripts = str(soup.find_all("script")[1]).split("<script type=\"text/javascript\">")[1].split("</script>")[0]
        imgLists = eval(scripts.split("var imagelist = ")[1].split(";")[0])
        mpvkey = scripts.split("mpvkey = \"")[1].split("\"")[0]
        mpvLists = []
        tempParams = self.params
        tempParams["useHeaders"] = True
        tempHeaders = self.headers
        tempHeaders["Content-Type"] = "application/json"
        title = waziExHentai.getTitle(self, link, params)
        if method == "download":
            waziExHentai.createFolder(self, link, params)
        i = 0
        for dic in imgLists:
            i += 1
            post["page"] = i
            post["imgkey"] = dic["k"]
            post["mpvkey"] = mpvkey
            requestParams = self.request.handleParams(tempParams, "post", self.urls["api"], tempHeaders, self.proxies)
            requestParams["data"] = json.dumps(post).encode()
            lists = json.loads(str(self.request.do(requestParams).read(), encoding = "utf-8"))
            if method == "get":
                mpvLists.append({
                    "name": dic["n"],
                    "url": lists["i"]
                })
            if method == "download":
                requestParams = self.request.handleParams(tempParams, "get", lists["i"], self.headers, self.proxies)
                with open(os.path.join(params["path"], title, dic["n"]), "wb") as f:
                    f.write(self.request.do(requestParams).read())
                mpvLists.append(os.path.join(params["path"], title, dic["n"]))
        return mpvLists

    def getImages(self, soup, method, title, params = None):
        waziTick = 0
        images = []
        tempParams = self.params
        tempParams["useHeaders"] = True
        pics = soup.find_all(id = "gdt")[0].find_all("a")
        for pic in pics:
            waziTick += 1
            href = pic["href"]
            soup = waziExHentai.returnSoup(self, href)
            src = soup.find_all(id = "img")[0].attrs["src"]
            if method == "get":
                images.append(src)
            if method == "download":
                requestParams = self.request.handleParams(tempParams, "get", src, self.headers, self.proxies)
                with open(os.path.join(params["path"], title, src.split("/")[-1]), "wb") as f:
                    f.write(self.request.do(requestParams).read())
                images.append(os.path.join(params["path"], title, src.split("/")[-1]))
        return images

    def getNormalImages(self, link, method, params = None):
        title = waziExHentai.getTitle(self, link, params)
        normalImages = []
        if method == "download":
            waziExHentai.createFolder(self, link, params)
        page = waziExHentai.getPages(self, link)
        if page == 0:
            soup = waziExHentai.returnSoup(self, link)
            return waziExHentai.getImages(self, soup, method, title, params)
        else:
            for i in range(page + 1):
                url = link + "?p=" + str(i)
                soup = waziExHentai.returnSoup(self, url)
                normalImages.append(waziExHentai.getImages(self, soup, method, title, params))
            return normalImages

    def getArchivesHATH(self, link):
        soup = waziExHentai.returnSoup(self, link)
        url = soup.find_all(class_ = "g2 gsp")[0].a.attrs["onclick"].split("'")[1]
        soup = waziExHentai.returnSoup(self, url)
        archiveLists = []
        tempParams = self.params
        tempParams["useHeaders"] = True
        action = soup.find_all("form")[0].attrs["action"]
        for i in soup.find_all("td"):
            if i.find_all("p")[1].get_text() == "N/A":
                archiveTemp = {
                    "sample": i.find_all("p")[0].get_text(),
                    "size": i.find_all("p")[1].get_text(),
                    "cost": i.find_all("p")[2].get_text(),
                    "code": "N/A",
                    "url": "N/A"
                }
                archiveLists.append(archiveTemp)
            else:
                archiveTemp = {
                    "sample": i.find_all("p")[0].get_text(),
                    "size": i.find_all("p")[1].get_text(),
                    "cost": i.find_all("p")[2].get_text(),
                    "code": i.find_all("p")[0].a.attrs["onclick"].split("'")[1],
                    "url": action
                }
                archiveLists.append(archiveTemp)
        return archiveLists

    def toHATH(self, link, code):
        forms = {
            "hathdl_xres": code
        }
        forms = urllib.parse.urlencode(forms).encode("utf-8")
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "post", link, self.headers, self.proxies)
        requestParams["data"] = forms
        try:
            self.request.do(requestParams)
        except:
            return "Error, check your cookies and something balabala. / 错误，请检查你的 Cookies 或者其他乱七八糟的东西。"
        else:
            return "Done! / 完成！"

    def parseArchives(self, form, action):
        tempParams = self.params
        tempParams["useHeaders"] = True
        forms = urllib.parse.urlencode(form).encode("utf-8")
        requestParams = self.request.handleParams(tempParams, "post", action, self.headers, self.proxies)
        requestParams["data"] = forms
        soup = BeautifulSoup(self.request.do(requestParams), "lxml")
        tempUrl = soup.find_all("script")[0]
        tempUrl = str(tempUrl).split("document.location = \"")[1].split("\";")[0]
        requestParams = self.request.handleParams(tempParams, "get", tempUrl, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams), "lxml")
        href = soup.find_all("a")[0].attrs["href"]
        downloadLink = urllib.parse.urljoin(tempUrl, href)
        return downloadLink

    def getArchives(self, link):
        soup = waziExHentai.returnSoup(self, link)
        url = soup.find_all(class_="g2 gsp")[0]
        url = url.a.attrs["onclick"].split("'")[1]
        soup = waziExHentai.returnSoup(self, url)
        twoLists = []
        tempParams = self.params
        tempParams["useHeaders"] = True
        action = soup.find_all("form")[0].attrs["action"]
        orgForms = {
            "dltype": "org",
            "dlcheck": "Download Original Archive"
        }
        resForms = {
            "dltype": "res",
            "dlcheck": "Download Resample Archive"
        }
        orgExist = "disabled" in soup.find_all("form")[0].div.input.attrs
        resExist = "disabled" in soup.find_all("form")[1].div.input.attrs
        if not orgExist:
            temp = {
                "type": "original",
                "link": waziExHentai.parseArchives(self, orgForms, action)
            }
            twoLists.append(temp)
        if not resExist:
            temp = {
                "type": "resample",
                "link": waziExHentai.parseArchives(self, resForms, action)
            }
            twoLists.append(temp)
        return twoLists

    def downloadArchives(self, link, params):
        tempParams = self.params
        tempParams["useHeaders"] = True
        title = waziExHentai.getTitle(self, link, params)
        waziExHentai.createFolder(self, link, params)
        links = waziExHentai.getArchives(self, link)
        if not links:
            return "No url return. / 没有返回 URL。"
        for i in links:
            requestParams = self.request.handleParams(tempParams, "get", i["link"], self.headers, self.proxies)
            temp = self.request.do(requestParams)
            fileName = temp.info().get_filename().encode("latin1").decode("utf-8")
            with open(os.path.join(params["path"], title, i["type"] + "_" + fileName), "wb") as f:
                f.write(temp.read())
        return "Done! / 完工！"

class waziPicAcg:
    # An APP that facilitates people to view magazines (R-18).
    # my impression of it is that it is particularly difficult to do crawling.
    #
    # 一个方便人们观看杂志（R-18）的 APP。
    # 我对它的印象就是：特别难做爬虫。
    # [2]
    def __init__(self):
        super(waziPicAcg, self).__init__()
        self.empty = ""
        self.headers = {
            "api-key": "",
            "accept": "application/vnd.picacomic.com.v1+json",
            "app-channel": "3",
            "time": "0",
            "nonce": "",
            "signature": "0",
            "app-version": "2.2.1.3.3.4",
            "app-uuid": "418e56fb-60fb-352b-8fca-c6e8f0737ce6",
            "app-platform": "android",
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "okhttp/3.8.1",
            "app-build-version": "45"
        }
        self.info = {
            "secretKey": "~d}$Q7$eIni=V)9\\RK/P.RM4;9[7|@/CA}b~OW!3?EV`:<>M7pddUBL5n|0/*Cn",
            "baseUrl": "https://picaapi.picacomic.com/",
            "uuid": "",
            "apiKey": "C69BAF41DA5ABD1FFEDC6D2FEA56B"
        }
        self.params = {}
        self.proxies = {
            "proxyAddress": "127.0.0.1",
            "proxyPort": "7890"
        }
        self.token = ""
        self.urls = {
            "login": "https://picaapi.picacomic.com/auth/sign-in",
            "init": "https://139.59.113.68/init",
            "categories": "https://picaapi.picacomic.com/categories",
            "search": "https://picaapi.picacomic.com/comics/search",
            "comics": "https://picaapi.picacomic.com/comics",
            "comicId": "https://picaapi.picacomic.com/comics/{comicId}",
            "comicEps": "https://picaapi.picacomic.com/comics/{comicId}/eps",
            "comicPages": "https://picaapi.picacomic.com/comics/{comicId}/order/{order}/pages",
            "comicRecommend": "https://picaapi.picacomic.com/comics/{comicId}/recommendation",
            "keywords": "https://picaapi.picacomic.com/keywords",
            "myComments": "https://picaapi.picacomic.com/users/my-comments",
            "myFavourites": "https://picaapi.picacomic.com/users/favourite?s=dd",
            "profile": "https://picaapi.picacomic.com/users/profile",
            "games": "https://picaapi.picacomic.com/games",
            "comicFavourite": "https://picaapi.picacomic.com/comics/{comicId}/favourite",
            "comicLike": "https://picaapi.picacomic.com/comics/{comicId}/like",
            "comicComments": "https://picaapi.picacomic.com/comics/{comicId}/comments",
            "advSearch": "https://picaapi.picacomic.com/comics/advanced-search",
            "punchIn": "https://picaapi.picacomic.com/users/punch-in"
        }
        self.request = waziRequest()

    def giveParams(self, params):
        self.params = params
        return self.params

    def headers(self):
        self.info["uuid"] = str(uuid.uuid4()).replace("-", "")
        self.headers["nonce"] = self.info["uuid"]
        self.headers["api-key"] = self.info["apiKey"]

    def sign(self, url, method):
        sig = waziCheck().construct(url, method, self.info["baseUrl"], self.info["uuid"], self.info["apiKey"],
                                    self.info["secretKey"])
        self.headers["signature"] = sig[0]
        self.headers["time"] = str(sig[1])

    def login(self, username, password):
        tempParams = self.params
        tempParams["useHeaders"] = True
        waziPicAcg.sign(self, self.urls["login"], "POST")
        body = {
            "email": username,
            "password": password
        }
        requestParams = self.request.handleParams(tempParams, "post", self.urls["login"], self.headers, self.proxies)
        requestParams["data"] = json.dumps(body).encode()
        jsons = json.loads(self.request.do(requestParams))
        self.token = jsons["data"]["token"]

    def getCategories(self):
        tempParams = self.params
        tempParams["useHeaders"] = True
        waziPicAcg.sign(self, self.urls["categories"], "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", self.urls["categories"], self.headers,
                                                  self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getComics(self, page, c, t, s):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["comics"] + "?page=" + str(page) + "&c=" + urllib.parse.quote(c)
        newUrl += "&t=" + urllib.parse.quote(t) + "&s=" + s
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def search(self, page, keyword):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["search"] + "?page=" + str(page) + "&q=" + urllib.parse.quote(keyword)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getComic(self, comicId):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["comicId"].replace("{comicId}", comicId)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getComicEps(self, comicId, page):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["comicEps"].replace("{comicId}", comicId) + "?page=" + str(page)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def advancedSearch(self, categories, keyword, sort, page):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["advSearch"] + "?page=" + str(page)
        body = {
            "categories": categories,
            "keyword": keyword,
            "sort": sort
        }
        waziPicAcg.sign(self, newUrl, "POST")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "post", newUrl, self.headers, self.proxies)
        requestParams["data"] = json.dumps(body).encode()
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getComicPages(self, comicId, eps, page):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["comicPages"].replace("{comicId}", comicId).replace("{order}", eps) + "?page=" + str(page)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getComicRecommend(self, comicId):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["comicRecommend"].replace("{comicId}", comicId)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getKeywords(self):
        tempParams = self.params
        tempParams["useHeaders"] = True
        waziPicAcg.sign(self, self.urls["keywords"], "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", self.urls["keywords"], self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getMyComments(self, page):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["myComments"] + "?page=" + str(page)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getMyFavourites(self, page):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["myFavourites"] + "&page=" + str(page)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getMyProfile(self):
        tempParams = self.params
        tempParams["useHeaders"] = True
        waziPicAcg.sign(self, self.urls["profile"], "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", self.urls["profile"], self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getGames(self, page):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["games"] + "?page=" + str(page)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getGamesInfo(self, gameId):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["games"] + "/" + str(gameId)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def favOrUnFavComic(self, comicId):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["comicFavourite"].replace("{comicId}", comicId)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def likeOrUnLikeComic(self, comicId):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["comicLike"].replace("{comicId}", comicId)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getComicComments(self, comicId, page):
        tempParams = self.params
        tempParams["useHeaders"] = True
        newUrl = self.urls["comicComments"].replace("{comicId}", comicId) + "?page=" + str(page)
        waziPicAcg.sign(self, newUrl, "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "get", newUrl, self.headers, self.proxies)
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def postComments(self, comicId, content):
        tempParams = self.params
        tempParams["useHeaders"] = True
        url = self.urls["comicComments"].replace("{comicId}", comicId)
        body = {
            "content": content
        }
        self.headers["authorization"] = self.token
        waziPicAcg.sign(self, url, "POST")
        requestParams = self.request.handleParams(tempParams, "post", url, self.headers, self.proxies)
        requestParams["data"] = json.dumps(body).encode()
        jsons = json.loads(self.request.do(requestParams))
        return jsons

    def getSinglePage(self, fileServer, path):
        self.empty = ""
        return fileServer + "/static/" + path

    def punchIn(self):
        tempParams = self.params
        tempParams["useHeaders"] = True
        waziPicAcg.sign(self, self.urls["punchIn"], "GET")
        self.headers["authorization"] = self.token
        requestParams = self.request.handleParams(tempParams, "post", self.urls["punchIn"], self.headers, self.proxies)
        requestParams["data"] = None
        jsons = json.loads(self.request.do(requestParams))
        return jsons

# [1]: 代码使用： https://github.com/WWILLV/iav （未注明详细的版权协议）
# [2]: Api 参考： https://github.com/AnkiKong/picacomic （MIT 版权）
#      Headers 引用： https://github.com/tonquer/picacg-windows （LGPL-3.0 版权）
#      相关信息参考： https://www.hiczp.com/wang-luo/mo-ni-bi-ka-android-ke-hu-duan.html （版权归 czp，未注明详细的版权协议）
