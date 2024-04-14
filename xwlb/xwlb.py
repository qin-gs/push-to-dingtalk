import json
import re
from typing import List, Dict

import datetime
import pytz
import requests
from lxml import etree

from common.config import get_value_from_yaml
from common.push import Messenger
from mongo.mongo import insert_to_mongo, delete_from_mongo
from parse_html import parse_html
from common.time import get_current_time


def get_sections(date: str) -> List[Dict[str, str]]:
    # 访问主站
    xwlb_url = get_value_from_yaml("xwlb.day_url").format(date)
    html = parse_html(xwlb_url)

    # 构建XPath表达式并计算 <div> 下的 <li> 元素数量，统计有多少个子章节。
    count_xpath = 'count(//html/body/li)'
    count = int(html.xpath(count_xpath))

    # 存储获取到的信息 (链接、标题、主要内容)
    # [{id: 1, url: '', title: '', content: ''}]
    sections = []

    # 循环获取每个视频的链接，第 1 个是全部内容，从第 2 个开始才是每一段具体信息
    for i in range(2, count + 1):
        # 获取图片
        image_xpath = '//html/body/li[{}]/div/a/img/@src'.format(i)
        image_url = 'http:' + html.xpath(image_xpath)[0]

        # 循环访问每个节视频的链接,获取信息
        section_xpath = '//html/body/li[{}]/a/@href'.format(i)
        section_url = html.xpath(section_xpath)[0]
        sub_html = parse_html(section_url)
        # 简介(摘要)
        abstracts_xpath = '//*[@id="page_body"]/div[1]/div[2]/div[2]/div[2]/div/ul/li[1]/p/text()'
        abstracts = sub_html.xpath(abstracts_xpath)
        # 主要内容
        content_xpath = '//*[@id="content_area"]//text()'
        content = sub_html.xpath(content_xpath)
        # 根据 pid 获取内容 tag
        pattern = r'var guid = "(.*?)";'
        match = re.search(pattern, etree.tostring(sub_html, encoding="unicode"))

        tags = ''
        if match:
            pid = match.group(1)
            # 根据 pid 获取内容 tag
            pid_text = requests.get(get_value_from_yaml("xwlb.tag_url").format(pid)).text
            tags = json.loads(pid_text)['tag']

        sections.append({
            "id": i - 1,
            "date": date,
            "image_url": image_url,
            "tags": tags,
            "abstract": ''.join(abstracts),
            "content": ''.join(content),
            "video_url": section_url
        })
    return sections


def push_to_dingtalk(sections: List[Dict[str, str]]) -> None:
    section_format = '[{}. 摘要：{}]([完整版视频链接]({}))![图片]({})'
    all_text = []
    for section in sections:
        all_text.append(section_format.format(section["id"],
                                              section["abstract"],
                                              section["video_url"],
                                              section["image_url"]))

    text = '\n'.join(all_text)
    m = Messenger()
    m.send_md(title, text)


def write_to_file(sections: List[Dict[str, str]]) -> None:
    file_name = "./content/" + title + "共{}条".format(len(sections)) + ".json"
    with open(file_name, "w") as f:
        f.write(json.dumps(sections, indent=4, ensure_ascii=False))


def write_to_mongo(sections: List[Dict[str, str]]) -> None:
    insert_to_mongo("xwlb", sections)


# 调用函数获取当前时间
date, iso_time = get_current_time()
# 推送标题
title = date + "新闻联播"

if __name__ == '__main__':
    sections = get_sections(date)
    write_to_file(sections)
    delete_from_mongo('xwlb', date)
    write_to_mongo(sections)
