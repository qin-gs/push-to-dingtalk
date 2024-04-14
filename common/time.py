from datetime import datetime

import pytz


# 定义一个函数获取数据当前时间和ISO 8601时间
def get_current_time() -> tuple[str, str]:
    # 获取当前时间
    current_time = datetime.now()

    # 设置时区为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    beijing_time = current_time.astimezone(beijing_tz)

    # 获取 YYYYMMDD 格式的日期
    date_format = beijing_time.strftime('%Y%m%d')

    # 获取ISO 8601格式的时间
    iso_format = beijing_time.strftime('%Y-%m-%dT%H:%M:%S%z')

    return date_format, iso_format

