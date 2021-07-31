# PyWazi 的说明文档

> Yazawazi
>
> 仅针对 1.0.0 版本 因时间和个人问题 英文版以后再写

## 特别注明

目前本人无法在 Windows 下使用 requests，原因不明，暂时不替换 urllib。

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
> > requests 2.25.1
>
> Packages in 3.8.8:
>
> > beautifulsoup4 4.9.3
> > certifi 2020.12.5
> > lxml 4.6.3
> > requests 2.25.1

## 说明

代码写的很烂，如果要改建议直接 fork 一份出去自己改，要是你有什么需求可以跟我讲，我尽量给你整出来。

## 环境要求

Python 3 代应该都可以吧（

需要的是 beautifulsoup4 lxml 应该就够了

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
    "proxyAddress": "127.0.0.1", # HTTPS 代理地址
    "proxyPort": "7890", # HTTPS 代理端口
    "useHeaders": False, # 是否用自定义头部 （不建议填写，程序自动补充）
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.164 Safari/537.36"
    } # 自定义头部内容 （不建议填写，程序自动补充，自己填写可能导致部分程序错误）
})

wdb.setApi("https://yande.re") # 设置域名 要求该 Danbooru 网站支持 https 协议
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
},]
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
    "proxyAddress": "127.0.0.1", # HTTPS 代理地址
    "proxyPort": "7890", # HTTPS 代理端口
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
2. 压根只返回了空页面，部分画廊会出现这样的情况，一个想法是用 `http.client` 重写一下；
3. 你的账户看不了这个。

1 的话换个 DNS 换个梯子试试看，2 的话等我琢磨琢磨，3 的话借号去吧。

### 初始化并配置

```python
from pywazi import waziExHentai

wex = waziExHentai()

wex.giveParams({
    "useProxies": True, # 是否使用代理
    "proxyAddress": "127.0.0.1", # HTTPS 代理地址
    "proxyPort": "7890", # HTTPS 代理端口
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

我非常推荐开发者使用自定义搜索来快速构建一个更为严谨的搜索模式。但是最气的就是有 BUG，同开头的第二条。

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
[{'time': '02 July 2021, 17:41', 'uploader': 'https://exhentai.org/uploader/%E9%82%A3%E7%8F%82%E3%81%A1%E3%82%83%E3%82%93', 'uploaderName': '那珂ちゃん', 'scores': 'None / 不适用', 'htmlComments': '\n https://fantia.jp/posts/615177\n <br/>\n <br/>\n <a href="https://exhentai.org/s/0dcc07ddde/1948847-1">\n  001~010 文字あり\n </a>\n <br/>\n <a href="https://exhentai.org/s/0e34105f9a/1948847-11">\n  011~020 文字なし\n </a>\n\n'}, {'time': '30 July 2021, 04:56', 'uploader': 'https://exhentai.org/uploader/pop9', 'uploaderName': 'pop9', 'scores': '+76', 'htmlComments': '\n https://ehwiki.org/wiki/japanese\n <br/>\n <br/>\n Default language flag;\n <strong>\n  do NOT use this tag\n </strong>\n outside of legitimate dual-language galleries and translations to Japanese.\n\n'}]
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

# 本子 url
```

返回 JSON （取一例）：

```
[{'sample': '780x', 'size': '1.42 MB', 'cost': 'Free', 'code': '780', 'url': 'https://exhentai.org/archiver.php?gid=1948847&token=f81687b96e&or=452154-1c41df26535532bfc35cff7874319017afed3418'}, ...]
```

`sample` 表示分辨率，`size` 表示大小，`cost` 表示花费点数，`code` 表示代码，`url` 表示 H@H 请求链接。

##### H@H 下载

```python
wex.toHATH("https://exhentai.org/archiver.php?gid=1948847&token=f81687b96e&or=452154-1c41df26535532bfc35cff7874319017afed3418", "780")
```

如果返回 `Done! / 完成！` 就表示成了，否则，按照提示做。

##### 列出压缩包下载地址

```python
wex.getArchives("https://exhentai.org/g/1948847/f81687b96e/")

# 本子 url
```

返回 JSON （取一例）：

```
[{'type': 'original', 'link': 'https://plprhexcngkbxoopaqlx.hath.network/archive/1948847/1d0756978bba0f6166cc5eafa1b05cc33257a77d/cxltzmu9ovu/2?start=1'}, {'type': 'resample', 'link': 'https://plprhexcngkbxoopaqlx.hath.network/archive/1948847/1d0756978bba0f6166cc5eafa1b05cc33257a77d/cxltzmu9ovu/3?start=1'}]
```

`type` 表示压缩包类型，`link` 表示下载地址

##### 下载压缩包

```python
wex.downloadArchives("https://exhentai.org/g/1948847/f81687b96e/", {"path": "./download", "japanese": True})

# 本子 url
# 后面 path 表示你的下载路径 相对和绝对都可以
# japanese 如果是 True 那么使用日文名文件名
```

因为我从来没下载完过，就不清楚是否能正常返回最后预定的格式了。

返回 410 就是说，你现在没法下载了。

