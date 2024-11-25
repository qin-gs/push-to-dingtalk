import logging
import os
import re

import yaml

"""
    读取 yaml 格式的配置文件，根据 key 获取值
    参考: https://www.cnblogs.com/superhin/p/16104767.html
"""

log = logging.getLogger(__name__)

# 默认的配置文件名
config_file_name: str = "../config/config.yaml"
# 前后可以拥有多个任意字符，使用小括号分组只取当前变量${变量名}内容，`?`表示非贪婪匹配。
pattern = re.compile('.*?(\${\w+}).*?')


def env_var_constructor(loader, node):
    value = loader.construct_scalar(node)
    # 遍历所有匹配到到${变量名}的变量, 如${USER}
    for item in pattern.findall(value):
        # 如 USER
        var_name = item.strip('${} ')
        # 用环境变量中取到的对应值替换当前变量
        value = value.replace(item, os.getenv(var_name, item))
        # 如 qgs 替换${USER}，取不到则使用原值${USER}

    return value


# 添加新tag即对应的构造器
yaml.SafeLoader.add_constructor('!env', env_var_constructor)
# 为tag指定一种正则匹配
yaml.SafeLoader.add_implicit_resolver('!env', pattern, None)




def get_value_from_yaml_or_env(props: str, file_path: str = config_file_name) -> str:
    """
    Get the value from YAML file based on the provided keys.

    Parameters:
        props (str): The keys to navigate through the YAML structure.
        file_path (str): The path to the YAML file.

    Returns:
        The value corresponding to the provided keys.
    """
    # 读取 YAML 文件
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)

    # 使用点号分割字符串来得到键列表
    keys = props.split(".")

    # 逐级获取值
    value = config
    for key in keys:
        value = value[key]

    if value is not None:
        return value
    else:
        os.getenv(props, None)


if __name__ == "__main__":
    print(get_value_from_yaml_or_env("wordpress.username"))
    # with open(config_file_name) as f:
    #     print(yaml.safe_load(f))
