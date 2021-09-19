import hmac
import time
import hashlib

class waziCheck:
    # Separate checksum and crypto system for ExHentai search and PicAcg encryption and decryption processing.
    # 单独的校验和密码系统，针对 ExHentai 的搜索和 PicAcg 的加解密处理。
    def __init__(self):
        super(waziCheck, self).__init__()
        self.sha1 = hashlib.sha1()
        # These are ExHentai's tags.
        # 这些是 ExHentai 的标签。
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
        # These are the corresponding scores for the ExHentai tag.
        # You can see the values corresponding to all tags in table.itc of ExHentai.
        #
        # 这些是 ExHentai 标签的对应分数。
        # 在 ExHentai 的 table.itc 中可以看到所有标签对应的数值。
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
        # I've listed all the possible scoring displacement codes that can occur.
        # 我将所有可能出现的评分位移代码列举出来了。
        self.ratingPos = {
            "-80px -1px": 0,
            "-80px -21px": 0,
            "-64px -21px": 0.5,
            "-64px -1px": 1,
            "-48px -21px": 1.5,
            "-48px -1px": 2,
            "-32px -21px": 2.5,
            "-32px -1px": 3,
            "-16px -21px": 3.5,
            "-16px -1px": 4,
            "0px -21px": 4.5,
            "0px -1px": 5
        }

    @staticmethod
    def returnHasTorrents(soup):
        torrentsImg = soup.attrs["src"]
        # My idea is to compare whether the download icon address matches the download icon address of the existing
        # seed gallery Although it is more intuitive to use the title parameter for comparison But I think the URL is
        # a little more current and perhaps more reliable.
        #
        # 我的思路是对比下载图标地址是否与存在种子画廊的下载图标地址是否一致
        # 尽管使用 title 参数进行对比更加直观
        # 但我认为 URL 的资源时效性更高一点，或许更加可靠。
        if torrentsImg == "https://exhentai.org/img/t.png":
            hasTorrents = True
        else:
            hasTorrents = False
        return hasTorrents

    def returnRatingNum(self, pos):
        if pos in self.ratingPos:
            return self.ratingPos[pos]
        else:
            return "I can't get it, check your codes. / 我无法获取该评分，检查你的代码。"

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

    @staticmethod
    def signature(url, times, method, baseURL, uuids, apiKey, secretKey):
        raw = url.replace(baseURL, "") + str(times) + uuids + method + apiKey
        raw = raw.lower()
        hc = hmac.new(secretKey.encode(), digestmod = hashlib.sha256)
        hc.update(raw.encode())
        return hc.hexdigest()

    @staticmethod
    def construct(url, method, baseURL, uuids, apiKey, secretKey):
        times = int(time.time())
        sig = waziCheck.signature(url, times, method, baseURL, uuids, apiKey, secretKey)
        return [sig, times]
