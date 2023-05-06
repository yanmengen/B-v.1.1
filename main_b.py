import requests
import re
import pprint
import json
import os
import ffmpeg
import matplotlib.pyplot as plt
import copy

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        "cookie": "buvid3=BE12E978-6855-C0CE-61D2-50D801AED44434165infoc; nostalgia_conf=-1; _uuid=382C382C-4786-A4710-393F-"
                  "462833D1097F629066infoc; CURRENT_FNVAL=4048; b_nut=100; i-wanna-go-back=-1; rpdid=|(um~JR~R|km0J'uYY)YmuJuk;"
                  " buvid_fp_plain=undefined; buvid4=C1EA2EB9-A32E-F1B2-6F10-2C63A2D5E68935720-022111719-EAK3sQjE1V7%2BBlz29%2FXo5A%3D%3D;"
                  " DedeUserID=346300659; DedeUserID__ckMd5=0e5b8963dff72b4d; b_ut=5; hit-new-style-dyn=0; hit-dyn-v2=1; go_old_video=1;"
                  " header_theme_version=CLOSE; home_feed_column=5; CURRENT_PID=0f747c80-d065-11ed-b94e-59dd22031221;"
                  " fingerprint=80dc85eacf2480afb024e7d873e42b5f; CURRENT_QUALITY=0; PVID=6; b_lsid=F5683EE3_187745D8F1A;"
                  " FEED_LIVE_VERSION=V8; SESSDATA=53088f55%2C1696836506%2C1fece%2A42; bili_jct=a85f5b2cc5c8ee3372dd4b754112d219; sid=631aziqx; innersign=1; bp_video_offset_346300659=783595308523192300; buvid_fp=80dc85eacf2480afb024e7d873e42b5f",
        'referer': 'https://www.bilibili.com/video/BV1kJ411979Q/?spm_id_from=333.999.0.0&vd_source=cadd803574c021e8eedd7d822017fe7b'
    }


def ch_name(name1):
    list1 = ['\\', '/' ,'*', '?', '"','<', '>', '|']
    list2 = []
    for zifu in name1:
        if zifu in list1:
            list2.append(zifu)
    list3 = list(set(list2))
    for zifu2 in list3:
        name2 = name1.replace(zifu2, '').replace(' ', '')
        name1 = name2
    return name1


def get_data(url):
    # url = input('请输入视频链接:')
    response = requests.get(url=url, headers=headers)
    url_date = response.text
    return url_date


def parse_data(url_date):
    # url_date = get_data()
    del_data = re.findall('<script>window.__playinfo__=(.*?)</script>', url_date, re.S)
    name1 = re.findall('<title data-vue-meta="true">(.*?)</title>', url_date, re.S)[0]
    name = ch_name(name1)
    data = del_data[0]
    dict_date = json.loads(data)
    audio_url = dict_date['data']['dash']['audio'][0]['backupUrl'][0]
    Video_url = dict_date['data']['dash']['video'][0]['backupUrl'][0]
    return audio_url, Video_url, name

def down_data(url):
    url_date = get_data(url)
    audio_url, Video_url, name = parse_data(url_date)
    yin_cont = requests.get(audio_url, headers=headers).content
    vid_cont = requests.get(Video_url, headers=headers).content
    with open(f'{name}.mp3', mode='wb') as f:
        f.write(yin_cont)
        f.close()
    with open(f'{name}.mp4', mode='wb') as f:
        f.write(vid_cont)
        f.close()
    audio = ffmpeg.input(f'{name}.mp3')
    video = ffmpeg.input(f'{name}.mp4')
    out = ffmpeg.output(video, audio, f'{name}1.mp4').run()
    os.remove(f'{name}.mp3')
    os.remove(f'{name}.mp4')


def xml(max_num, url_date, name):
    """
    :param max_num: 需要的排行数量
    :param url_date: html数据
    :return:
    """
    del_data = re.findall('<script>window.__playinfo__=(.*?)</script>', url_date, re.S)
    # name1 = re.findall('<title data-vue-meta="true">(.*?)</title>', url_date, re.S)[0]
    # name = ch_name(name1)
    data = del_data[0]
    dict_date = json.loads(data)
    audio_url = dict_date['data']['dash']['audio'][0]['backupUrl'][0]
    cid = audio_url.split('/')[6]
    url = f'https://comment.bilibili.com/{cid}.xml'
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    d = {}
    data = re.findall('p=".*?">(.*?)</d><d', response.text, re.S)
    with open(f'{name}弹幕资源.txt', mode='a', encoding='utf-8') as f:
        for xmls in data:
            f.write(xmls + '\n')
            d[xmls] = d.get(xmls, 0) + 1 # 进行计数
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(figsize=(7, 6), dpi=200) # 设置幕布的分辨率
        plt.xticks(fontsize=7, rotation=90) # fontsize:设置x轴的字体大小，rotation:设置字体转向
        plt.yticks(fontsize=7) # 同上设置y轴
        x1 = list(d.items())
        x2 = sorted(x1,key=lambda x1:x1[1], reverse=True) #排序
        try:
            need_list = x2[0:max_num]  #确定排行数量
        except:
            need_list = x2[0:len(x2)]  # 如果max_num过大，将全部输出
        need_dict = dict(need_list)
        x = need_dict.keys()
        y = need_dict.values()
        for a,b in zip(x,y):
            plt.text(a, b + 0.05, b, ha='center', va='bottom', fontsize=5)  #给y坐标添加注释
        plt.bar(x,y)
        plt.tight_layout()  # ⾃动调整布局空间，就不会出现图⽚保存不完整
        plt.savefig(fname=f"{name}.png", dip=100, facecolor = 'blue', edgecolor = 'green', bbox_inches = 'tight')
                    #名字可加地址        分辨率    # 视图边界颜⾊设置       # 视图边界颜⾊设置

