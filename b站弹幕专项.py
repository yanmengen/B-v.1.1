import requests
import parsel
import datetime
import re
import google.protobuf.text_format as text_format
import dm_pb2 as Danmaku
import pprint
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        "cookie": "buvid3=BE12E978-6855-C0CE-61D2-50D801AED44434165infoc; nostalgia_conf=-1; _uuid=382C382C-4786-A4710-393F-"
                  "462833D1097F629066infoc; CURRENT_FNVAL=4048; b_nut=100; i-wanna-go-back=-1; rpdid=|(um~JR~R|km0J'uYY)YmuJuk;"
                  " buvid_fp_plain=undefined; buvid4=C1EA2EB9-A32E-F1B2-6F10-2C63A2D5E68935720-022111719-EAK3sQjE1V7%2BBlz29%2FXo5A%3D%3D;"
                  " DedeUserID=346300659; DedeUserID__ckMd5=0e5b8963dff72b4d; b_ut=5; hit-new-style-dyn=0; hit-dyn-v2=1; go_old_video=1;"
                  " header_theme_version=CLOSE; home_feed_column=5; CURRENT_PID=0f747c80-d065-11ed-b94e-59dd22031221;"
                  " fingerprint=80dc85eacf2480afb024e7d873e42b5f; CURRENT_QUALITY=0; PVID=6; b_lsid=F5683EE3_187745D8F1A;"
                  " FEED_LIVE_VERSION=V8; SESSDATA=53088f55%2C1696836506%2C1fece%2A42; bili_jct=a85f5b2cc5c8ee3372dd4b754112d219; sid=631aziqx; innersign=1; bp_video_offset_346300659=783595308523192300; buvid_fp=80dc85eacf2480afb024e7d873e42b5f",
    }

def get_data(url):
    response = requests.get(url=url, headers=headers)
    url_date = response.text
    return url_date

def par_data(url_data):
    min_date = re.findall('<meta data-vue-meta="true" itemprop="uploadDate" content="(.*?) .*?">',url_data ,re.S)[0].split(' ')[0]
    # print(min_date)
    oid = int(re.findall('"cid":(.*?),"vid":""', url_data, re.S)[0].split(',')[0])
    title = re.findall('<title data-vue-meta="true">(.*?)</title>', url_data, re.S)
    return min_date, oid, title

def time_going(min_date):  # 获取两时间段内的日期
    time_list = []
    now_time = str(datetime.datetime.now()).split(' ')[0]  # 获取当前时间，并对时间进行处理，处理成年——月——日的类型，下面要进行时间数据的整理，和构建网址
    star_time = datetime.datetime.strptime(min_date, '%Y-%m-%d')  # 对开始时间进行处理，注意时间要是str类型，'%Y-%m-%d' 是时间类型， Y是指2022，y是对22
    end_time = datetime.datetime.strptime(now_time, '%Y-%m-%d')  # strptime 是实例化的作用，可以将规定输入的时间(字符串)转化为事件类型，以进行操作
    time_list.append(star_time)
    while star_time <= end_time:
        time_str = star_time.strftime('%Y-%m-%d') #strftime 是把指定的时间(按照指定的格式('%Y-%m-%d'))转化为字符串
        time_list.append(time_str)
        star_time += datetime.timedelta(days=1)  # 对时间进行累加，单位是一天
    return time_list

def get_data_del(time_list):
    time_list1 = time_list[1:]
    # print(time_list1)
    mon_data_list = []
    for data in time_list1:
        mon_data_list.append(data[0:7])  # 这里是只取年月
    mon_data_list_set = set(mon_data_list)  # 去重
    return mon_data_list_set

def xml_del(mon_data_list_set, oid):
    list_all = []
    for data in mon_data_list_set:    # 通过年月和oid构建params请求到json数据，内含data所在的月份那一天有数据
        params = {
            'month': f'{data}',
            'type': 1,
            'oid': oid
        }
        data_list_page_js_list = requests.get(url='https://api.bilibili.com/x/v2/dm/history/index',headers=headers ,params=params).json()['data']
        # print(data_list_page_js_list)
        for del_data in data_list_page_js_list:
            params2 = {
                'type': 1,
                'oid': oid,
                'date': del_data
            }
            xml_del_data = requests.get(url='https://api.bilibili.com/x/v2/dm/web/history/seg.so', headers=headers, params=params2).content
            # print(xml_del_data)   #  获取序列化的弹幕数据
            danmaku_seg = Danmaku.DmSegMobileReply()  # Danmaku 是逆序化的相应规则，可以上网查找，本次的规则是在GitHub下载，用cmd封装成了对象
            danmaku_seg.ParseFromString(xml_del_data)
            result = text_format.MessageToString(danmaku_seg, as_utf8=True)  # 以上三步进行对弹幕资源的逆序化
            xml_del = re.findall('content: "(.*?)"', result, re.S)  # 用正则进行对弹幕的提取
            list_all.append({'弹幕内容': xml_del, '日期':del_data})
    return list_all



def main():
    url = input('请输入视频链接:')
    url_date = get_data(url)
    min_date, oid, title = par_data(url_date)
    time_list = time_going(min_date)
    mon_data_list_set = get_data_del(time_list)
    list_all = xml_del(mon_data_list_set, oid)
    # pprint.pprint(list_all)
    return list_all, title


def save_data():
    list_all, title= main()
    with open(f'{title}.txt', mode='a', encoding='utf-8') as f:
        for del_data in list_all:
            xml_data_list = del_data['弹幕内容']
            xml_time = del_data['日期']
            f.write(xml_time + '\n')
            for xml in xml_data_list:
                f.write(xml + '\n')

save_data()  # 注意请求次数过多可能会遭到反扒
# main()






