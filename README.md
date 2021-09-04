# PyWazi

PyWazi 是一个针对 ExHentai, JavBus, Danbooru, PicAcg 的一个数据采集和处理、操作模块，使用 Python 语言。目前版本为 1.0.0，如果你有想法或在使用中出现问题了，欢迎提出 issue。

[![Python](https://shields.io/badge/Python-3-green?style=flat-square)](https://www.python.org/) [![Version](https://shields.io/badge/Version-1.0.0-yellow?style=flat-square)](https://github.com/Yazawazi/pywazi) [![Dev-Version](https://shields.io/badge/Dev_Version-1.0.1.3-orange?style=flat-square)](https://github.com/Yazawazi/pywazi/blob/main/PyWazi-Dev.py)

## 声明

本模块完全开放源代码，仅供大家学习参考使用，出了事跟我没啥关系（逃

本人临时有事（指上学去了），暂停维护 PyWazi 一个月（或者更多），回来保证焕然一新（或许吧，大概就是更多的功能，拆分，简化和优化，顺便整点注释，翻译一下文档）。

## 安装

如果你是 Windows 用户请前往 Python 官网下载 Python 3 代的安装包或通过 Microsoft Store 下载 Python 3 代并 Git 或 Download ZIP 本项目。

如果你是非 Windows 用户，检查你的系统是否自带 Python 3 和 Git。否则请使用 apt yum pacman 等包管理器安装，并 Git 或 Download ZIP 本项目。

前置 Python 库详见：[说明文档](https://github.com/Yazawazi/pywazi/blob/main/doc.md)

## 使用说明

有时候我的想法比较混乱，并且我不遵守 PEP 8，所以部分代码你可能看不懂。如果你有问题的话，可以找我谈谈或者自己修改一下。如果出现以下问题了，请试着解答以下问题找找原因：

1. 前置环境有安装吗？Python 是 3 代的吗？
2. 配置对了吗，HTTP / HTTPS / SOCK5 等代理不要搞混；
3. 账号密码或 Cookies 请保证正确，账号确保不受限；
4. 查看 [说明文档](https://github.com/Yazawazi/pywazi/blob/main/doc.md) 找找相关内容或百度、谷歌等相关内容。

如果这些都解决不了问题，请发表 issue 并提供上下文，可能的代码、系统版本等可能有关内容。

## 可以干什么

你可以单独使用 PyWazi 来进行开发或爬虫，也可以使用该模块开发开源或闭源项目。

您可以随意 fork 或 clone 等本代码，随意修改，想做什么就做什么。

## 计划要做的事情
1. Danbooru 的高级 Post 搜索（可能，只在 yande.re 下测试）；
2. ExHentai 其他显示模式的支持；
3. PicAcg 的一些内容：
    1. 支持 PicAcg 下载；
    2. PicAcg 封面图的地址处理；
    3. 神魔推荐；
    4. 排行榜：24 小时；7 日排行；30 日排行；骑士榜；
    5. 搜索类：支持随机的本子获取；搜索筛选；最近更新；
    6. 用户类：注册账号；修改密码；修改个人信息；获取通知公告；
    7. 分流类：可选择分流；
    8. 聊天室、留言板和小程式我研究研究；
    9. 重写一下，抽象出来。
4. 英文翻译；
5. 计划使用 requests 代替 urllib3。

## Dev 版本
目前上传了一个 Dev 版本（1.0.1.3），部分新增的功能使用方式已经写在代码中了，以下是新增功能列表：
1. PicAcg 类：
    1. 增加了注册账号的功能；
    2. 增加了修改 / 上传头像的功能；
    3. （可能）增加了修改头衔的功能：
    4. （疑似官方废弃接口）增加了重置密码的功能；
    5. （抽风 连哔咔安卓端都返回 1015）增加了忘记密码的功能；
    6. （管理员用可能）增加了修正用户经验值的功能；
    7. 增加了修改账号密码的功能；
    8. （官方表示现在不行 返回 1030）增加了修改昵称的功能；
    9. 增加了修改签名的功能；
    10. 增加了修改 Q&A 的功能；
    11. （废弃或管理员用）删除用户评论；
    12. 给收藏夹增加了排序功能；
    13. 增加了天排行榜、周排行榜、月排行榜，骑士榜；
    14. 增加了返回随机漫画的功能；
    15. （未经测试）抽象出了 up 函数方便发送网络请求；
    16. 修复了重置密码时请求方式不一致（但是还是不能用）。

## 联系我

如果你有更多的想法，欢迎提出 issues 或者与我联系，我的 QQ 是：2586651867。其他社交平台不活跃，所以不公开。您可以向我提供如下内容：
1. 关于 PicAcg 和 ExHentai 的更多的接口和方法；
2. 一些网站，我将考虑添加到程序中；
3. 一些建议和功能。

## 鸣谢

本项目的开发离不开以下开源项目：

1. JavBus 代码参考：[WWILLV/iav: 可搜索javbus、btso的磁力链接和avgle的预览视频 (github.com)](https://github.com/WWILLV/iav)；
2. PicAcg 部分：[AnkiKong/picacomic: 哔咔漫画相关api (github.com)](https://github.com/AnkiKong/picacomic) 提供了大部分的 Api 链接；使用了 [tonquer/picacg-windows: 哔咔漫画，picacomic，bika，PC客户端。 (github.com)](https://github.com/tonquer/picacg-windows)  中的最新 headers；https://www.hiczp.com/wang-luo/mo-ni-bi-ka-android-ke-hu-duan.html 提供了一些想法（GitHub 地址：[czp3009/czp-blog (github.com)](https://github.com/czp3009/czp-blog)）。

感谢 [cloudwindy (github.com)](https://github.com/cloudwindy) 提供的 ExHentai 账号，得以我进行开发测试。

## Unable to read Simplified Chinese / 无法阅读简体中文

如果你无法阅读简体中文的话，你可以阅读英文版的文档。（未完成）

英文版翻译进度：

1. Readme.md 0%
2. doc.md 0%



If you can't read Simplified Chinese, you can read the English version of the document. (not finished)

English translation progress:

1. Readme.md 0%
2. doc.md 0%

