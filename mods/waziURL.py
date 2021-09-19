from urllib import parse

class waziURL:
    # A class for URL encoding.
    # 一个进行 URL 编码的类。
    def __init__(self):
        super(waziURL, self).__init__()

    @staticmethod
    def getFullURL(url, params):
        if url.endswith("?"):
            return url + parse.urlencode(params)
        else:
            return url + "?" + parse.urlencode(params)

    @staticmethod
    def getExHentaiAllURL(url, params):
        allParams = {
            "f_cats": "0",
            "advsearch": "1",
            "f_sname": "on",
            "f_stags": "on",
            "f_sh": "on",
            "f_sdt2": "on",
            "f_sfl": "on",
            "f_sfu": "on",
            "f_sft": "on"
        }
        queryParams = params
        queryParams.update(allParams)
        return waziURL.getFullURL(url, queryParams)