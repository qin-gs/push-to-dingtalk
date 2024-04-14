
import json
from typing import List, Dict

import requests
from lxml import etree
from config import get_value_from_yaml
from mongo.mongo import insert_to_mongo, delete_from_mongo
from parse_html import parse_html
from common.time import get_current_time


def get_content(date: str) -> Dict:
    jrsf_url = get_value_from_yaml("jdft.day_url").format(1, 1)
    jrsf_text = etree.tostring(parse_html(jrsf_url), encoding="utf-8")

    # 提取 Callback 中的内容
    start_index = jrsf_text.find(b'lanmu_0(') + len(b'lanmu_0(')
    end_index = jrsf_text.rfind(b');')
    callback_content = jrsf_text[start_index:end_index]

    # 转换为字典
    text_dict = json.loads(callback_content)['data']['list'][0]

    pid = text_dict['guid']
    tag_text = requests.get(get_value_from_yaml("jdft.tag_url").format(pid))
    tags = json.loads(tag_text.text, )['tag']

    content = {
        "date": date,
        "title": text_dict['title'],
        "image_url": text_dict['image'],
        "content": text_dict['brief'],
        "video_url": text_dict['url'],
        "guid": text_dict['guid'],
        "tags": tags
    }

    return content


def write_to_file(content: Dict[str, str]) -> None:
    file_name = "./content/" + title + ".json"
    with open(file_name, "w") as f:
        f.write(json.dumps(content, indent=4, ensure_ascii=False))


def write_to_mongo(content: Dict[str, str]) -> None:
    insert_to_mongo("jdft", [content])


# 调用函数获取当前时间
date, iso_time = get_current_time()
# 推送标题
title = date + "焦点访谈"

if __name__ == '__main__':
    content = get_content(date)
    print(content)
    write_to_file(content)

    delete_from_mongo("jdft", date)
    write_to_mongo(content)
