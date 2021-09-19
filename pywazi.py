"""
Program for crawling web resources.
See Readme.md & doc.md for more details.

爬取网络资源的程序。
详情请看 Readme.md & doc.md。
"""

from sites.waziJavBus import waziJavBus as Wjb
from sites.waziPicAcg import waziPicAcg as Wpa
from sites.waziDanbooru import waziDanbooru as Wdb
from sites.waziExHentai import waziExHentai as Weh

waziJavBus = Wjb()
waziPicAcg = Wpa()
waziDanbooru = Wdb()
waziExHentai = Weh()

# [1]: 代码使用： https://github.com/WWILLV/iav （未注明详细的版权协议）
# [2]: Api 参考： https://github.com/AnkiKong/picacomic （MIT 版权）
#      Headers 引用： https://github.com/tonquer/picacg-windows （LGPL-3.0 版权）
#      相关信息参考： https://www.hiczp.com/wang-luo/mo-ni-bi-ka-android-ke-hu-duan.html （版权归 czp，未注明详细的版权协议）
#      我参考了一位开源者的代码，但是很可惜，我已经在 GitHub 找不到他的项目了（可能是代码进行改动了）
# 感谢我的朋友： cloudwindy 提供了 ExHentai 账号信息
