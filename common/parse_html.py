import requests
from lxml import etree


def parse_html(url: str):
    # 发起网站请求
    response = requests.get(url)

    # 设置编码方式为 UTF-8
    response.encoding = 'utf-8'

    # 解析返回的 HTML 数据
    return etree.HTML(response.text)
