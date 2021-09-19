import os
import json
import uuid
import base64
import urllib.parse
import urllib.request
from mods.waziCheck import waziCheck
from mods.waziRequest import waziRequest

class waziPicAcg:
    # An APP that facilitates people to view magazines (R-18).
    # my impression of it is that it is particularly difficult to do crawling.
    #
    # 一个方便人们观看杂志（R-18）的 APP。
    # 我对它的印象就是：特别难做爬虫。
    # [2]
    def __init__(self):
        super(waziPicAcg, self).__init__()
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
            "app-build-version": "45",
            "image-quality": "original"
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
            "register": "https://picaapi.picacomic.com/auth/register",
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
            "punchIn": "https://picaapi.picacomic.com/users/punch-in",
            "gameLike": "https://picaapi.picacomic.com/games/{gameId}/like",
            "gameComments": "https://picaapi.picacomic.com/games/{gameId}/comments",
            "avatar": "https://picaapi.picacomic.com/users/avatar",
            "userTitle": "https://picaapi.picacomic.com/users/{userId}/title",
            "forgotPassword": "https://picaapi.picacomic.com/auth/forgot-password",
            "resetPassword": "https://picaapi.picacomic.com/auth/reset-password",
            "adjustExp": "https://picaapi.picacomic.com/utils/adjust-exp",
            "password": "https://picaapi.picacomic.com/users/password",
            "updateId": "https://picaapi.picacomic.com/users/update-id",
            "updateQA": "https://picaapi.picacomic.com/users/update-qa",
            "removeComment": "https://picaapi.picacomic.com/utils/remove-comment",
            "leaderBoard": "https://picaapi.picacomic.com/comics/leaderboard",
            "knight": "https://picaapi.picacomic.com/comics/knight-leaderboard",
            "randomComic": "https://picaapi.picacomic.com/comics/random",
            "collections": "https://picaapi.picacomic.com/collections",
            "banners": "https://picaapi.picacomic.com/banners",
            "init": "http://68.183.234.72/init",
            "initAndroid": "https://picaapi.picacomic.com/init?platform=android",
            "commentsChildren": "https://picaapi.picacomic.com/comments/{commentId}/childrens?page={page}",
            "replyComment": "https://picaapi.picacomic.com/comments/{commentId}",
            "chat": "https://picaapi.picacomic.com/chat",
            "apps": "https://picaapi.picacomic.com/pica-apps",
            "androidAPPs": "https://picaapi.picacomic.com/applications?platform=android&page={page}",
            "blockUser": "https://picaapi.picacomic.com/utils/block-user",
            "notifications": "https://picaapi.picacomic.com/users/notifications?page={page}",
            "announcements": "https://picaapi.picacomic.com/announcements?page={page}",
            "dirty": "https://picaapi.picacomic.com/users/{userId}/dirty",
            "userProfile": "https://picaapi.picacomic.com/users/{userId}/profile",
            "commentLike": "https://picaapi.picacomic.com/comments/{commentId}/like",
            "commentHide": "https://picaapi.picacomic.com/comments/{commentId}/hide",
            "commentReport": "https://picaapi.picacomic.com/comments/{commentId}/report",
            "commentTop": "https://picaapi.picacomic.com/comments/{commentId}/top"
        }
        self.request = waziRequest()
        self.check = waziCheck()
        self.editHeaders()

    def giveParams(self, params):
        self.params = params
        return self.params

    def editHeaders(self):
        self.info["uuid"] = str(uuid.uuid4()).replace("-", "")
        self.headers["nonce"] = self.info["uuid"]
        self.headers["api-key"] = self.info["apiKey"]

    def sign(self, url, method):
        sig = self.check.construct(url, method, self.info["baseUrl"], self.info["uuid"], self.info["apiKey"],
                                   self.info["secretKey"])
        self.headers["signature"] = sig[0]
        self.headers["time"] = str(sig[1])

    def up(self, url, needAuth, data, method, jsonNeed):
        tempParams = self.params
        tempParams["useHeaders"] = True
        waziPicAcg.sign(self, url, method)
        if needAuth:
            self.headers["authorization"] = self.token
        else:
            self.headers["authorization"] = ""
        return waziPicAcg.normalUP(self, tempParams, url, data, method, jsonNeed)

    def justUP(self, url, data, method, jsonNeed):
        tempParams = self.params
        tempParams["useHeaders"] = False
        return waziPicAcg.normalUP(self, tempParams, url, data, method, jsonNeed)

    def normalUP(self, tempParams, url, data, method, jsonNeed):
        requestParams = self.request.handleParams(tempParams, method.lower(), url, self.headers, self.proxies)
        if method.lower() != "get":
            if data is None:
                requestParams["data"] = json.dumps({}).encode()
            else:
                requestParams["data"] = json.dumps(data).encode()
        if jsonNeed:
            jsons = json.loads(self.request.do(requestParams).data.decode("utf-8"))
            return jsons
        else:
            return self.request.do(requestParams)

    def login(self, username, password):
        body = {
            "email": username,
            "password": password
        }
        try:
            self.token = waziPicAcg.up(self, self.urls["login"], False, body, "POST", True)["data"]["token"]
        except:
            return "Account not available. / 无法获取账号。"
        else:
            return self.token

    def getCategories(self):
        return waziPicAcg.up(self, self.urls["categories"], True, None, "GET", True)

    def getComics(self, page, c, t, s):
        newUrl = self.urls["comics"] + "?page=" + str(page) + "&c=" + urllib.parse.quote(c)
        newUrl += "&t=" + urllib.parse.quote(t) + "&s=" + s
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def search(self, page, keyword):
        newUrl = self.urls["search"] + "?page=" + str(page) + "&q=" + urllib.parse.quote(keyword)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def getComic(self, comicId):
        newUrl = self.urls["comicId"].replace("{comicId}", comicId)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def getComicEps(self, comicId, page):
        newUrl = self.urls["comicEps"].replace("{comicId}", comicId) + "?page=" + str(page)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def advancedSearch(self, categories, keyword, sort, page):
        newUrl = self.urls["advSearch"] + "?page=" + str(page)
        body = {
            "categories": categories,
            "keyword": keyword,
            "sort": sort
        }
        return waziPicAcg.up(self, newUrl, True, body, "POST", True)

    def getComicPages(self, comicId, eps, page):
        newUrl = self.urls["comicPages"].replace("{comicId}", comicId).replace("{order}", eps) + "?page=" + str(page)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def getComicRecommend(self, comicId):
        newUrl = self.urls["comicRecommend"].replace("{comicId}", comicId)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def getKeywords(self):
        return waziPicAcg.up(self, self.urls["keywords"], True, None, "GET", True)

    def getMyComments(self, page):
        newUrl = self.urls["myComments"] + "?page=" + str(page)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    # page 分页 从 1 数起
    # s 排序
    def getMyFavourites(self, page, s):
        newUrl = self.urls["myFavourites"] + "?page=" + str(page) + "&s=" + s
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def getMyProfile(self):
        return waziPicAcg.up(self, self.urls["profile"], True, None, "GET", True)

    def getGames(self, page):
        newUrl = self.urls["games"] + "?page=" + str(page)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def getGameInfo(self, gameId):
        newUrl = self.urls["games"] + "/" + str(gameId)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def likeOrUnLikeGame(self, gameId):
        newUrl = self.urls["gameLike"].replace("{gameId}", gameId)
        return waziPicAcg.up(self, newUrl, True, None, "POST", True)

    def favOrUnFavComic(self, comicId):
        newUrl = self.urls["comicFavourite"].replace("{comicId}", comicId)
        return waziPicAcg.up(self, newUrl, True, None, "POST", True)

    def likeOrUnLikeComic(self, comicId):
        newUrl = self.urls["comicLike"].replace("{comicId}", comicId)
        return waziPicAcg.up(self, newUrl, True, None, "POST", True)

    def likeOrUnLikeComment(self, commentId):
        newUrl = self.urls["commentLike"].replace("{commentId}", commentId)
        return waziPicAcg.up(self, newUrl, True, None, "POST", True)

    def hideOrUnHideComment(self, commentId):
        newUrl = self.urls["commentHide"].replace("{commentId}", commentId)
        return waziPicAcg.up(self, newUrl, True, None, "POST", True)

    def getCommentsChildren(self, commentId, page):
        newUrl = self.urls["commentsChildren"].replace("{commentId}", commentId).replace("{page}", str(page))
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def replyComment(self, commentId, content):
        newUrl = self.urls["replyComment"].replace("{commentId}", commentId)
        body = {
            "content": content
        }
        return waziPicAcg.up(self, newUrl, True, body, "POST", True)

    def reportComment(self, commentId):
        newUrl = self.urls["commentReport"].replace("{commentId}", commentId)
        return waziPicAcg.up(self, newUrl, True, None, "POST", True)

    def topComment(self, commentId):
        newUrl = self.urls["commentTop"].replace("{commentId}", commentId)
        return waziPicAcg.up(self, newUrl, True, None, "POST", True)

    def getGameComments(self, gameId, page):
        newUrl = self.urls["gameComments"].replace("{gameId}", gameId) + "?page=" + str(page)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def postGameComment(self, gameId, content):
        newUrl = self.urls["gameComments"].replace("{gameId}", gameId)
        body = {
            "content": content
        }
        return waziPicAcg.up(self, newUrl, True, body, "POST", True)

    def getComicComments(self, comicId, page):
        newUrl = self.urls["comicComments"].replace("{comicId}", comicId) + "?page=" + str(page)
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    def postComicComment(self, comicId, content):
        newUrl = self.urls["comicComments"].replace("{comicId}", comicId)
        body = {
            "content": content
        }
        return waziPicAcg.up(self, newUrl, True, body, "POST", True)

    @staticmethod
    def getSinglePage(fileServer, path):
        return fileServer + "/static/" + path

    def punchIn(self):
        return waziPicAcg.up(self, self.urls["punchIn"], True, None, "POST", True)

    # 测试版新增内容
    # 功能：PicAcg - 注册一个账号
    # loginName 登录用户名 要求符合正则表达式：/^(?!.*\\.\\.)(?!.*\\.$)[^\\W][\\w.]{0,29}$/i
    # password 登陆密码 明文传输
    # birthday 时间戳（不清楚是不是毫秒级别的）
    # gender 性别 支持 m（女） f（男） bot（机器人）
    # displayName 昵称
    # qa 一个字典，记录了找回账号的密码和问题
    # 示例：
    # wpa.register("pywazi2021",
    #              "pywazi2021520",
    #              0,
    #              "m",
    #              "PyWazi233",
    #              [{"question": "q", "answer": "q"},
    #              {"question": "q", "answer": "q"},
    #              {"question": "q", "answer": "q"}])
    # 成功返回 JSON：
    # {'code': 200, 'message': 'success'}
    # 感谢 https://github.com/tonquer/picacg-windows/blob/main/src/server/req.py 中提供的参数
    def register(self, loginName, password, birthday, gender, displayName, qa):
        data = {
            "email": loginName,
            "password": password,
            "birthday": birthday,
            "gender": gender,
            "name": displayName,
            "answer1": qa[0]["answer"],
            "answer2": qa[1]["answer"],
            "answer3": qa[2]["answer"],
            "question1": qa[0]["question"],
            "question2": qa[1]["question"],
            "question3": qa[2]["question"]
        }
        return waziPicAcg.up(self, self.urls["register"], False, data, "POST", True)

    # 测试版新增内容
    # 功能：PicAcg - 上传 / 修改一个头像
    # params 参数
    # 示例：
    # wpa.uploadAvatar({"type": "file", "path": "F:/avaa.jpeg"}) 通过提供文件路径上传头像（测试通过：jpeg png）
    # wpa.uploadAvatar({"type": "base64", "format": "jpeg", "data": "aaaaaaaaaa"}) 直接提供 base64 数据上传头像（不推荐）
    # 成功返回 JSON：
    # {'code': 200, 'message': 'success'}
    # 感谢 https://github.com/tonquer/picacg-windows/blob/main/src/server/req.py 中提供的参数
    def uploadAvatar(self, params):
        if params["type"] == "base64":
            upload = "data:image/" + params["format"] + ";base64," + params["data"]
        else:
            fileFormat = os.path.splitext(params["path"])[-1][1:]
            with open(params["path"], "rb") as f:
                data = base64.b64encode(f.read()).decode("utf-8")
            upload = "data:image/" + fileFormat + ";base64," + data
        data = {
            "avatar": upload
        }
        return waziPicAcg.up(self, self.urls["avatar"], True, data, "PUT", True)

    # 测试版新增内容
    # 功能：PicAcg - 修改头衔
    # userId 用户 ID
    # title 头衔内容
    # 示例：
    # wpa.setTitle("5f92f94fa94c02192e0d5c6a", "awa")
    # 成功返回 JSON（推测）：
    # {'code': 200, 'message': 'success'}
    # 我只能拿到 {'code': 400, 'error': '1015', 'message': 'invalid request', 'detail': ':('}
    # 难道是有等级限制？我基本不用 PicAcg 看本，请大佬们讲讲这事。
    # 感谢 https://github.com/tonquer/picacg-windows/blob/main/src/server/req.py 中提供的参数

    def setTitle(self, userId, title):
        newUrl = self.urls["userTitle"].replace("{userId}", userId)
        data = {
            "title": title
        }
        return waziPicAcg.up(self, newUrl, True, data, "PUT", True)

    # 重置密码？疑似废弃接口
    def resetPassword(self, loginName, questionNo, answer):
        data = {
            "email": loginName,
            "questionNo": int(questionNo),
            "answer": answer
        }
        return waziPicAcg.up(self, self.urls["resetPassword"], False, data, "POST", True)

    # app 返回 1015 等待服务器修一下
    def forgotPassword(self, loginName):
        data = {
            "email": loginName
        }
        return waziPicAcg.up(self, self.urls["forgotPassword"], False, data, "POST", True)

    # 估计是管理员用的
    # 调整用户经验值
    # wpa.adjustExp("5f92f94fa94c02192e0d5c6a", 470)
    # userId 表示用户 ID，exp 表示经验值，不清楚是不是直接替换还是增加上去的
    def adjustExp(self, userId, exp):
        data = {
            "exp": int(exp),
            "userId": userId
        }
        return waziPicAcg.up(self, self.urls["adjustExp"], True, data, "POST", True)

    # 修改账号密码
    # wpa.changePassword(你的旧密码, 你的新密码)
    # 返回 JSON：
    # {'code': 200, 'message': 'success'}
    def changePassword(self, oldPassword, newPassword):
        data = {
            "old_password": oldPassword,
            "new_password": newPassword
        }
        return waziPicAcg.up(self, self.urls["password"], True, data, "PUT", True)

    # 修改昵称 官方说现在不能用
    def changeDisplayName(self, loginName, newDisplayName):
        data = {
            "email": loginName,
            "name": newDisplayName
        }
        return waziPicAcg.up(self, self.urls["updateId"], True, data, "PUT", True)

    # 修改签名
    # wpa.changeSlogan(你的新签名)
    # 返回 JSON：
    # {'code': 200, 'message': 'success'}
    def changeSlogan(self, newSlogan):
        data = {
            "slogan": newSlogan
        }
        return waziPicAcg.up(self, self.urls["profile"], True, data, "PUT", True)

    # 修改注册时的找回密码的三个问题和答案
    # wpa.changeQA([{"q": "第一个问题", "a": "第一个答案"},
    #               {"q": "第二个问题", "a": "第二个答案"},
    #               {"q": "第三个问题", "a": "第三个答案"}]
    #             )
    # 返回 JSON：
    # {'code': 200, 'message': 'success'}
    def changeQA(self, qa):
        data = {
            "question1": qa[0]["q"],
            "question2": qa[1]["q"],
            "question3": qa[2]["q"],
            "answer1": qa[0]["a"],
            "answer2": qa[1]["a"],
            "answer3": qa[2]["a"]
        }
        return waziPicAcg.up(self, self.urls["updateQA"], True, data, "PUT", True)

    # 删除某个用户的评论
    # 可能是管理员用的 也可能是废弃的 返回 1007
    def removeComment(self, userId):
        data = {
            "userId": userId
        }
        return waziPicAcg.up(self, self.urls["removeComment"], True, data, "POST", True)

    # 天排行榜
    def getH24LeaderBoard(self):
        newUrl = self.urls["leaderBoard"] + "?tt=H24&ct=VC"
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    # 周排行榜
    def getD7LeaderBoard(self):
        newUrl = self.urls["leaderBoard"] + "?tt=D7&ct=VC"
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    # 月排行榜
    def getD30LeaderBoard(self):
        newUrl = self.urls["leaderBoard"] + "?tt=D30&ct=VC"
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    # 骑士榜
    def knightLeaderBoard(self):
        return waziPicAcg.up(self, self.urls["knight"], True, None, "GET", True)

    # 随机漫画
    def getRandomComics(self):
        return waziPicAcg.up(self, self.urls["randomComic"], True, None, "GET", True)

    # 神魔推荐
    def getCollections(self):
        return waziPicAcg.up(self, self.urls["collections"], True, None, "GET", True)

    # 首页横幅内容
    def getBanners(self):
        return waziPicAcg.up(self, self.urls["banners"], True, None, "GET", True)

    # 分流 IP 获得
    def init(self):
        return waziPicAcg.justUP(self, self.urls["init"], None, "GET", True)

    # 分流图像的 Key
    def initAndroid(self):
        return waziPicAcg.up(self, self.urls["initAndroid"], True, None, "GET", True)

    # 修改质量
    def changeImageQuality(self, number):
        imageQuality = ["original", "low", "medium", "high"]
        self.headers["image-quality"] = imageQuality[number]

    @staticmethod
    def createFolder(path, title):
        isExists = os.path.exists(os.path.join(path, title))
        if not isExists:
            os.makedirs(os.path.join(path, title))

    @staticmethod
    def createFolderEps(path, title, docTitle):
        isExists = os.path.exists(os.path.join(path, title, docTitle))
        if not isExists:
            os.makedirs(os.path.join(path, title, docTitle))

    # 获取封面
    def getThumbImage(self, comicId, path):
        comicInfo = waziPicAcg.getComic(self, comicId)
        originalName = comicInfo["data"]["comic"]["thumb"]["originalName"]
        filePath = comicInfo["data"]["comic"]["thumb"]["path"]
        comicName = comicInfo["data"]["comic"]["title"]
        fileURL = "https://storage.wikawika.xyz/static/" + filePath
        waziPicAcg.createFolder(path, comicName)
        temp = waziPicAcg.justUP(self, fileURL, None, "GET", False)
        with open(os.path.join(path, comicName, "thumb_" + originalName), "wb") as f:
            f.write(temp.data)
        return os.path.join(path, comicName, "thumb_" + originalName)

    # 聊天频道获取
    def getChat(self):
        return waziPicAcg.up(self, self.urls["chat"], True, None, "GET", True)

    # 小程序获取
    def getAPPs(self):
        return waziPicAcg.up(self, self.urls["apps"], True, None, "GET", True)

    def singleDownloadComicImage(self, pageDict, path, comicName, docTitle):
        for i in pageDict["data"]["pages"]["docs"]:
            if "fileServer" in i["media"]:
                fileServer = i["media"]["fileServer"]
            else:
                fileServer = "https://storage1.picacomic.com"
            temp = waziPicAcg.justUP(self, waziPicAcg.getSinglePage(fileServer, i["media"]["path"]),
                                     None, "GET", False)
            with open(os.path.join(path, comicName, docTitle, i["media"]["originalName"]), "wb") as f:
                f.write(temp.data)

    # 下载
    def downloadComic(self, comicId, path):
        waziPicAcg.getThumbImage(self, comicId, path)
        comicInfo = waziPicAcg.getComic(self, comicId)
        comicName = comicInfo["data"]["comic"]["title"]
        eps = int(comicInfo["data"]["comic"]["epsCount"])
        for i in range(1, eps + 1):
            newEps = waziPicAcg.getComicEps(self, comicId, str(i))
            for j in newEps["data"]["eps"]["docs"]:
                waziPicAcg.createFolderEps(path, comicName, j["title"])
                newPage = waziPicAcg.getComicPages(self, comicId, str(i), str(j["order"]))
                if newPage["data"]["pages"]["pages"] == 1:
                    waziPicAcg.singleDownloadComicImage(self, newPage, path, comicName, j["title"])
                else:
                    for q in range(1, newPage["data"]["pages"]["pages"] + 1):
                        newPage = waziPicAcg.getComicPages(self, comicId, str(i), str(q))
                        waziPicAcg.singleDownloadComicImage(self, newPage, path, comicName, j["title"])
        return "Done! / 完工！"

    # 安卓程序
    def getAndroidAPPs(self, page):
        newUrl = self.urls["androidAPPs"].replace("{page}", str(page))
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    # 封禁用户
    def blockUser(self, userId):
        data = {
            "userId": userId
        }
        return waziPicAcg.up(self, self.urls["blockUser"], True, data, "POST", True)

    # 获取通知
    def getNotifications(self, page):
        newUrl = self.urls["notifications"].replace("{page}", str(page))
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    # 获取公告
    def getAnnouncements(self, page):
        newUrl = self.urls["announcements"].replace("{page}", str(page))
        return waziPicAcg.up(self, newUrl, True, None, "GET", True)

    # 不知道是啥
    def getUserDirty(self, userId):
        newUrl = self.urls["dirty"].replace("{userId}", userId)
        return waziPicAcg.up(self, newUrl, True, None, "POST", True)
