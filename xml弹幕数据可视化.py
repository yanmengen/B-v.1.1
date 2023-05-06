from main_b import ch_name
from main_b import get_data
from main_b import xml
from main_b import parse_data
from main_b import down_data
import re


def main_xml(url):
    url_date = get_data(url)
    max_num = int(input('请输入所需要的前几个弹幕(请输入数字，如数字不够所输入数字将全部输出):'))
    name1 = re.findall('<title data-vue-meta="true">(.*?)</title>', url_date, re.S)[0]
    name = ch_name(name1)
    xml(max_num, url_date, name)


def main_down(url):
    url_date = get_data(url)
    audio_url, Video_url, name = parse_data(url_date)
    down_data(url)

def max_both(url):
    url_date = get_data(url)
    max_num = int(input('请输入所需要的前几个弹幕(请输入数字，如数字不够所输入数字将全部输出):'))
    name1 = re.findall('<title data-vue-meta="true">(.*?)</title>', url_date, re.S)[0]
    name = ch_name(name1)
    audio_url, Video_url, name = parse_data(url_date)
    down_data(audio_url, Video_url, name)
    xml(max_num, url_date, name)
    # url_date = get_data(url)

def menu():
    i = int(input('输入1分析弹幕;输入2下载视频;输入3两者都需要:'))
    url = input('请输入对应视频链接:')
    if i == 1:
        main_xml(url)
    elif i == 2:
        main_down(url)
    elif i == 3:
        main_xml(url)
        main_down(url)

menu()