import os
import json
import urllib.parse
import urllib.request
from mods.waziURL import waziURL
from mods.waziRequest import waziRequest

class waziDanbooru:
    # Danbooru is a powerful image board system which uses tagging extensively.
    # like https://yande.re/ https://konachan.com/ (R-18 NSFW)
    # Danbooru 是一个非常牛逼的画廊展示系统（相册图库差不多吧），主要就是用标签多一点。
    # 像 https://yande.re/ https://konachan.com/ （R-18 不适合在公开场合或工作环境浏览）
    def __init__(self):
        super(waziDanbooru, self).__init__()
        self.request = waziRequest()
        self.URL = waziURL()
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

    def getPosts(self, page, tags, limit):
        params = {
            "page": str(page),
            "tags": urllib.parse.quote(tags),
            "limit": str(limit)
        }
        url = self.URL.getFullURL(urllib.parse.urljoin(self.api, "/post.json"), params)
        tempParams = self.request.handleParams(self.params, "get", url, self.headers, self.proxies)
        return json.loads(self.request.do(tempParams).data.decode("utf-8"))

    def downloadPosts(self, page, tags, limit, path):
        lists = waziDanbooru.getPosts(self, page, tags, limit)
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
                f.write(self.request.do(requestParams).data)
            downloadFiles.append(fileName)
        return downloadFiles
