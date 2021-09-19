# PyWazi
PyWazi 是一个针对 ExHentai, JavBus, Danbooru, PicAcg 的数据采集、处理和操作模块，使用 Python 语言。目前版本为 1.1，如果你有想法或在使用中出现问题了，欢迎提出 issue。

[![Python](https://shields.io/badge/Python-3-green?style=flat-square)](https://www.python.org/) [![Version](https://shields.io/badge/Version-1.1-yellow?style=flat-square)](https://github.com/Yazawazi/pywazi)

## 声明
本模块完全开放源代码，仅供大家学习参考使用，不鼓励一切在中国大陆境内的使用该模块的商业行为。

## 配置
如果你是 Windows 用户请前往 Python 官网下载 Python 3 代的安装包或通过 Microsoft Store 下载 Python 3 代，然后可以再下载一个 Git 使用 clone 指令将该模块下载到本地，或者直接 Download ZIP 本项目。

如果你是非 Windows 用户，请检查你的系统是否自带 Python 3 代和 Git，否则请使用 apt yum pacman 等包管理器安装，并使用 Git 克隆本项目或直接 Download ZIP 本项目。

前置库：
- beautifulsoup4
- lxml
- urllib3

## 一些说明
有时候我的想法比较混乱，并且我不遵守 PEP 8，所以部分代码你可能看不懂。如果你有问题的话，可以找我谈谈或者自己修改一下。如果出现以下问题了，请试着解答以下问题找找原因：

1. 前置环境有安装吗？Python 是 3 代的吗？
2. 配置对了吗，代理类型不要搞混；
3. 账号密码或 Cookies 请保证正确，账号确保不受限；
4. 查看说明文档找找相关内容或百度、谷歌等相关内容。

如果这些都解决不了问题，请发表 issue 并提供上下文，可能的代码，前置库版本等有关信息。

## 开发文档
目前暂时未完成，因为最新版本仍未进行测试。

## 有什么用
你可以单独使用 PyWazi 来进行开发爬虫，也可以使用该模块开发其他开源项目。

## 联系我
如果你有更多的想法，欢迎提出 issues 或者与我联系，请发送邮件到 yazawazier@gmail.com。您可以向我提供如下内容：

1. 关于 PicAcg 和 ExHentai 的更多的接口和方法；
2. 一些网站，我将考虑添加到程序中；
3. 一些建议和功能。

## 鸣谢
本项目的开发离不开以下开源项目：

1. JavBus 代码参考：[WWILLV/iav: 可搜索javbus、btso的磁力链接和avgle的预览视频 (github.com)](https://github.com/WWILLV/iav)；
2. PicAcg 部分：[AnkiKong/picacomic: 哔咔漫画相关api (github.com)](https://github.com/AnkiKong/picacomic) 提供了大部分的 Api 链接；使用了 [tonquer/picacg-windows: 哔咔漫画，picacomic，bika，PC客户端。 (github.com)](https://github.com/tonquer/picacg-windows)  中的最新 headers；https://www.hiczp.com/wang-luo/mo-ni-bi-ka-android-ke-hu-duan.html 提供了一些想法（GitHub 地址：[czp3009/czp-blog (github.com)](https://github.com/czp3009/czp-blog)）。

感谢 [cloudwindy (github.com)](https://github.com/cloudwindy) 提供的 ExHentai 账号，得以我进行开发测试。