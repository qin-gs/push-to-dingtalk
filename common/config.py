import yaml

"""
    读取 yaml 格式的配置文件，根据 key 获取值
"""

# 默认的配置文件名
config_file_name: str = "../config/config.yaml"


def get_value_from_yaml(props: str, file_path: str = config_file_name) -> str:
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
        config = yaml.load(f, Loader=yaml.FullLoader)

    # 使用点号分割字符串来得到键列表
    keys = props.split(".")

    # 逐级获取值
    value = config
    for key in keys:
        value = value[key]

    return value


if __name__ == "__main__":
    print(get_value_from_yaml("jrsf.day_url"))
