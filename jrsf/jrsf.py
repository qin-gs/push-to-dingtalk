import json
from typing import List, Dict

import requests
from lxml import etree
from config import get_value_from_yaml_or_env
from mongo.mongo import insert_to_mongo, delete_from_mongo
from mySql.mySql import delete_from_mysql, insert_to_mysql
from parse_html import parse_html
from common.time import get_current_time, get_yesterday_time
from pg.pg import delete_from_pg, insert_to_pg


def get_content(date: str) -> Dict:
    jrsf_url = get_value_from_yaml_or_env("jrsf.day_url").format(1, 1)
    jrsf_text = etree.tostring(parse_html(jrsf_url), encoding="utf-8")

    # 提取 Callback 中的内容
    start_index = jrsf_text.find(b'Callback(') + len(b'Callback(')
    end_index = jrsf_text.rfind(b');')
    callback_content = jrsf_text[start_index:end_index]

    # 转换为字典
    text_dict = json.loads(callback_content)['data']['list'][0]

    pid = text_dict['guid']
    tag_text = requests.get(get_value_from_yaml_or_env("jrsf.tag_url").format(pid))
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
    insert_to_mongo("jrsf", [content])


# 调用函数获取当前时间
date, iso_time = get_current_time()
# date, iso_time = get_yesterday_time()
# 推送标题
title = date + "今日说法"

if __name__ == '__main__':
    content = get_content(date)
    # write_to_file(content)

    # delete_from_mongo("tbl_jrsf", date)
    # write_to_mongo(content)

    # delete_from_pg("tbl_jrsf", date)
    # insert_to_pg("tbl_jrsf", [content])

    delete_from_mysql("tbl_jrsf", date)
    insert_to_mysql("tbl_jrsf", [content])
