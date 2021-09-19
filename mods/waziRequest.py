import urllib3

class waziRequest:
    # Network request class.
    # 网络请求类
    def __init__(self):
        super(waziRequest, self).__init__()
        self.isUseProxies = True
        self.proxies = ""
        self.isUseHeaders = False
        self.headers = {
            "User-Agent": "Use Your UA.",
        }

    def useProxies(self, isUse):
        self.isUseProxies = isUse
        return self.isUseProxies

    def editProxies(self, http, port):
        if http is None or port is None:
            self.proxies = None
        else:
            self.proxies = "http://" + http + ":" + str(port)
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

    def get(self, url):
        if self.isUseProxies:
            http = urllib3.ProxyManager(self.proxies)
        else:
            http = urllib3.PoolManager()
        if self.isUseHeaders:
            temp = http.request("GET", url, headers = self.headers)
        else:
            temp = http.request("GET", url)
        return temp

    def post(self, url, data):
        if self.isUseProxies:
            http = urllib3.ProxyManager(self.proxies)
        else:
            http = urllib3.PoolManager()
        if self.isUseHeaders:
            temp = http.request("POST", url, body = data, headers = self.headers)
        else:
            temp = http.request("POST", url, body = data)
        return temp

    def fieldsPost(self, url, data):
        if self.isUseProxies:
            http = urllib3.ProxyManager(self.proxies)
        else:
            http = urllib3.PoolManager()
        if self.isUseHeaders:
            temp = http.request("POST", url, headers = self.headers, fields = data)
        else:
            temp = http.request("POST", url, fields = data)
        return temp

    def put(self, url, data):
        if self.isUseProxies:
            http = urllib3.ProxyManager(self.proxies)
        else:
            http = urllib3.PoolManager()
        if self.isUseHeaders:
            temp = http.request("PUT", url, body = data, headers = self.headers)
        else:
            temp = http.request("PUT", url, body = data)
        return temp

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
        elif params["method"].lower() == "fieldspost":
            return waziRequest.fieldsPost(self, params["url"], params["data"])
        elif params["method"].lower() == "put":
            return waziRequest.put(self, params["url"], params["data"])
        else:
            return "Sorry, method must be get, post or put. / 对不起，模式一定得是 GET, POST 或者 PUT 呜呜呜。"

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
