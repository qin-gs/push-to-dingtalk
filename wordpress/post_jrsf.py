from datetime import datetime, timedelta
from io import BytesIO

import pytz
import requests
import json
from base64 import b64encode
from PIL import Image

from config import get_value_from_yaml_or_env
from mySql.mySql import get_data_from_MySql

username = get_value_from_yaml_or_env("wordpress.username")
password = get_value_from_yaml_or_env("wordpress.password")
auth_header = {
    'Authorization': 'Basic {}'.format(b64encode('{}:{}'.format(username, password).encode('utf-8')).decode('utf-8'))}


def add_posts_to_wordpress():
    url = get_value_from_yaml_or_env('wordpress.posts')
    data = get_data_from_MySql('tbl_jrsf', '20241125')
    date = datetime.now(pytz.timezone('UTC')).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    for item in data:
        # 首先上传一幅图片
        image_url: str = item['image_url']
        media_id = upload_image_to_wordpress(image_url)

        post = {
            'title': item['title'],
            'status': 'publish',
            'content': item['content'] + "<a target=\"_blank\" href='" + item['video_url'] + "'>参考链接</a>",
            'categories': 7,
            'date': date,
            "featured_media": media_id,
        }
        response = requests.post(url, headers=auth_header, json=post)
        print(response.text)


def upload_image_to_wordpress(image_url: str):
    """
        上传图片到 WordPress 并返回 media_id

        参数:
            image_url (str): 图片的 URL
            wordpress_site_url (str): WordPress 网站的 URL
            username (str): 用户名
            password (str): 应用密码

        返回:
            int: 上传图片的 media_id
    """
    # 获取图片数据
    response = requests.get(image_url)
    if response.status_code != 200:
        raise Exception("无法下载图片")

    # image_data = BytesIO(response.content)
    img = Image.open(BytesIO(response.content))
    buffer = BytesIO()
    img.save(buffer, format=img.format)
    buffer.seek(0)

    image_name = image_url.split("/")[-1]

    # WordPress 媒体 API URL
    media_url = get_value_from_yaml_or_env("wordpress.media")

    # 请求头
    headers = {
        "Content-Disposition": f"attachment; filename={image_name}",
        "Content-Type": "image/jpg",
        **auth_header
    }

    # 发送 POST 请求上传图片
    response = requests.post(media_url,
                             headers=headers,
                             data=buffer)

    if response.status_code not in [200, 201]:
        raise Exception(f"上传图片失败: {response.status_code}, {response.text}")

    media_id = response.json().get("id")
    print(f'media_id: {media_id}')
    return media_id


if __name__ == '__main__':
    add_posts_to_wordpress()
    # upload_image_to_wordpress('')
