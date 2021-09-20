import os
import re
import json
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from mods.waziURL import waziURL
from mods.waziCheck import waziCheck
from mods.waziRequest import waziRequest

class waziExHentai:
    # ExHentai is the world's largest erotic homoerotic manga site.
    # ExHentai 是全世界最大的色情同人志漫画网站。
    def __init__(self):
        super(waziExHentai, self).__init__()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.164 Safari/537.36",
            "Cookie": "",
            "Connection": "keep-alive"
        }
        self.proxies = {
            "proxyAddress": "127.0.0.1",
            "proxyPort": "7890"
        }
        self.request = waziRequest()
        self.check = waziCheck()
        self.URL = waziURL()
        self.urls = {
            "main": "https://exhentai.org/",
            "galleryTorrent": "https://exhentai.org/gallerytorrents.php?gid=",
            "api": "https://exhentai.org/api.php",
            "mpv": "https://exhentai.org/mpv/"
        }
        self.params = {}
        self.needParse = False

    def giveParams(self, params):
        self.params = params
        return self.params

    def setParse(self, boolean):
        self.needParse = boolean
        return self.needParse

    def setCookies(self, cookies):
        self.headers["Cookie"] = cookies
        return self.headers["Cookie"]

    @staticmethod
    def getDisplayMode(soup):
        options = soup.find_all(id = "dms")[0].find("select").find_all("option")
        for i in options:
            if "selected" in i.attrs:
                return i.get_text()

    def getMainInfo(self, soup, parserType):
        if parserType == "Extended":
            return waziExHentai.getExtendedMain(self, soup)
        elif parserType == "Minimal":
            return waziExHentai.getMinimalMain(self, soup)
        elif parserType == "Minimal+":
            return waziExHentai.getMinimalPlusMain(self, soup)
        elif parserType == "Compact":
            return waziExHentai.getCompactMain(self, soup)
        elif parserType == "Thumbnail":
            return waziExHentai.getThumbnailMain(self, soup)
        else:
            return []

    # These parsers are fragile, and as soon as an update or a slight change in the style of the site is made,
    # these conditions may render them inoperable.
    #
    # I recommend that you use Extended display mode because it is the most comprehensive (relatively) way to get
    # information and I have the most confidence in this mode.
    #
    # 这些解析器都很脆弱，只要一更新或者网站的样式稍微修改，
    # 这些情况都有可能使他们无法运行。
    #
    # 我建议你使用 Extended 显示模式，因为该模式下获取的信息最全面（相对），并且这个模式我最有把握。

    def getMinimalJSON(self, soup, parseType):
        ratingPos = soup.find(class_ = "ir").attrs["style"].split("background-position:")[1].split(";")[0]
        ratingNum = self.check.returnRatingNum(ratingPos)
        cover = soup.find(class_ = "glthumb").find("img").attrs["src"]
        if "data:image" in cover:
            cover = soup.find(class_ = "glthumb").find("img").attrs["data-src"]
        if parseType == "plus":
            title = soup.find(class_ = "gl3m glname").find(class_ = "glink").get_text()
        else:
            title = soup.find(class_ = "gl3m glname").get_text()
        tempBooks = {
            "title": title,
            "URL": soup.find(class_ = "gl3m glname").find("a").attrs["href"],
            "cat": soup.find(class_ = "gl1m glcat").get_text(),
            "cover": cover,
            "uploader": soup.find(class_ = "gl5m glhide").get_text(),
            "uploaderURL": soup.find(class_ = "gl5m glhide").find("a").attrs["href"],
            "time": soup.find(class_ = "gl2m").find_all("div")[-1].get_text(),
            "hasTorrents": self.check.returnHasTorrents(soup.find(class_ = "gl6m").find("img")),
            "rating": ratingNum,
            "pages": soup.find_all("div")[2].find_all("div")[-1].get_text().split(" ")[0]
        }
        if parseType == "plus":
            if soup.find(class_ = "gltm") is None:
                markedTags = []
            else:
                markedTags = []
                for c in soup.find(class_ = "gltm").find_all("div"):
                    markedTags.append(c.attrs["title"])
            tempBooks["others"] = {
                "type": "Minimal+ Own Information",
                "has": ["markedTags"],
                "markedTags": markedTags
            }
        return tempBooks

    def getMinimalMain(self, soup):
        booksList = []
        bigBody = soup.find_all(class_ = "itg gltm")[0].find_all("tr")
        bigBody.pop(0)
        for i in bigBody:
            booksList.append(waziExHentai.getMinimalJSON(self, i, "normal"))
        return booksList

    def getMinimalPlusMain(self, soup):
        booksList = []
        body = soup.find(class_ = "itg gltm").find_all("tr")
        body.pop(0)
        for i in body:
            booksList.append(waziExHentai.getMinimalJSON(self, i, "plus"))
        return booksList

    def getCompactMain(self, soup):
        booksList = []
        body = soup.find(class_ = "itg gltc").find_all("tr")
        body.pop(0)
        for i in body:
            ratingPos = i.find_all(class_ = "ir")[0].attrs["style"].split("background-position:")[1].split(";")[0]
            ratingNum = self.check.returnRatingNum(ratingPos)
            cover = soup.find(class_="glthumb").find("img").attrs["src"]
            if "data:image" in cover:
                cover = soup.find(class_="glthumb").find("img").attrs["data-src"]
            href = i.find_all("a")[1].attrs["href"]
            if "https://exhentai.org/uploader/" in href:
                href = i.find_all("a")[0].attrs["href"]
            tagsDiv = i.find_all(class_ = "gt")
            if tagsDiv is None:
                tags = []
            else:
                tags = []
                for c in tagsDiv:
                    tags.append(c.attrs["title"])
            tempBooks = {
                "title": i.find(class_ = "glink").get_text(),
                "URL": href,
                "cat": i.find(class_ = "cn").get_text(),
                "cover": cover,
                "uploader": i.find_all("a", attrs = {"href": re.compile("uploader")})[0].get_text(),
                "uploaderURL": i.find_all("a", attrs = {"href": re.compile("uploader")})[0].attrs["href"],
                "time": i.find_all("div", attrs = {"onclick": re.compile("popUp")})[0].get_text(),
                "hasTorrents": self.check.returnHasTorrents(i.find_all(class_ = "gldown")[0].find("img")),
                "rating": ratingNum,
                "pages": int(i.find_all(class_ = "gl4c glhide")[0].find_all("div")[1].get_text().split(" ")[0]),
                "others": {
                    "type": "Compact Own Information",
                    "has": ["tags"],
                    "tags": tags
                }
            }
            booksList.append(tempBooks)
        return booksList

    def getThumbnailMain(self, soup):
        booksList = []
        body = soup.find(class_ = "itg gld").find_all(class_ = "gl1t")
        for i in body:
            ratingPos = i.find_all(class_="ir")[0].attrs["style"].split("background-position:")[1].split(";")[0]
            ratingNum = self.check.returnRatingNum(ratingPos)
            if i.find(class_ = "gl6t") is None:
                markedTags = []
            else:
                markedTags = []
                gtList = i.find(class_ = "gl6t").find_all(class_ = "gt")
                for gt in gtList:
                    markedTags.append(gt.attrs["title"])
            tempBooks = {
                "title": i.find(class_ = "gl4t glname glink").get_text(),
                "URL": i.find_all("a")[0].attrs["href"],
                "cat": i.find(class_ = "cs").get_text(),
                "cover": i.find("img").attrs["src"],
                "uploader": "Uploader information is not available in thumbnail mode. / 缩略模式下无法获取上传者信息。",
                "uploaderURL": "Uploader information is not available in thumbnail mode. / 缩略模式下无法获取上传者信息。",
                "time": i.find_all("div", attrs = {"onclick": re.compile("popUp")})[0].get_text(),
                "rating": ratingNum,
                "pages": int(i.find(class_ = "gl5t").find_all("div")[5].get_text().split(" ")[0]),
                "others": {
                    "type": "Thumbnail Own Information",
                    "has": ["markedTags"],
                    "markedTags": markedTags
                }
            }
            booksList.append(tempBooks)
        return booksList

    def getExtendedMain(self, soup):
        booksList = []
        urls = soup.find_all(class_ = "itg glte")[0].find_all(class_ = "gl2e")
        covers = soup.find_all(class_ = "itg glte")[0].find_all(class_ = "gl1e")
        coverTimes = -1
        for tempUrl in urls:
            coverTimes += 1
            try:
                divs = tempUrl.find_all("table")[0].find_all("div")
            except:
                tags = []
            else:
                tags = []
                for i in divs:
                    tags.append(i.attrs["title"])
            ratingPos = tempUrl.find_all(class_ = "ir")[0].attrs["style"].split("background-position:")[1].split(";")[0]
            ratingNum = self.check.returnRatingNum(ratingPos)
            tempBooks = {
                "title": tempUrl.find_all(class_ = "glink")[0].get_text(),
                "URL": tempUrl.find_all("a", attrs = {"href": re.compile("/g/")})[0].attrs["href"],
                "cat": tempUrl.find_all(class_ = "cn")[0].get_text(),
                "cover": covers[coverTimes].find_all("img")[0].attrs["src"],
                "uploader": tempUrl.find_all("a", attrs = {"href": re.compile("uploader")})[0].get_text(),
                "uploaderURL": tempUrl.find_all("a", attrs = {"href": re.compile("uploader")})[0].attrs["href"],
                "time": tempUrl.find_all("div", attrs = {"onclick": re.compile("popUp")})[0].get_text(),
                "hasTorrents": self.check.returnHasTorrents(tempUrl.find_all(class_ = "gldown")[0].find("img")),
                "rating": ratingNum,
                "pages": int(tempUrl.find_all(class_ = "gl3e")[0].find_all("div")[4].get_text().split(" ")[0]),
                "others": {
                    "type": "Extended Own Information",
                    "has": ["tags"],
                    "tags": tags
                }
            }
            booksList.append(tempBooks)
        return booksList

    def getBooks(self, url):
        soup = waziExHentai.returnSoup(self, url)
        if self.needParse:
            parserType = waziExHentai.getDisplayMode(soup)
            return waziExHentai.getMainInfo(self, soup, parserType)
        else:
            return waziExHentai.getMainInfo(self, soup, "Extended")

    def browse(self, page):
        params = {
            "page": str(page)
        }
        url = self.URL.getFullURL(self.urls["main"], params)
        return waziExHentai.getBooks(self, url)

    def allBrowse(self, page):
        params = {
            "f_spf": "",
            "f_spt": "",
            "page": str(page)
        }
        url = self.URL.getExHentaiAllURL(self.urls["main"], params)
        return waziExHentai.getBooks(self, url)

    def search(self, page, text):
        params = {
            "page": str(page),
            "f_search": urllib.parse.quote(text)
        }
        url = self.URL.getFullURL(self.urls["main"], params)
        return waziExHentai.getBooks(self, url)

    def allSearch(self, page, text):
        params = {
            "page": str(page),
            "f_search": urllib.parse.quote(text)
        }
        url = self.URL.getExHentaiAllURL(self.urls["main"], params)
        return waziExHentai.getBooks(self, url)

    def tagSearch(self, page, tag):
        url = self.urls["main"] + "tag/" + urllib.parse.quote(tag) + "/" + str(page) + "?empty=0"
        return waziExHentai.getBooks(self, url)

    def uploaderSearch(self, page, uploader):
        url = self.urls["main"] + "uploader/" + urllib.parse.quote(uploader) + "/" + str(page) + "?empty=0"
        return waziExHentai.getBooks(self, url)

    def uploaderAllSearch(self, page, uploader):
        params = {
            "page": str(page),
            "f_search": "uploader%3A" + urllib.parse.quote(uploader),
            "f_spf": "",
            "f_spt": ""
        }
        url = self.URL.getExHentaiAllURL(self.urls["main"], params)
        return waziExHentai.getBooks(self, url)

    def advancedSearch(self, params):
        queryParams = {
            "f_cats": str(self.check.getSources(params))
        }
        if str(params["search"]):
            queryParams["f_search"] = urllib.parse.quote(str(params["search"]))
        queryParams["advsearch"] = "1"
        if params["sgn"]:
            queryParams["f_sname"] = "on"
        if params["sgt"]:
            queryParams["f_stags"] = "on"
        if params["sgd"]:
            queryParams["f_sdesc"] = "on"
        if params["stf"]:
            queryParams["f_storr"] = "on"
        if params["osgwt"]:
            queryParams["f_sto"] = "on"
        if params["slpt"]:
            queryParams["f_sdt1"] = "on"
        if params["sdt"]:
            queryParams["f_sdt2"] = "on"
        if params["seg"]:
            queryParams["f_sh"] = "on"
        if params["mr"]:
            queryParams["f_sr"] = "on"
            queryParams["f_srdd"] = str(params["mrs"])
        if params["b"]:
            queryParams["f_sp"] = "on"
            queryParams["f_spf"] = str(params["b1"])
            queryParams["f_spt"] = str(params["b2"])
        if params["dfl"]:
            queryParams["f_sfl"] = "on"
        if params["dfu"]:
            queryParams["f_sfu"] = "on"
        if params["dft"]:
            queryParams["f_sft"] = "on"
        queryParams["page"] = str(params["page"])
        url = self.URL.getFullURL(self.urls["main"], queryParams)
        return waziExHentai.getBooks(self, url)

    def imageSearch(self, params):
        sha1 = ""
        if params["type"] == "sha1":
            sha1 = params["sha1"]
        if params["type"] == "file":
            sha1 = self.check.getFileSHA1(params["path"])
        queryParams = {
            "f_shash": sha1
        }
        if params["similar"]:
            queryParams["fs_similar"] = "1"
        if params["cover"]:
            queryParams["fs_covers"] = "1"
        if params["exp"]:
            queryParams["fs_exp"] = "1"
        url = self.URL.getFullURL(self.urls["main"], queryParams)
        return waziExHentai.getBooks(self, url)

    def customSearch(self, params):
        queryParams = {}
        if "cats" in params:
            queryParams["f_cats"] = str(waziCheck().getSources(params))
        else:
            queryParams["f_cats"] = "0"
        queryParams["f_search"] = ""
        if "uploaders" in params:
            for i in params["uploaders"]:
                queryParams["f_search"] += "uploader:" + urllib.parse.quote(i) + "+"
            queryParams["f_search"] = queryParams["f_search"][:-1]
        if "tags" in params:
            if "uploaders" in params:
                queryParams["f_search"] += "+"
            for i in params["tags"]:
                queryParams["f_search"] += urllib.parse.quote(i) + "+"
            queryParams["f_search"] = queryParams["f_search"][:-1]
        if "text" in params:
            if "tags" in params:
                queryParams["f_search"] += "+"
            queryParams["f_search"] += urllib.parse.quote(params["text"])
        if "advanced" in params:
            queryParams["advanced"] = "1"
            if "search" in params["advanced"]:
                if params["advanced"]["search"]["galleryName"]:
                    queryParams["f_sname"] = "on"
                elif not params["advanced"]["search"]["galleryName"]:
                    queryParams["f_sname"] = ""
                else:
                    pass
                if params["advanced"]["search"]["galleryTags"]:
                    queryParams["f_stags"] = "on"
                elif not params["advanced"]["search"]["galleryTags"]:
                    queryParams["f_stags"] = ""
                else:
                    pass
                if params["advanced"]["search"]["galleryDescription"]:
                    queryParams["f_sdesc"] = "on"
                elif not params["advanced"]["search"]["galleryDescription"]:
                    queryParams["f_sdesc"] = ""
                else:
                    pass
                if params["advanced"]["search"]["torrentFilenames"]:
                    queryParams["f_storr"] = "on"
                elif not params["advanced"]["search"]["torrentFilenames"]:
                    queryParams["f_storr"] = ""
                else:
                    pass
                if params["advanced"]["search"]["low-powerTags"]:
                    queryParams["f_sdt1"] = "on"
                elif not params["advanced"]["search"]["low-powerTags"]:
                    queryParams["f_sdt1"] = ""
                else:
                    pass
                if params["advanced"]["search"]["downvotedTags"]:
                    queryParams["f_sdt2"] = "on"
                elif not params["advanced"]["search"]["downvotedTags"]:
                    queryParams["f_sdt2"] = ""
                else:
                    pass
                if params["advanced"]["search"]["expungedGalleries"]:
                    queryParams["f_sh"] = "on"
                elif not params["advanced"]["search"]["expungedGalleries"]:
                    queryParams["f_sh"] = ""
                else:
                    pass
            if "limit" in params["advanced"]:
                if params["advanced"]["limit"]["onlyShowGalleriesWithTorrents"]:
                    queryParams["f_sto"] = "on"
                elif not params["advanced"]["limit"]["onlyShowGalleriesWithTorrents"]:
                    queryParams["f_sto"] = ""
                else:
                    pass
                if params["advanced"]["limit"]["minimumRating"]:
                    queryParams["f_sr"] = "on"
                    queryParams["f_srdd"] = str(params["advanced"]["limit"]["minimumRatingNumber"])
                elif not params["advanced"]["limit"]["minimumRating"]:
                    queryParams["f_sr"] = ""
                    queryParams["f_srdd"] = ""
                else:
                    pass
                if params["advanced"]["limit"]["between"]:
                    queryParams["f_sp"] = "on"
                    queryParams["f_spf"] = str(params["advanced"]["limit"]["betweenPages"][0])
                    queryParams["f_spt"] = str(params["advanced"]["limit"]["betweenPages"][1])
                elif not params["advanced"]["limit"]["between"]:
                    queryParams["f_sp"] = ""
                    queryParams["f_spf"] = ""
                    queryParams["f_spt"] = ""
                else:
                    pass
            if "disableFilters" in params["advanced"]:
                if params["advanced"]["disableFilters"]["language"]:
                    queryParams["f_sfl"] = "on"
                elif not params["advanced"]["disableFilters"]["language"]:
                    queryParams["f_sfl"] = ""
                else:
                    pass
                if params["advanced"]["disableFilters"]["uploader"]:
                    queryParams["f_sfu"] = "on"
                elif not params["advanced"]["disableFilters"]["uploader"]:
                    queryParams["f_sfu"] = ""
                else:
                    pass
                if params["advanced"]["disableFilters"]["tags"]:
                    queryParams["f_sft"] = "on"
                elif not params["advanced"]["disableFilters"]["tags"]:
                    queryParams["f_sft"] = ""
                else:
                    pass
        if "file" in params:
            if "main" in params["file"]:
                if "type" in params["file"]["main"]:
                    if params["file"]["main"]["type"] == "path":
                        queryParams["f_shash"] = self.check.getFileSHA1(params["file"]["main"]["value"])
                    elif params["file"]["main"]["type"] == "sha1":
                        queryParams["f_shash"] = params["file"]["main"]["value"]
                    else:
                        pass
            if "options" in params["file"]:
                if params["file"]["options"]["useSimilarityScan"]:
                    queryParams["fs_similar"] = "1"
                elif not params["file"]["options"]["useSimilarityScan"]:
                    queryParams["fs_similar"] = ""
                else:
                    pass
                if params["file"]["options"]["onlySearchCovers"]:
                    queryParams["fs_covers"] = "1"
                elif not params["file"]["options"]["onlySearchCovers"]:
                    queryParams["fs_covers"] = ""
                else:
                    pass
                if params["file"]["options"]["showExpunged"]:
                    queryParams["fs_exp"] = "1"
                elif not params["file"]["options"]["showExpunged"]:
                    queryParams["fs_exp"] = ""
                else:
                    pass
        url = self.URL.getFullURL(self.urls["main"], queryParams)
        return [{"url": url}, waziExHentai.getBooks(self, url)]

    def returnSoup(self, link):
        tempParams = self.params
        tempParams["useHeaders"] = True
        if not self.needParse:
            link += "&inline_set=dm_e"
        requestParams = self.request.handleParams(tempParams, "get", link, self.headers, self.proxies)
        soup = BeautifulSoup(self.request.do(requestParams).data.decode("utf-8"), "lxml")
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
            "cat": soup.find_all(id = "gdc")[0].div.get_text(),
            "tags": tags,
            "time": soup.find_all(class_ = "gdt2")[0].get_text(),
            "father": soup.find_all(class_ = "gdt2")[1].get_text(),
            "viewable": soup.find_all(class_ = "gdt2")[2].get_text(),
            "language": soup.find_all(class_ = "gdt2")[3].get_text().split(" \xa0")[0],
            "size": soup.find_all(class_ = "gdt2")[4].get_text(),
            "pages": int(soup.find_all(class_ = "gdt2")[5].get_text().split(" ")[0]),
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
        return json.loads(self.request.do(requestParams).data.decode("utf-8"))

    def getPages(self, link):
        soup = waziExHentai.returnSoup(self, link)
        try:
            pages = int(soup.find_all(class_ = "ptt")[0].find_all("a")[-2].get_text())
        except:
            return 0
        else:
            return pages

    @staticmethod
    def parseSoupForLargeThumbnails(soup):
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
            return waziExHentai.parseSoupForLargeThumbnails(soup)
        else:
            for i in range(page + 1):
                url = link + "?p=" + str(i)
                soup = waziExHentai.returnSoup(self, url)
                thumbnails.append(waziExHentai.parseSoupForLargeThumbnails(soup))
            return thumbnails

    @staticmethod
    def parseSoupForNormalThumbnails(soup):
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
            return waziExHentai.parseSoupForNormalThumbnails(soup)
        else:
            for i in range(page + 1):
                url = link + "?p=" + str(i)
                soup = waziExHentai.returnSoup(self, url)
                thumbnails.append(waziExHentai.parseSoupForNormalThumbnails(soup))
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
            lists = json.loads(self.request.do(requestParams).data.decode("utf-8"))
            if method == "get":
                mpvLists.append({
                    "name": dic["n"],
                    "url": lists["i"]
                })
            if method == "download":
                requestParams = self.request.handleParams(tempParams, "get", lists["i"], self.headers, self.proxies)
                with open(os.path.join(params["path"], title, dic["n"]), "wb") as f:
                    f.write(self.request.do(requestParams).data)
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
                    f.write(self.request.do(requestParams).data)
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
        tempParams = self.params
        tempParams["useHeaders"] = True
        requestParams = self.request.handleParams(tempParams, "fieldsPost", link, self.headers, self.proxies)
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
        requestParams = self.request.handleParams(tempParams, "fieldsPost", action, self.headers, self.proxies)
        requestParams["data"] = form
        soup = BeautifulSoup(self.request.do(requestParams).data.decode("utf-8"), "lxml")
        tempUrl = soup.find_all("script")[0]
        try:
            tempUrl = str(tempUrl).split("document.location = \"")[1].split("\";")[0]
        except:
            return "None / 无"
        else:
            requestParams = self.request.handleParams(tempParams, "get", tempUrl, self.headers, self.proxies)
            soup = BeautifulSoup(self.request.do(requestParams).data.decode("utf-8"), "lxml")
            href = soup.find_all("a")[0].attrs["href"]
            downloadLink = urllib.parse.urljoin(tempUrl, href)
            return downloadLink

    def getArchives(self, link):
        soup = waziExHentai.returnSoup(self, link)
        url = soup.find_all(class_="g2 gsp")[0]
        url = url.a.attrs["onclick"].split("'")[1]
        soup = waziExHentai.returnSoup(self, url)
        twoLists = []
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

    def downloadArchives(self, link, params, sample):
        tempParams = self.params
        tempParams["useHeaders"] = True
        title = waziExHentai.getTitle(self, link, params)
        waziExHentai.createFolder(self, link, params)
        links = waziExHentai.getArchives(self, link)
        files = []
        if not links:
            return "No url return. / 没有返回 URL。"
        if sample != "":
            for i in links:
                if not i == "None / 无":
                    if i["type"] == sample:
                        requestParams = self.request.handleParams(tempParams, "get", i["link"], self.headers,
                                                                  self.proxies)
                        try:
                            temp = self.request.do(requestParams)
                        except:
                            pass
                        else:
                            try:
                                fileName = temp.headers["Content-Disposition"]
                            except:
                                fileName = i["type"] + "_" + title + ".zip"
                            else:
                                fileName = fileName.split("filename=\"")[1][:-1].encode("latin1").decode("utf-8")
                            with open(os.path.join(params["path"], title, i["type"] + "_" + fileName), "wb") as f:
                                f.write(temp.data)
                            return os.path.join(params["path"], title, i["type"] + "_" + fileName)
        for i in links:
            if not i == "None / 无":
                requestParams = self.request.handleParams(tempParams, "get", i["link"], self.headers, self.proxies)
                try:
                    temp = self.request.do(requestParams)
                except:
                    pass
                else:
                    try:
                        fileName = temp.headers["Content-Disposition"]
                    except:
                        fileName = i["type"] + "_" + title + ".zip"
                    else:
                        fileName = fileName.split("filename=\"")[1][:-1].encode("latin1").decode("utf-8")
                    files.append(os.path.join(params["path"], title, i["type"] + "_" + fileName))
                    with open(os.path.join(params["path"], title, i["type"] + "_" + fileName), "wb") as f:
                        f.write(temp.data)
        return files
