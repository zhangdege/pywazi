# PyWazi 的说明文档

> Yazawazi
>
> 仅针对 1.0.0 版本 因时间和个人问题 英文版以后再写

[TOC]

## 特别注明

暂时使用 urllib3，等我搓一个轮子出来。有时间再搓一个用 requests 的玩玩。

> 我将可能的，含有隐私的内容进行了一个码的打。

测试环境：

> CPU - Intel(R) Core(TM) i5-9400F CPU @ 2.90GHz
> RAM - 32.00 GB DDR4 2666 MHz (Kingston)
> Use Hong Kong (China) Proxy
> Windows 11 22000.100
>
> Python:
>
> > Python 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)] on win32
> > Python 3.8.8 (default, Apr 13 2021, 15:08:03) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
>
> Packages in 3.9.6:
>
> > beautifulsoup4 4.9.3
> > certifi 2021.5.30
> > lxml 4.6.3
> > urllib3 1.26.6
>
> Packages in 3.8.8:
>
> > beautifulsoup4 4.9.3
> > certifi 2020.12.5
> > lxml 4.6.3
> > urllib3 1.26.4

## 说明

代码写的很烂，如果要改建议直接 fork 一份出去自己改，要是你有什么需求可以跟我讲，我尽量给你整出来。

## 环境要求

Python 3 代应该都可以吧（

需要的是 beautifulsoup4 lxml urllib4 应该就够了

## 功能

### 针对 Danbooru 的功能
1. Posts 时间线
    1. 获取 Posts 时间线
    2. 下载 Posts 时间线

### 针对 JavBus 的功能
1. 搜索番号磁链

### 针对 ExHentai 的功能
1. Cookies 登录
2. 浏览
    1. 普通模式（可能展示不全或经过设置）
    2. 全部模式（无视设置并允许其他内容）
3. 搜索
    1. 普通模式
    2. 全部模式
    3. 标签模式
    4. 上传者模式
    5. 上传者全部模式
    6. 高级模式
    7. 图片模式
    8. 自定义模式
4. 信息获取
    1. 种子信息
    2. 基础信息
        1. 通过网页端的模式
        2. 通过 API 接口
    3. 评论内容
    4. 手动翻页次数
5. 图片
    1. 缩略图
        1. Large 模式
        2. Normal 模式
    2. 列出下载地址或进行下载
        1. 普通模式
        2. （MPV 权限用户限定）API MPV 下载
    3. 压缩包
        1. H@H 下载（不清楚，看代码）
        2. 列出原图压缩包下载地址或直接下载
        3. 列出普通画质压缩包下载地址或直接下载

### 针对 PicAcg 的功能
1. 登录 
2. 获取分区
3. 搜索
    1. Comics 接口
    2. 关键字搜索
    3. 高级搜索
4. 漫画
    1. 基本信息
    2. 分页
    3. 分页内容
    4. 针对该本漫画的推荐
    5. 喜欢或取消喜欢
    6. 收藏或取消收藏
    7. 获取评论
    8. 进行评论
5. 获取热词
6. 个人
    1. 评论
    2. 收藏
    3. 个人信息
    4. 签到
7. 游戏
    1. 游戏列表
    2. 游戏信息
    3. 喜欢或取消喜欢
    4. 获取评论
    5. 进行评论
8. 其它
    1. 获取单独的图片地址

## 开始

### 导入 PyWazi

本来想做 install.py 上传包的，但是想了想，垃圾代码就没必要上传 pip 了。使用时请把 pywazi.py 放在你的项目目录下。

在你的 Python 文件中加入：
```python
from pywazi impory *
```

如果只想 import 部分内容则：

```python
from pywazi import waziXXXX, waziXXXX
```

### 操作初始化

如果你需要操作 waziXXXX，那么你必须得定义一个外部实例来调用该类，其他同理，如：

```python
from pywazi import waziExHentai

eh = waziExHentai()
```

## waziDanbooru 教程

Danbooru 是一个开源的图集展示系统，而且它开放 Api，有https://yande.re/ https://konochan.com/等。

我就是根据这两个做的，不清楚其他网站会不会有问题。

### 初始化并配置

```python
from pywazi import waziDanbooru

wdb = waziDanbooru()

wdb.giveParams({
    "useProxies": True, # 是否使用代理
    "proxyAddress": "127.0.0.1", # HTTPS / HTTP 代理地址
    "proxyPort": "7890", # HTTPS / HTTP 代理端口
    "useHeaders": False, # 是否用自定义头部 （不建议填写，程序自动补充）
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.164 Safari/537.36"
    } # 自定义头部内容 （不建议填写，程序自动补充，自己填写可能导致部分程序错误）
})

wdb.setApi("https://yande.re") # 设置域名
```

### Posts 时间线

访问接口是：`URL/post.json`（当然也可以是`post.xml`）

不同的网站有不同的格式，但是都差不多。

#### 获取 Posts 时间线

```python
wdb.getPosts(0, "")

# 第一个表示页码 第二个表示标签
# 第一页为 0 无标签则以空字符串代替 多标签请用加号连接
# 仅允许英文字符（罗马音包括）
```

返回格式为 JSON （取其中一例）：

```
[{
	'id': 823891,
	'tags': 'bikini erect_nipples swimsuits tomozero wet',
	'created_at': 1627717072,
	'updated_at': 1627717074,
	'creator_id': 225185,
	'approver_id': None,
	'author': 'hiroimo2',
	'change': 4291445,
	'source': 'https://i.pximg.net/img-original/img/2021/07/31/16/20/09/91622368_p0.jpg',
	'score': 0,
	'md5': 'c38d6a2e109414510d02bd963c66c970',
	'file_size': 1823848,
	'file_ext': 'jpg',
	'file_url': 'https://files.yande.re/image/c38d6a2e109414510d02bd963c66c970/yande.re%20823891%20bikini%20erect_nipples%20swimsuits%20tomozero%20wet.jpg',
	'is_shown_in_index': True,
	'preview_url': 'https://assets.yande.re/data/preview/c3/8d/c38d6a2e109414510d02bd963c66c970.jpg',
	'preview_width': 84,
	'preview_height': 150,
	'actual_preview_width': 169,
	'actual_preview_height': 300,
	'sample_url': 'https://files.yande.re/sample/c38d6a2e109414510d02bd963c66c970/yande.re%20823891%20sample%20bikini%20erect_nipples%20swimsuits%20tomozero%20wet.jpg',
	'sample_width': 844,
	'sample_height': 1500,
	'sample_file_size': 226287,
	'jpeg_url': 'https://files.yande.re/image/c38d6a2e109414510d02bd963c66c970/yande.re%20823891%20bikini%20erect_nipples%20swimsuits%20tomozero%20wet.jpg',
	'jpeg_width': 1000,
	'jpeg_height': 1777,
	'jpeg_file_size': 0,
	'rating': 'q',
	'is_rating_locked': False,
	'has_children': True,
	'parent_id': None,
	'status': 'pending',
	'is_pending': False,
	'width': 1000,
	'height': 1777,
	'is_held': False,
	'frames_pending_string': '',
	'frames_pending': [],
	'frames_string': '',
	'frames': [],
	'is_note_locked': False,
	'last_noted_at': 0,
	'last_commented_at': 0,
	'flag_detail': {
		'post_id': 823891,
		'reason': 'low-res',
		'created_at': '2021-07-31T07:37:52.765Z',
		'user_id': None,
		'flagged_by': 'system'
	}
}, ...]
```

因为篇幅受限和各个 Danbooru 类网站返回的 JSON 格式都不一致，故无法详细解读。

#### 下载 Posts 时间线

```python
wdb.downloadPosts(0, "", "./download")

# 格式同获取 Posts 时间线一致（getPosts）
# 最后加上一个路径（可以是相对 也可以是绝对）
```

下载未作优化，如果有多线程需求可以查看：[cloudwindy/yander: Yande.re 爬虫 (github.com)](https://github.com/cloudwindy/yander)

返回如下内容：

```
['./download/823893.jpg', './download/823892.jpg', './download/823891.jpg', './download/823890.png', './download/823889.png', './download/823888.png', './download/823887.png', './download/823886.png', './download/823885.png', './download/823883.png', './download/823882.png', './download/823881.png', './download/823880.png', './download/823879.png', './download/823878.png', './download/823877.png', './download/823876.png', './download/823875.png', './download/823874.png', './download/823873.png', './download/823872.png', './download/823871.png', './download/823870.png', './download/823869.png', './download/823868.png', './download/823867.png', './download/823866.png', './download/823865.png', './download/823864.png', './download/823863.png', './download/823862.png', './download/823861.png', './download/823860.png', './download/823859.png', './download/823858.png', './download/823857.png', './download/823856.png', './download/823855.png', './download/823854.png', './download/823853.png']
```

记录了你的下载位置（是否相对取决于你的路径）。

## waziJavBus 教程

关于更多的内容请访问：https://www.javbus.com/ 自己一探究竟。

### 初始化并配置

```python
from pywazi import waziJavBus

wjb = waziJavBus()

wjb.giveParams({
    "useProxies": True, # 是否使用代理
    "proxyAddress": "127.0.0.1", # HTTPS / HTTP 代理地址
    "proxyPort": "7890", # HTTPS / HTTP 代理端口
    "useHeaders": False, # 是否用自定义头部 （不建议填写，程序自动补充）
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.164 Safari/537.36"
    } # 自定义头部内容 （不建议填写，程序自动补充，自己填写可能导致部分程序错误）
})

# 可选内容
wjb.customUrl("https://www.javbus.icu/") # 设置镜像站
wjb.useDomainApi(True) # 是否使用主站的 Api 部分镜像站需要设置为 True
```

### 获取番号磁链

```python
wjb.getMagnet("doks-539")

# 填写番号名 注意大小写
```

返回 JSON 格式：

```
[{'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}, {'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}, {'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}, {'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}, {'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}, {'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}, {'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}, {'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}, {'title': 'DOKS-539', 'magnet': 'magnet:?xt=urn:btih:BD68655E788DA7B8CAAE739C7D46F3B4890F3A89&dn=DOKS-539', 'size': '5.01GB', 'date': '2021-03-31'}]
```

`title` 表示标签，`magnet` 表示下载磁链，`size` 表示大小，`date` 表示上传日期。

## waziExHentai 教程

ExHentai 是 E-Hentai 的里站，需要有权限的账户才能进入（本人不提供）。在使用本程序前，请确保您的显示方式设置为 `Extended`，未在其他显示模式下测试。（主要是我菜菜）

并且请确保您的网络通顺，部分页面不能加载出来是因为：

1. 你网不好，多试几次总能成的；
2. 你的账户看不了这个。

1 的话换个 DNS 换个梯子试试看，2 的话借号去吧。

### 初始化并配置

```python
from pywazi import waziExHentai

wex = waziExHentai()

wex.giveParams({
    "useProxies": True, # 是否使用代理
    "proxyAddress": "127.0.0.1", # HTTPS / HTTP 代理地址
    "proxyPort": "7890", # HTTPS / HTTP 代理端口
    "useHeaders": False, # 是否用自定义头部 （不建议填写，程序自动补充）
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.164 Safari/537.36"
    } # 自定义头部内容 （不建议填写，程序自动补充，自己填写可能导致部分程序错误）
})

wex.setCookies("xxxxxx=xxxxxxxxxx;xxxxxxx=xxxxxxxxxxxxxxx;xxxxxx=xxxxxxx") # 设置你的 Cookies
```

#### 如何获取你的 Cookies

1. 打开 https://exhentai.org/。（如果没有登录，那就登录一下先）
2. 右键 -> 检查 -> 控制台（只要打开 console 就好了 F12 也行）
3. 输入 `document.cookie` 并回车。
4. 复制内容，这就是你的 Coookies 了。

### 浏览

就是直接看，不搜索。（草）内置两种浏览模式，保证满足需求。（雾）

#### 普通模式

就正常浏览，或者默认设置下的显示内容。

```python
wex.browse(0) # 页码，从 0 开始数起
```

返回 JSON（取其中一例）：

```
[{
		'title': '[すいかのたね (はしくれ太郎)] 放課後生徒指導2 [DL版]',
		'href': 'https://exhentai.org/g/1973120/1c59805f78/',
		'bCats': 'Doujinshi',
		'cover': 'https://exhentai.org/t/56/10/5610ad5e372e392b68bbc83b6a35a7c30bc56c14-1131381-1075-1518-jpg_250.jpg'
}, ...]
```

`title` 表示日文标题，`href` 表示画廊链接，`bCats` 表示分类，`cover` 表示封面。

#### 全部模式

将会无视你的默认设置，关闭你的过滤器，并展示更多内容，如：被删除的画廊、低分标签等。

```python
wex.allBrowse(0) # 页码，从 0 开始数起
```

格式同**普通浏览模式一致**。

### 搜索

我写这个好了好久，快 emo 了。

#### 普通模式

通过你的默认设置进行搜索。

```python
wex.search(0, "dress")
# 页码 从 0 计数
# 搜索内容
```

格式同**普通浏览模式一致**。

#### 全部模式

无视你的默认模式并允许其他内容。

```python
wex.allSearch(0, "dress")
# 页码 从 0 计数
# 搜索内容
```

格式同**普通浏览模式一致**。

#### 标签搜索

通过默认模式进行标签搜索。

```python
wex.tagSearch(0, "female:lolicon")
# 页码 从 0 计数
# 标签名 [包括 : 前的内容（若有）]
```

如果你要问标签全部搜索模式在哪里。笨蛋！用全部模式搜索就好了。呐，格式还是跟上面一样。

#### 上传者搜索

通过默认模式进行上传者搜索。

```python
wex.uploaderSearch(0, "如歌的行板")
# 页码 从 0 计数
# 上传者名 无需带上 uploader: 前缀
```

#### 上传者全部搜索

无视默认模式进行上传者搜索。

```python
wex.uploaderAllSearch(0, "如歌的行板")
# 页码 从 0 计数
# 上传者名 无需带上 uploader: 前缀
```

#### 高级搜索

**不推荐使用，因为这个东西的参数内容过于抽象，建议使用自定义搜索。**

```python
wex.advancedSearch({
	"cats": ["Non-H"], # 需要搜索的分类
    "search": "", # 搜索内容
    "sgn": True, # 是否搜索画廊名称
    "sgt": True, # 是否搜索画廊标签
    "sgd": False, # 是否搜索画廊描述
    "stf": False, # 是否搜索种子名称
    "osgwt": False, # 是否只查看那些带有种子的画廊
    "slpt": False, # 搜索冷门标签或低评分标签
    "sdt": False, # 搜索投票过差的标签
    "seg": False, # 搜索被移除的画廊
    "mr": True, # 是否限定最低评分
    "mrs": 5, # 最低评分 范围是 2 - 5
    "b": False, # 搜索限定范围
    "b1": "", # 起始范围
    "b2": "", # 结束范围
    "dfl": False, # 关掉默认或设置对语言的过滤
    "dfu": False, # 关掉默认或设置对上传者的过滤
    "dft": False, # 关掉默认或设置对标签的过滤
    "page": 0 # 页码 从 0 计数
})
```

#### 图片搜索

**不推荐使用，因为这个东西的参数内容过于抽象，建议使用自定义搜索。**

通过默认模式进行图片搜索。

##### 自己给出文件的 SHA-1

```python
wex.imageSearch({
	"type": "sha1",
    "sha1": "C75774D8D2F003C8337F1EA57BA3184A9A4FD515",
    "similar": True, # 是否搜索相似的图片
    "cover": True, # 是否搜索封面
    "exp": True # 是否搜索被移除的画廊
})
```

##### 自己给出图片的路径

```python
wex.imageSearch({
	"type": "file",
    "path": "./11.jpg", # 绝对和相对均可
    "similar": True, # 是否搜索相似的图片
    "cover": True, # 是否搜索封面
    "exp": True # 是否搜索被移除的画廊
})
```

#### 自定义搜索

我非常推荐开发者使用自定义搜索来快速构建一个更为严谨的搜索模式。

```python
wex.customSearch({
	"cats": ["Doujinshi", "Manga", "Artist CG", "Game CG"], # 搜索需要的分类 不提供表示全搜索
	"uploaders": ["Pokom", "NekoHime27"], # 是否搜索上传者 不提供表示不搜索
	"tags": ["female:lolicon"], # 是否搜索标签 不提供表示不搜索
	"text": "", # 是否搜索关键词 不提供表示不搜索 三者互相制约
	"advanced": { # 高级搜索 不提供表示不进行高级搜索
		"search": {
			"galleryName": True, # 是否搜索画廊名称
			"galleryTags": True, # 是否搜索画廊标签
			"galleryDescription": False, # 是否搜索画廊描述
			"torrentFilenames": False, # 是否搜索种子名
			"low-powerTags": False, # 是否搜索低力量标签
			"downvotedTags": False, # 是否搜索投票给差的标签
			"expungedGalleries": False, # 是否搜索被移除的标签
		},
		"limit": {
			"onlyShowGalleriesWithTorrents": False, # 是否只搜索带种子的画廊
			"minimumRating": False, # 是否启用最低评分
			"minimumRatingNumber": 2, # 最低评分 2 - 5
			"between": False, # 范围
			"betweenPages": [0, 0] # 起始与结束
		},
		"disableFilters": {
			"language": False, # 是否关闭语言过滤器
			"uploader": False, # 是否关闭上传者过滤器
			"tags": False # 是否关闭标签过滤器
		}
	},
	"file": { # 文件搜索，不提供表示不进行文件搜索
		"main": {
			"type": "path", # 可以是 sha1
			"value": "./a.jpg" # sha 1 值
		},
		"options": {
			"useSimilarityScan": True, # 是否启用相似搜索
			"onlySearchCovers": False, # 是否指搜索封面
			"showExpunged": False # 查看被移除的画廊
		}
	}
})
```

### 信息获取

包含种子信息，基础信息，评论内容和分页四大要素。

#### 种子信息

```python
wex.getTorrent("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url
```

返回为 JSON：

```
[{'time': '2021-07-02 17:44', 'size': '107.0 MB', 'seeds': '7', 'peers': '0', 'total': '2810', 'link': 'https://exhentai.org/torrent/1948847/122ce9d316681251fe0ea634e0c0af8f0e491d74.torrent', 'name': '(同人CG集) [tokunocin (徳之ゆいか) 妄想少女キクリちゃん #1.zip'}]
```

`time` 表示上传时间，`size` 表示文件大小，`seeds` 和 `peers` 我也不懂，我不搞种子的。`total` 表示下载总量，`link` 表示种子的下载地址，`name` 表示种子文件名

#### 基础信息

分了两个获取方式出来：1. 通过网页端；2. 通过 API 接口。

##### 通过网页端模式

```python
wex.getInfo("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url
```

返回为 JSON：

```
{'title': '[tokunocin (Tokuno Yuika)] Mousou Shoujo Kikuri-chan # 1', 'jTitle': '[tokunocin (徳之ゆいか)] 妄想少女キクリちゃん #1', 'cats': 'Artist CG', 'tags': ['group:tokunocin', 'artist:tokuno yuika', 'female:stockings', 'female:sole female', 'female:solo action', 'female:masturbation', 'variant set'], 'time': '2021-07-02 17:41', 'father': 'None', 'viewable': 'Yes', 'language': 'Japanese', 'size': '107.0 MB', 'pages': '20 pages', 'favTimes': '229 times', 'uploader': '那珂 ちゃん', 'rate': '4.58', 'cover': 'https://exhentai.org/t/0d/cc/0dcc07ddde12dd84a128ae83f9ff48375e32f768-5456884-2921-4112-png_250.jpg'}
```

`title` 表示罗马字/英文标题，`jTitle` 表示日文或其他语种标题，`cats` 表示分类，`tags` 表示标签，`time` 表示上传时间，`father` 表示父级图集，`viewable` 表示是否可见，`language` 表示语言，`size` 表示大小，`pages` 表示页码，`favTimes` 表示被收藏次数，`uploader` 表示上传者，`rate` 表示评分，`cover` 表示封面。

##### 通过 Api 接口获取

```python
wex.apiInfo("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url
```

返回为 JSON：

```
{'gmetadata': [{'gid': 1948847, 'token': 'f81687b96e', 'archiver_key': '452153--5199ecd2562338cc94aa8a09db897b32011d18d0', 'title': '[tokunocin (Tokuno Yuika)] Mousou Shoujo Kikuri-chan # 1', 'title_jpn': '[tokunocin (徳之ゆいか)] 妄想少女 キクリちゃん #1', 'category': 'Artist CG', 'thumb': 'https://exhentai.org/t/0d/cc/0dcc07ddde12dd84a128ae83f9ff48375e32f768-5456884-2921-4112-png_l.jpg', 'uploader': '那珂ちゃん', 'posted': '1625247675', 'filecount': '20', 'filesize': 112188093, 'expunged': False, 'rating': '4.58', 'torrentcount': '1', 'torrents': [{'hash': '122ce9d316681251fe0ea634e0c0af8f0e491d74', 'added': '1625247855', 'name': '(同人CG集) [tokunocin (徳之ゆいか) 妄想少女キクリちゃん #1.zip', 'tsize': '17487', 'fsize': '112192764'}], 'tags': ['group:tokunocin', 'artist:tokuno yuika', 'female:masturbation', 'female:sole female', 'female:solo action', 'female:stockings', 'variant set']}]}
```

`gid` 和 `token` 请你自己猜猜，`archiver_key` 是压缩包下载地址的后缀, `title` 是标题，`title_jpn` 是日文标题，`category` 是分类，`thumb` 是封面，`uploader` 是上传者, `posted` 是秒级别的时间戳，`filecount` 是文件数量，`filesize` 是文件大小，`expunged` 是否被移除状态，`rating` 是评分，`torrentcount` 是种子数量，`hash` 是种子哈希值，`added` 是秒级别的时间戳，`name` 是种子文件名，`tsize` 和 `fszie` 我不清楚，`tags` 是标签。

#### 评论内容

```python
wex.getComments("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url
```

返回为 JSON：

```
[{'time': '02 July 2021, 17:41', 'uploader': 'https://exhentai.org/uploader/%E9%82%A3%E7%8F%82%E3%81%A1%E3%82%83%E3%82%93', 'uploaderName': '那珂ちゃん', 'scores': 'None / 不适用', 'htmlComments': '\n https://fantia.jp/posts/615177\n <br/>\n <br/>\n <a href="https://exhentai.org/s/0dcc07ddde/1948847-1">\n  001~010 文字あり\n </a>\n <br/>\n <a href="https://exhentai.org/s/0e34105f9a/1948847-11">\n  011~020 文字なし\n </a>\n\n'}, {'time': '30 July 2021, 04:56', 'uploader': 'https://exhentai.org/uploader/[打码]', 'uploaderName': '[打码]', 'scores': '+76', 'htmlComments': '\n https://ehwiki.org/wiki/japanese\n <br/>\n <br/>\n Default language flag;\n <strong>\n  do NOT use this tag\n </strong>\n outside of legitimate dual-language galleries and translations to Japanese.\n\n'}]
```

`time` 表示评论时间，`uploader` 表示评论者主页，`uploaderName` 表示评论者昵称，`scores` 表示评分，`htmlComments` 表示 html 版本的评论。

#### 是否多页

```python
wex.getPages("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url
```

返回为 0 表示无需翻页，返回正整数表示需要翻页，该数值表示需要手动翻页几次。

### 图片

下载图片，获取图片。

#### 缩略图

缩略图给了两种模式：Large 跟 Normal。

##### Large 模式

```python
wex.getLargeThumbnails("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url
```

返回 JSON （举一例说明）：

```
[{'url': 'https://exhentai.org/t/0d/cc/0dcc07ddde12dd84a128ae83f9ff48375e32f768-5456884-2921-4112-png_l.jpg', 'style': 'height:302px', 'alt': '01', 'title': 'Page 1: cien_2102_01_full.png', 'text': '01'}, ...]
```

`url` 表示缩略图下载地址，`style` 表示这张图的叠层样式表信息，`alt` 表示缺失时内容，`title` 表示图片信息，`text` 大概率也是一种图片信息吧（

##### Normal 模式

```python
wex.getNormalThumbnails("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url
```

返回 JSON （举一例说明）：

```
[{'style': 'height:161px', 'divMargin': '1px auto 0', 'divWidth': '100px', 'divHeight': '141px', 'url': 'https://exhentai.org/m/001948/1948847-00.jpg', 'transparent': '-0px 0 no-repeat', 'imgAlt': '01', 'imgTitle': 'Page 1: cien_2102_01_full.png', 'imgWidth': '100px', 'imgHeight': '140px', 'imgMargin': '-1px 0 0 -1px'}, ...]
```

我也不清楚怎么说明（其实是懒），对于这一块，最好的搞清楚的办法就是去看 Normal 模式下的网站源码。

#### 列出下载地址或下载

##### 普通模式

```python
wex.getNormalImages("https://exhentai.org/g/1948847/f81687b96e/", "get", {"path": "./download", "japanese": True})

# 本子 url
# 方式：get 表示获取 download 表示下载
# 后面 path 表示你的下载路径 相对和绝对都可以
# japanese 如果是 True 那么使用日文名文件名
```

get 返回：

```
['https://psnnstn.svbhzynmthvg.hath.network:6643/h/9a46b72d4e41e2cb71904e3f47a3a225041614f6-702136-2400-3379-jpg/keystamp=1627754700-3893ea4f9c;fileindex=94546547;xres=2400/cien_2102_01_full.jpg', ...]
```

download 返回：

```
['./download\\[tokunocin (徳之ゆいか)] 妄想少女キクリちゃん #1\\cien_2102_01_full.jpg', ...]
```

##### MPV 权限用户

```python
wex.getMPVImages("https://exhentai.org/g/1948847/f81687b96e/", "get", {"path": "./download", "japanese": True})

# 本子 url
# 方式：get 表示获取 download 表示下载
# 后面 path 表示你的下载路径 相对和绝对都可以
# japanese 如果是 True 那么使用日文名文件名
```

get 返回：

```
[{'name': 'cien_2102_01_full.png', 'url': 'https://vzwiuar.bgjtsezaekpi.hath.network:9880/h/219a879c79dddf63c230e02408ccebceebd9cccb-283462-1280-1802-jpg/keystamp=1627755900-c26b737547;fileindex=94546547;xres=1280/cien_2102_01_full.jpg'}, ...]
```

`name` 表示文件名，`url` 表示下载链接。

download 返回：

```
['./download\\[tokunocin (徳之ゆいか)] 妄想少女キクリちゃん #1\\cien_2102_01_full.jpg', ...]
```

#### 压缩包

分三个：H@H、链接、下载

##### H@H 获取

```python
wex.getArchivesHATH("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url。
```

返回 JSON （取一例）：

```
[{'sample': '780x', 'size': '1.42 MB', 'cost': 'Free', 'code': '780', 'url': 'https://exhentai.org/archiver.php?gid=1948847&token=f81687b96e&or=452154-1c41df26535532bfc35cff7874319017afed3418'}, ...]
```

`sample` 表示分辨率，`size` 表示大小，`cost` 表示花费点数，`code` 表示代码，`url` 表示 H@H 请求链接。

##### H@H 下载

```python
wex.toHATH("https://exhentai.org/archiver.php?gid=1948847&token=f81687b96e&or=452154-1c41df26535532bfc35cff7874319017afed3418", "780")

# getArchivesHATH 返回的 url 和 code
```

如果返回 `Done! / 完成！` 就表示成了，否则，按照提示做。

##### 列出压缩包下载地址

```python
wex.getArchives("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url。
```

返回 JSON （取一例）：

```
[{'type': 'original', 'link': 'https://plprhexcngkbxoopaqlx.hath.network/archive/1948847/1d0756978bba0f6166cc5eafa1b05cc33257a77d/cxltzmu9ovu/2?start=1'}, {'type': 'resample', 'link': 'https://plprhexcngkbxoopaqlx.hath.network/archive/1948847/1d0756978bba0f6166cc5eafa1b05cc33257a77d/cxltzmu9ovu/3?start=1'}]
```

`type` 表示压缩包类型，`link` 表示下载地址

##### 下载压缩包

```python
wex.downloadArchives("https://exhentai.org/g/1948847/f81687b96e/", {"path": "./download", "japanese": True})

# 本子 url。
# 后面 path 表示你的下载路径 相对和绝对都可以。
# japanese 如果是 True 那么使用日文名文件名。
```

因为我从来没下载完过，就不清楚是否能正常返回最后预定的格式了。

返回 410 就是说，你现在没法下载了。

## waziPicAcg 教程

### 初始化并配置

```python
from pywazi import waziPicAcg

wpa = waziPicAcg()

wpa.giveParams({
    "useProxies": True, # 是否使用代理
    "proxyAddress": "127.0.0.1", # HTTPS / HTTP 代理地址
    "proxyPort": "7890", # HTTPS / HTTP 代理端口
    "useHeaders": False, # 是否用自定义头部 （不建议填写，程序自动补充）
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.164 Safari/537.36"
    } # 自定义头部内容 （你填了我估计没法访问）
})

wpa.login("你的用户名", "你的密码")
```

正常登陆后返回一串 token，如果失败了，大概率是：

1. 网络问题，一开始我就进了这坑；
2. 时间同步问题，尤其是双系统（Windows + Linux）刚装好的；
3. 账号密码不对或不存在；
4. （偶尔）重大更新了。

### 获取分区

```python
wpa.getCategories()
```

返回 （JSON）：

```
{
	'code': 200,
	'message': 'success',
	'data': {
		'categories': [{
			'title': '援助嗶咔',
			'thumb': {
				'originalName': 'help.jpg',
				'path': 'help.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': True,
			'active': True,
			'link': 'https://donate.wikawika.xyz'
		}, {
			'title': '嗶咔小禮物',
			'thumb': {
				'originalName': 'picacomic-gift.jpg',
				'path': 'picacomic-gift.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': True,
			'link': 'https://gift-web.wikawika.xyz',
			'active': True
		}, {
			'title': '小電影',
			'thumb': {
				'originalName': 'av.jpg',
				'path': 'av.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': True,
			'link': 'https://av.wikawika.xyz',
			'active': True
		}, {
			'title': '小里番',
			'thumb': {
				'originalName': 'h.jpg',
				'path': 'h.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': True,
			'link': 'https://h.wikawika.xyz',
			'active': True
		}, {
			'title': '嗶咔畫廊',
			'thumb': {
				'originalName': 'picacomic-paint.jpg',
				'path': 'picacomic-paint.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': True,
			'link': 'https://paint-web.wikawika.xyz',
			'active': True
		}, {
			'title': '嗶咔鍋貼',
			'thumb': {
				'originalName': 'picacomic-post.jpg',
				'path': 'picacomic-post.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': True,
			'link': 'https://post-web.wikawika.xyz',
			'active': True
		}, {
			'title': '嗶咔商店',
			'thumb': {
				'originalName': 'picacomic-shop.jpg',
				'path': 'picacomic-shop.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': True,
			'link': 'https://online-shop-web.wikawika.xyz',
			'active': True
		}, {
			'title': '大家都在看',
			'thumb': {
				'originalName': 'every-see.jpg',
				'path': 'every-see.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': False,
			'active': True
		}, {
			'title': '下雨了呢',
			'thumb': {
				'originalName': 'recommendation.jpg',
				'path': '829847d3-36ab-4357-834f-676411041554.jpg',
				'fileServer': 'https://storage1.picacomic.com'
			},
			'isWeb': False,
			'active': True
		}, {
			'title': '那年今天',
			'thumb': {
				'originalName': 'old.jpg',
				'path': 'old.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': False,
			'active': True
		}, {
			'title': '官方都在看',
			'thumb': {
				'originalName': 'promo.jpg',
				'path': 'promo.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': False,
			'active': True
		}, {
			'title': '嗶咔運動',
			'thumb': {
				'originalName': 'picacomic-move-cat.jpg',
				'path': 'picacomic-move-cat.jpg',
				'fileServer': 'https://wikawika.xyz/static/'
			},
			'isWeb': True,
			'active': True,
			'link': 'https://move-web.wikawika.xyz'
		}, {
			'_id': '5821859b5f6b9a4f93dbf6e9',
			'title': '嗶咔漢化',
			'description': '未知',
			'thumb': {
				'originalName': 'translate.png',
				'path': 'f541d9aa-e4fd-411d-9e76-c912ffc514d1.png',
				'fileServer': 'https://storage1.picacomic.com'
			}
		}, {
			'_id': '5821859b5f6b9a4f93dbf6d1',
			'title': '全彩',
			'description': '未知',
			'thumb': {
				'originalName': '全彩.jpg',
				'path': '8cd41a55-591c-424c-8261-e1d56d8b9425.jpg',
				'fileServer': 'https://storage1.picacomic.com'
			}
		}, {
			'_id': '5821859b5f6b9a4f93dbf6cd',
			'title': '長篇',
			'description': '未知',
			'thumb': {
				'originalName': '長篇.jpg',
				'path': '681081e7-9694-436a-97e4-898fc68a8f89.jpg',
				'fileServer': 'https://storage1.picacomic.com'
			}
		}, ...
		}]
	}
}
```

### 获取热词

```python
wpa.getKeywords()
```

返回：

```
{'code': 200, 'message': 'success', 'data': {'keywords': ['乳汁', '短髮', '全彩', '自慰', '吞精', '橫切面', '無修正', '
短篇合集', '校園', '人外娘', '開大車']}}
```

### 搜索

分了三类：`Comics` 模式、关键字模式和高级模式。

#### Comics 模式

```python
wpa.getComics("1", "足の恋", "全彩", "ua")

# 第一位参数表示页码，从 1 计数。
# 第二位参数表示分区名字，应当为 categories 里面的 title。
# 第三位参数表示标签名字，由 info 返回数据里面的 tags 获得。
# 第四位参数表示排序依据，分别为：
# 	ua -> 默认排序
#	dd -> 从新到旧
#	da -> 从旧到新
#	vd -> 最多绅士指名
#	ld -> 最多爱心
```

返回 JSON：

```
{
	'code': 200,
	'message': 'success',
	'data': {
		'comics': {
			'docs': [{
				'_id': '610399ae3a8a1824a38ec6d2',
				'title': ' How to use dolls RE',
				'author': 'ooyun',
				'totalViews': 138134,
				'totalLikes': 2122,
				'pagesCount': 35,
				'epsCount': 1,
				'finished': True,
				'categories': ['短篇', '同人', '全彩', '足の恋', '純愛', '後宮閃光'],
				'thumb': {
					'originalName': '00.jpg',
					'path': 'tobeimg/qjKm0jTW70tSw0IyEa-hSI5aMgTLre9aDOa-0nqriSU/fill/300/400/sm/0/aHR0cHM6Ly9zdG9yYWdlMS5waWNhY29taWMuY29tL3N0YXRpYy9kYmQ3MDkyZi01ZjJiLTQ0Y2EtODMyZC01M2NlZjM1MzAxZDkuanBn.jpg',
					'fileServer': 'https://storage1.picacomic.com'
				},
				'id': '610399ae3a8a1824a38ec6d2',
				'likesCount': 2122
			}, ...],
			'total': 83,
			'limit': 20,
			'page': 1,
			'pages': 5
		}
	}
}
```

#### 关键词搜索

```python
wpa.search("1", "伪娘")

# 第一位参数表示页码，从 1 计数。
# 第二位参数表示关键词。
```

返回格式同上。

#### 高级搜索

```python
wpa.advancedSearch(["偽娘哲學"], "全彩", "ld", 1)

# 第一位表示分区，支持多个分区，应当为 list 类型，若不想要可以直接填写 []。
# 第二位表示搜索的关键词。
# 第三位表示排序方式。
# 第四位表示页码，从 1 计数。
```

### 漫画

PS: 漫画下面的 `「进行评论」` 功能鄙人不敢测试（

#### 基本信息

```python
wpa.getComic("60f5aab6e239c4708507c5d9")

# 第一位表示漫画 ID，_id 中可见。
```

返回 JSON：

```
{'code': 200, 'message': 'success', 'data': {'comic': {'_id': '60f5aab6e239c4708507c5d9', '_creator': {'_id': '58b2fe52288c3778fcbaba4d', 'gender': 'f', 'name': 'Selestial', 'verified': False, 'exp': 4586, 'level': 7, 'characters': ['knight'], 'role': 'knight', 'title': '萌新', 'avatar': {'originalName': 'avatar.jpg', 'path': 'f959bc38-94c0-4793-bc02-b1465d74f0bc.jpg', 'fileServer': 'https://storage1.picacomic.com'}, 'slogan': '......', 'character': 'https://pica-web.wakamoment.tk/images/halloween_f.png'}, 'title': 'ホクロ流星群せかんど [中国翻訳] [DL版]', 'description': '早该好好学学了\n（05 后别看05后别看05后别看）', 'thumb': {'originalName': 'QQ图片20210718224515.png', 'path': 'tobeimg/Gxkeem7A4h_VvYKYnIJbQx3ZCAcWFNj38-CFbeOfhZ4/fill/300/400/sm/0/aHR0cHM6Ly9zdG9yYWdlMS5waWNhY29taWMuY29tL3N0YXRpYy9jMjJjODVjNi0yYzUzLTQxMWQtYmIwNi1jZjg0NzBmZGVmZmEucG5n.png', 'fileServer': 'https://storage1.picacomic.com'}, 'author': '書肆マガジンひとり (ホクロ流 星群)', 'chineseTeam': '观星能治颈椎病个人渣翻', 'categories': ['偽娘哲學', '全彩', '短篇'], 'tags': ['偽娘', '口交', ' 制服', '雌墜', '女裝'], 'pagesCount': 30, 'epsCount': 1, 'finished': True, 'updated_at': '2021-07-19T16:39:18.121Z', 'created_at': '2021-07-18T15:12:14.015Z', 'allowDownload': True, 'allowComment': True, 'totalLikes': 438, 'totalViews': 51574, 'viewsCount': 51574, 'likesCount': 438, 'isFavourite': False, 'isLiked': False, 'commentsCount': 97}}}
```

#### 分页

```python
wpa.getComicEps("60f5aab6e239c4708507c5d9", "1")

# 第一位表示漫画 ID。
# 第二位表示第几个分页
# 返回的 epsCount 中注明了有几个分页
```

返回 JSON：

```
{'code': 200, 'message': 'success', 'data': {'eps': {'docs': [{'_id': '60f5aab6e239c4708507c5da', 'title': '第1話', 'order': 1, 'updated_at': '2021-07-18T15:17:47.711Z', 'id': '60f5aab6e239c4708507c5da'}], 'total': 1, 'limit': 40, 'page': 1, 'pages': 1}}}
```

#### 分页内容

```python
wpa.getComicPages("60f5aab6e239c4708507c5d9", "1", "1")

# 第一位表示漫画 ID。
# 第二位表示第几个分页。
# 第三位表示第几页。
# 返回的 pages 注明了全部页码 page 表示现在是第几页。
```

返回 JSON：

```
{
	'code': 200,
	'message': 'success',
	'data': {
		'pages': {
			'docs': [{
				'_id': '60f5aab6e239c4708507c5db',
				'media': {
					'originalName': '00.jpg',
					'path': 'tobeimg/wHyKO5BdzvRZkBugyFPJV0PsDVWI0a6_jDL6FuYISJE/fit/800/800/ce/0/aHR0cHM6Ly9zdG9yYWdlMS5waWNhY29taWMuY29tL3N0YXRpYy8xODU4MzQ0YS1jNTA3LTRhNWYtODYzMC0zYmFiZDYyYWM1ODUuanBn.jpg',
					'fileServer': 'https://storage1.picacomic.com'
				},
				'id': '60f5aab6e239c4708507c5db'
			}, ...],
			'total': 31,
			'limit': 40,
			'page': 1,
			'pages': 1
		},
		'ep': {
			'_id': '60f5aab6e239c4708507c5da',
			'title': '第1話'
		}
	}
}
```

#### 漫画推荐

不知道是不是我写错了，为什么总是不推荐内容。

```python
wpa.getComicRecommend("60f5aab6e239c4708507c5d9")

# 第一位表示漫画 ID。
```

返回 JSON：

```
{'code': 200, 'message': 'success', 'data': {'comics': []}}
```

如果能返回 comics 的话，应该同：[AnkiKong/picacomic: 哔咔漫画相关api (github.com)](https://github.com/AnkiKong/picacomic#recommend-看了這本子的人也在看) 一致。

#### 喜欢或取消喜欢

```python
wpa.likeOrUnLikeComic("60f5aab6e239c4708507c5d9")

# 第一位表示漫画 ID。
```

返回 JSON：

```
{'code': 200, 'message': 'success'}
```

第一次是喜欢，第二次是取消喜欢。

#### 收藏或取消收藏

```python
wpa.favOrUnFavComic("60f5aab6e239c4708507c5d9")

# 第一位表示漫画 ID。
```

返回 JSON：

```
{'code': 200, 'message': 'success'}
```

同上：第一次是收藏，第二次是取消收藏。

#### 获取评论

```python
wpa.getComicComments("60f5aab6e239c4708507c5d9", "1")

# 第一位表示漫画 ID。
# 第二位表示评论页码。
```

返回 JSON：

而且这个 JSON 我删掉了好多评论，可能误删了其他内容。

```
{'code': 200, 'message': 'success', 'data': {'comments': {'docs': [{'_id': '61053f8efde353772059fbac', 'content': '有洗
脑的味儿了', '_user': {'_id': '58c2f6da3f5ca24bed33a10e', 'gender': 'm', 'name': '[打码]', 'verified': False, 'exp': 1405, 'level': 4, 'characters': [], 'role': 'member', 'avatar': {'originalName': 'avatar.jpg', 'path': 'c8bf310f-999b-4d57-81f0-673e0dec67f3.jpg', 'fileServer': 'https://storage1.picacomic.com'}, 'title': '[打码]', 'slogan': '[打码]', 'character': 'https://pica-web.wakamoment.tk/images/halloween_m.png'}, '_comic': '60f5aab6e239c4708507c5d9', 'isTop': False, 'hide': False, 'created_at': '2021-07-31T12:18:22.870Z', 'id': '61053f8efde353772059fbac', 'likesCount': 0, 'commentsCount': 0, 'isLiked': False}, {'_id': '6102101969279b6daec6d2e5', 'content': '小朋友们 快跑啊——\n(未成年请在家长陪同下观看)', '_user': {'_id': '5b93df6fa45b9d65304f4ab7', 'gender': 'bot', 'name': '[打码]', 'title': '[打码]', 'verified': False, 'exp': 3570, 'level': 6, 'characters': [], 'role': 'member', 'avatar': {'fileServer': 'https://storage1.picacomic.com', 'path': 'ae492e1b-cc43-4b10-8a84-30574759cbf2.jpg', 'originalName': 'avatar.jpg'}, 'slogan': '[打码]', 'character': 'https://pica-web.wakamoment.tk/images/halloween_bot.png'}, '_comic': '60f5aab6e239c4708507c5d9', 'isTop': False, 'hide': False, 'created_at': '2021-07-29T02:19:05.590Z', 'id': '6102101969279b6daec6d2e5', 'likesCount': 4, 'commentsCount': 0, 'isLiked': False}, {'_id': '61010b14e65322b6796ff730', 'content': 'hso', '_user': {'_id': '5bf0e5dc0fdd3c38c9517afa', 'gender': 'm', 'name': '[打码]', 'title': '[打码]', 'verified': False, 'exp': 210, 'level': 2, 'characters': [], 'role': 'member', 'avatar': {'fileServer': 'https://storage1.picacomic.com', 'path': '6bc97079-8404-4e91-96f3-ae2c7914e85d.jpg', 'originalName': 'avatar.jpg'}, 'slogan': '[打码]', 'character': 'https://pica-web.wakamoment.tk/images/halloween_m.png'}, '_comic': '60f5aab6e239c4708507c5d9', 'isTop': False, 'hide': False, 'created_at': '2021-07-28T07:45:24.006Z', 'id': '61010b14e65322b6796ff730', 'likesCount': 0, 'commentsCount': 0, 'isLiked': False}, {'_id': '60fef9011ba3a4b65a7ba877', 'content': '可以', '_user': {'_id': '584ecc8b0554fd247dd63194', 'gender': 'm', 'name': '[打码]', 'verified': False, 'exp': 825, 'level': 3, 'characters': [], 'role': 'member', 'avatar': {'originalName': 'avatar.jpg', 'path': '7e53d9e5-7dd8-4a1b-aed4-23757c17f7d5.jpg', 'fileServer': 'https://storage1.picacomic.com'}, 'title': '[打码]', 'slogan': '[打码]', 'character': 'https://pica-web.wakamoment.tk/images/halloween_m.png'}, '_comic': '60f5aab6e239c4708507c5d9', 'isTop': False, 'hide': False, 'created_at': '2021-07-26T18:03:45.405Z', 'id': '60fef9011ba3a4b65a7ba877', 'likesCount': 0, 'commentsCount': 0, 'isLiked': False}, {'_id': '60fe2dc8273afa59289d02b6', 'content': '[打码]', '_user': {'_id': '5b624f89baa50311bef929cf', 'gender': 'm', 'name': '[打码]', 'title': '[打码]', 'verified': False, 'exp': 390, 'level': 2, 'characters': [], 'role': 'member', 'avatar': {'originalName': 'avatar.jpg', 'path': '69009713-1b8f-4a75-b2d3-3351a801adc3.jpg', 'fileServer': 'https://storage1.picacomic.com'}}, '_comic': '60f5aab6e239c4708507c5d9', 'isTop': False, 'hide': False, 'created_at': '2021-07-26T03:36:40.134Z', 'id': '60fe2dc8273afa59289d02b6', 'likesCount': 11, 'commentsCount': 0, 'isLiked': False},, '_comic': '60f5aab6e239c4708507c5d9', 'isTop': False, 'hide': False, 'created_at': '2021-07-22T07:04:32.970Z', 'id': '60f91880281d48c9b80eac72', 'likesCount': 0, 'commentsCount': 0, 'isLiked': False}], 'total': 70, 'limit': 20, 'page': '1', 'pages': 4}, 'topComments': []}}
```

#### 发表评论

```python
wpa.postComicComment("60f5aab6e239c4708507c5d9", "支持")

# 第一位表示漫画 ID。
# 第二位表示评论内容。
```

我不清楚会返回什么，我没那个勇气发表高见。

### 游戏

有时候不太想看本子，就想在手机上玩玩 Gal。

#### 游戏列表

```python
wpa.getGames(1)

# 第一位表示分页，从 1 数起。
```

返回 JSON：

```
{
	'code': 200,
	'message': 'success',
	'data': {
		'games': {
			'docs': [{
				'_id': '60f6a6cf77a54e70a918f3d4',
				'title': '機甲戰姬',
				'version': '1.0.0',
				'publisher': 'JG Game',
				'suggest': False,
				'adult': False,
				'android': True,
				'ios': False,
				'icon': {
					'originalName': 'gumdam_APP - 250.png',
					'path': '90ac9d84-e8d5-456e-a805-3dce8449dad3.png',
					'fileServer': 'https://storage1.picacomic.com'
				}
			}, {
				'_id': '5ded08947cd2ce4ed0f5e101',
				'title': '真愛の百合は赤く染まる',
				'version': '1.0.0',
				'publisher': 'バグシステム',
				'suggest': False,
				'adult': True,
				'android': True,
				'ios': True,
				'icon': {
					'originalName': '2019-12-09 23.29.05.jpg',
					'path': '260034ca-77b3-458a-99c1-1eb11b3a05a4.jpg',
					'fileServer': 'https://storage1.picacomic.com'
				}
			}, ...],
			'total': 133,
			'limit': 100,
			'page': 1,
			'pages': 2
		}
	}
}
```

#### 游戏信息

```python
wpa.getGameInfo("5ded08947cd2ce4ed0f5e101")

# 第一位表示游戏 ID，在 _id 中可见。
```

返回 JSON：

```
{'code': 200, 'message': 'success', 'data': {'game': {'_id': '5ded08947cd2ce4ed0f5e101', 'title': '真愛の百合は赤く染ま
る', 'description': '----------團長特別警告!!----------\n\n純愛大作，厄夜良心推薦。\n親自測試，絕對無雷!\n(๑•̀ᄇ•́)و ✧\n\n物語的主人公「真奈美」最近剛搬到了一個新的小鎮裡，而身為蕾絲的她暗地裡對同班同學的「愛實」抱有著愛意。\n\n一直嘗試隱藏的這份感情卻被對方輕易看穿，而真奈美也從她那聽到了令人驚愕的發言——\n\n「我其實也……喜歡女孩子」\n\n心意相通的兩人很快便確立了關系，然而這份關系卻隨著時間的流逝漸漸變質得不可名狀。「MANAMI」到底能滿足「MANAMI」到什麼程度呢。不久，這份異常的緣分便將她們以外的人們也卷入了事件的漩渦當中，而本應純情的物語也開始大幅度地產生扭曲……\n\n請用zarchiver解壓，用krkr2玩耍。', 'version': '1.0.0', 'icon': {'originalName': '2019-12-09 23.29.05.jpg', 'path': '260034ca-77b3-458a-99c1-1eb11b3a05a4.jpg', 'fileServer': 'https://storage1.picacomic.com'}, 'publisher': 'バグシステム', 'ios': True, 'iosLinks': ['https://game.eroge.xyz/hhh.php?id=106'], 'android': True, 'androidLinks': ['https://game.eroge.xyz/hhh.php?id=106'], 'adult': True, 'suggest': False, 'downloadsCount': 0, 'screenshots': [{'originalName': '2019-12-09 23.29.10.jpg', 'path': 'ad636f7b-cbbd-474a-81f4-ce1509eda319.jpg', 'fileServer': 'https://storage1.picacomic.com'}, {'originalName': '2019-12-09 23.29.14.jpg', 'path': '11ccbab5-8673-4be6-b1bd-f8f9c5687fa9.jpg', 'fileServer': 'https://storage1.picacomic.com'}, {'originalName': '2019-12-09 23.29.18.jpg', 'path': '36d49e43-36b6-4075-9447-1d7ebe460f6e.jpg', 'fileServer': 'https://storage1.picacomic.com'}, {'originalName': '2019-12-09 23.29.22.jpg', 'path': '142140b8-b5bf-47d7-bc0e-4648c79a9290.jpg', 'fileServer': 'https://storage1.picacomic.com'}, {'originalName': '2019-12-09 23.29.25.jpg', 'path': '8e0d66c7-daf9-4dc6-8479-7492bd2fddfd.jpg', 'fileServer': 'https://storage1.picacomic.com'}, {'originalName': '2019-12-09 23.29.29.jpg', 'path': '33eb34ae-e21e-4c4d-a131-bc4bc14fadb0.jpg', 'fileServer': 'https://storage1.picacomic.com'}], 'androidSize': 632.23, 'iosSize': 632.23, 'updated_at': '2020-06-03T14:27:27.042Z', 'created_at': '2019-12-08T14:28:36.369Z', 'likesCount': 8870, 'isLiked': False, 'commentsCount': 1291}}}
```

#### 喜欢或取消喜欢

```python
wpa.likeOrUnLikeGame("5ded08947cd2ce4ed0f5e101")

# 第一位表示游戏 ID。
```

同漫画喜欢：第一次是喜欢，第二次是取消喜欢，返回内容不再赘述。

#### 获取评论

```python
wpa.getGameComments("5ded08947cd2ce4ed0f5e101", "1")

# 第一位表示游戏 ID。
# 第二位表示评论区分页，从 1 数起。
```

返回 JSON，同漫画的获取评论一致，返回内容不再赘述。

#### 发表评论

```python
wpa.postGameComment("5ded08947cd2ce4ed0f5e101", "非常支持")

# 第一位表示游戏 ID。
# 第二位表示评论内容。
```

我说白了，我不敢评论，不敢测试，你们自己试试看。

### 个人

获取基本的个人信息（就你自己）

#### 评论

```python
wpa.getMyComments("1")

# 第一位表示分页，从 1 数起。
```

因为我没评论，返回的 JSON 是空的：

```
{'code': 200, 'message': 'success', 'data': {'comments': {'docs': [], 'total': 0, 'limit': 20, 'page': '1', 'pages': 1}}}
```

#### 收藏

```python
wpa.getMyFavourites("1")

# 第一位表示分页，从 1 数起。
```

返回 JSON：

```
{
	'code': 200,
	'message': 'success',
	'data': {
		'comics': {
			'pages': 12,
			'total': 231,
			'docs': [{
				'_id': '58ab30dea34f167444930a44',
				'title': '鹿島で足コキ48手 (艦隊これくしょん -艦これ-)',
				'author': '嘘つき屋 (大嘘)',
				'pagesCount': 65,
				'epsCount': 1,
				'finished': True,
				'categories': ['同人', '短篇', '足の恋', '艦隊收藏'],
				'thumb': {
					'originalName': '2.jpg',
					'path': '91cf2d7e-fc35-47bb-b0db-99be58a4a2da.jpg',
					'fileServer': 'https://storage1.picacomic.com'
				},
				'totalViews': 425305,
				'totalLikes': 10114,
				'likesCount': 10114
			}, {
				'_id': '5ec2bdc1e2a7bd11c7fb4cce',
				'title': '(C98) ジェントルコネクト!Re:Dive 2 「Amakuchi」(プリンセスコネクト!ReDive) [中国翻訳]',
				'author': 'けんじゃたいむ (MANA)',
				'totalViews': 593647,
				'totalLikes': 10689,
				'pagesCount': 22,
				'epsCount': 1,
				'finished': True,
				'categories': ['全彩', '短篇', '同人', '純愛', '後宮閃光', '非人類'],
				'thumb': {
					'originalName': '000.jpg',
					'path': 'b1c4d4b9-522d-4ee9-90a6-6acaf1eb51d1.jpg',
					'fileServer': 'https://storage1.picacomic.com'
				},
				'likesCount': 10689
			}, ...],
			'page': 1,
			'limit': 20
		}
	}
}
```

#### 资料

```python
wpa.getMyProfile()
```

返回 JSON：

```
{'code': 200, 'message': 'success', 'data': {'user': {'_id': '5f92f94fa94c02192e0d5c6a', 'birthday': '1999-10-08T00:00:00.000Z', 'email': 'yazawazi520', 'gender': 'f', 'name': '鸭杂袜子', 'slogan': '或许冬天我们要到厨房去', 'title': '萌新', 'verified': False, 'exp': 460, 'level': 2, 'characters': [], 'created_at': '2020-10-23T15:39:59.824Z', 'avatar': {'originalName': 'avatar.jpg', 'path': 'fe23bfa0-5e6b-4408-bac6-5b5735fac283.jpg', 'fileServer': 'https://storage1.picacomic.com'}, 'isPunched': True}}}
```

#### 签到

```python
wpa.punchIn()
```

因为我今天签到过了，明天补上。

### 其他

因为 PicAcg 不好做下载（其实是懒），所以写了一些东西（目前只有一个）帮助开发者对 PicAcg 进行更好的操作。

#### 获取图片地址

```python
wpa.getSinglePage("https://storage1.picacomic.com", "fe23bfa0-5e6b-4408-bac6-5b5735fac283.jpg")

# 第一位表示服务器地址，在 fileServer 中可见。
# 第二位表示图片路径，在 path 中可见。
```

返回字符串：

```
https://storage1.picacomic.com/static/fe23bfa0-5e6b-4408-bac6-5b5735fac283.jpg
```

## 结语

本项目的开发离不开以下开源项目：

1. JavBus 代码参考：[WWILLV/iav: 可搜索javbus、btso的磁力链接和avgle的预览视频 (github.com)](https://github.com/WWILLV/iav)；
2. PicAcg 部分：[AnkiKong/picacomic: 哔咔漫画相关api (github.com)](https://github.com/AnkiKong/picacomic) 提供了大部分的 Api 链接；使用了 [tonquer/picacg-windows: 哔咔漫画，picacomic，bika，PC客户端。 (github.com)](https://github.com/tonquer/picacg-windows)  中的最新 headers；https://www.hiczp.com/wang-luo/mo-ni-bi-ka-android-ke-hu-duan.html 提供了一些想法（GitHub 地址：[czp3009/czp-blog (github.com)](https://github.com/czp3009/czp-blog)）。

如果你有更多的想法，欢迎提出 issues 或者与我联系，我的常用联系方式是：

1. 你直接找我 QQ：2586651867。
