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
            request = urllib.request.Request(url = urllib.parse.quote(url), headers = self.headers)
        else:
            request = urllib.request.Request(url = urllib.parse.quote(url))
        return urllib.request.urlopen(request)

    def post(self, url, data):
        if self.useProxies:
            proxy = urllib.request.ProxyHandler(self.proxies)
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)
        if self.useHeaders:
            # Sometimes(like some JSON Data), you have to json.dumps(yourData).encode() to request.
            # 有时候（比如面对某些 JSON 数据），你必须得先 json.dumps(你数据).encode() 才能发送请求。
            request = urllib.request.Request(url = urllib.parse.quote(url), headers = self.headers, data = data)
        else:
            request = urllib.request.Request(url = urllib.parse.quote(url))
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

class waziDanbooru:
    # Danbooru is a powerful image board system which uses tagging extensively.
    # like https://yande.re/ https://konachan.com/ (R18 NSFW)
    # Danbooru 是一个非常牛逼的画廊展示系统（相册图库差不多吧），主要就是用标签多一点。
    # 像 https://yande.re/ https://konachan.com/ （R18 不适合在公开场合或工作环境浏览）
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
        url = self.api + "/post.json?page" + str(page)
        url += "&tags=" + tags
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
            fileName = path + "/" + str(i["id"]) + "." + i["file_url"].split(".")[-1]
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
        self.params = {}

    def giveParams(self, params):
        self.params = params
        return self.params

    def getAjax(self):
        url = "https://www.javbus.com/" + self.params["avId"]
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
        return "https://www.javbus.com/ajax/uncledatoolsbyajax.php?gid=" + gid + "&lang=zh&img=" + img + "&uc=" + uc

    def getMagnet(self):
        ajaxUrl = waziJavBus.getAjax(self)
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
            "Cookie": "",
        }
        self.proxies = {
            "proxyAddress": "127.0.0.1",
            "proxyPort": "7890"
        }
        self.request = waziRequest()
        self.displayMode = ""
        self.urls = {
            "main": "https://exhentai.org/",
            "galleryTorrent": "https://exhentai.org/gallerytorrents.php?gid=",
            "api": "https://exhentai.org/api.php"
        }
        self.params = {}

    def giveParams(self, params):
        self.params = params
        return self.params

    def setCookies(self, cookies):
        self.headers["Cookie"] = cookies
        return self.headers["Cookie"]

    def getBooks(self, url):
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "get", url, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams), "lxml")
        booksList = []
        urls = soup.find_all(class_ ='itg glte')[0].find_all(class_ ='gl2e')
        covers = soup.find_all(class_ ='itg glte')[0].find_all(class_ ='gl1e')
        coverTimes = -1
        for tempUrl in urls:
            coverTimes += 1
            title = tempUrl.find_all(class_ = "glink")[0].get_text()
            href = tempUrl.find_all("a", attrs = {"href": re.compile("/g/")})[0].attrs["href"]
            bCats = tempUrl.find_all(class_ = "cn")[0].get_text()
            cover = covers[coverTimes].find_all("img")[0].attrs["src"]
            booksList.append({"title": title, "href": href, "bCats": bCats, "cover": cover})
        return booksList

    def browse(self, page):
        url = self.urls["main"] + "?page=" + str(page)
        return waziExHentai.getBooks(self, url)

    def allBrowse(self, page):
        url = self.urls["main"] + "?page=" + str(page) + "&?f_cats=0&advsearch=1&f_sname=on&f_stags=on&f_sh=on&f_sdt2" \
                                                         "=on&f_sfl=on&f_sfu=on&f_sft=on&f_spf=&f_spt="
        return waziExHentai.getBooks(self, url)

    def search(self, page, text):
        url = self.urls["main"] + "?page=" + str(page) + "&f_search=" + text
        return waziExHentai.getBooks(self, url)

    def allSearch(self, page, text):
        url = self.urls["main"] + "?page=" + str(
            page) + "&?f_cats=0&advsearch=1&f_sname=on&f_stags=on&f_sh=on&f_sdt2=on&f_sfl=on&f_sfu=on&f_sft=on" \
                    "&f_search=" + text
        return waziExHentai.getBooks(self, url)

    def tagSearch(self, page, tag):
        url = self.urls["main"] + "tag/" + tag + "/" + str(page)
        return waziExHentai.getBooks(self, url)

    def uploaderSearch(self, page, uploader):
        url = self.urls["main"] + "/uploader/" + uploader + "/" + str(page)
        return waziExHentai.getBooks(self, url)

    def uploaderAllSearch(self, page, uploader):
        url = self.urls["main"] + "?page=" + str(page) + "&f_cats=0&f_search=uploader%3A" + uploader + "&advsearch=1" \
                                                                                                       "&f_sname=on" \
                                                                                                       "&f_stags=on" \
                                                                                                       "&f_sdt2=on" \
                                                                                                       "&f_spf=&f_spt" \
                                                                                                       "=&f_sfl=on" \
                                                                                                       "&f_sfu=on" \
                                                                                                       "&f_sft=on"
        return waziExHentai.getBooks(self, url)

    def advancedSearch(self, params):
        url = self.urls["main"]
        url += "?f_cats=" + waziCheck().getSources(params)
        if str(params["search"]):
            url += "&f_search=" + str(params["search"])
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
            url += "?f_cats=" + waziCheck().getSources(params)
        else:
            url += "?f_cats=0"
        url += "&f_search="
        if "uploaders" in params:
            for i in params["uploaders"]:
                url += "uploader:" + i + "+"
            url = url[:-1]
        if "tags" in params:
            if "uploaders" in params:
                url += "+"
            for i in params["tags"]:
                url += i + "+"
            url = url[:-1]
        if "text" in params:
            if "tags" in params:
                url += "+"
            url += params["text"]
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

    def getTorrent(self, link):
        tempParams = self.params
        tempParams["useHeaders"] = True
        url = self.urls["galleryTorrent"] + link.split("/")[4] + "&t=" + link.split("/")[5]
        requestParams = self.request.handleParams(tempParams, "get", url, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams), "lxml")
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
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "get", link, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams), "lxml")
        tags = []
        for tag in soup.find_all(id = "taglist")[0].find_all("a"):
            tags.append(tag.attrs["onclick"].split("'")[1])
        info = {
            "title": soup.h1.get_text(),
            "jTitle": soup.find_all(id = "gdc")[0].get_text(),
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
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "get", link, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams), "lxml")
        comments = []
        for i in soup.find_all(id = "cdiv")[0].find_all(class_ = "c1"):
            htmlComments = i.find_all(class_="c6")[0].prettify()
            start = re.findall("<div.*?>", i.find_all(class_ = "c6")[0].prettify())[0]
            htmlComments = htmlComments.replace(start, "")
            htmlComments = htmlComments.replace("</div>", "")
            tempComments = {
                "time": i.find(class_ = "c3").get_text().split(" by:")[0].split("Posted on ")[1],
                "uploader": i.find(class_ = "c3").a.attrs["href"],
                "uploaderName": i.find(class_ = "c3").a.get_text(),
                "scores": i.find(class_ = "c5 nosel").span.get_text(),
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
        tempParams["data"] = json.dumps(body).encode()
        requestParams = self.request.handleParams(tempParams, "post", self.urls["api"], headers, self.proxies)
        return json.loads(self.request.do(requestParams).read())

    # TODO: ExHentai： 缩略图（normal large） MPV 的图片列表与下载 普通用户的图片列表与下载 压缩包下载 其他显示模式的支持
    # TODO: JavBus： 首页爬虫 分类爬虫
    # TODO: Danbooru： 再看看能不能优化一下
    # TODO: PicAcg： 登录 获得所有分区 获取漫画信息 搜索 高级搜索 获取漫画 获取漫画分页 获取漫画分页图片 下载漫画
    # TODO: 加解密： PicAcg 那块
    # TODO: 其他： 写文档 测试 把用到的的几个开源项目写一下
