本项目可以进行某站的1080P视频下载，和对弹幕文件进行一定的可视化分析，需要提供视频链接，源码就在这里。需者自取

暂时还没有软件界面，之后会更新， 还会加上登陆系统

视频和弹幕可视化图片下载在代码所在的文件夹：

如需更改，仅需对以下的os.child处进行更改，添加自己想下载的位置

```python
import requests
import re
import pprint
import json
import os
import ffmpeg
import matplotlib.pyplot as plt
import copy

os.child('在这里加上需要的路径') # 例如'D:\\anaconda\\' 末尾记得加双\\

headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        "cookie": "", 
        'referer': 'https://www.bilibili.com/video/BV1kJ411979Q/?spm_id_from=333.999.0.0&vd_source=cadd803574c021e8eedd7d822017fe7b'
    }
```

