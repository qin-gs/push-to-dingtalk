import base64
import hashlib
import hmac
import json
import time
from urllib.parse import quote_plus

import requests

from common.config import get_value_from_yaml_or_env


# 推送消息到钉钉

class Messenger:

    def __init__(self, token=None, secret=None):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = get_value_from_yaml_or_env("dingtalk.send_url")
        self.headers = {'Content-Type': 'application/json'}
        self.token = token or get_value_from_yaml_or_env("dingtalk.access_token")
        self.secret = secret or get_value_from_yaml_or_env("dingtalk.secret")
        self.sign = self.generate_sign()
        self.params = {'access_token': self.token, 'sign': self.sign}

    def generate_sign(self):
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        return quote_plus(base64.b64encode(hmac_code))

    # 发送消息
    def send_md(self, title, text):
        data = {
            'msgtype': 'markdown',
            'markdown': {
                'title': title,
                'text': text
            }
        }
        self.params['timestamp'] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )


if __name__ == '__main__':
    m = Messenger()
    m.send_md("标题", '内容')
