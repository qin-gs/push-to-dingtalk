from typing import List, Dict, Any

from pymongo import MongoClient

from config import get_value_from_yaml_or_env


def insert_to_mongo(collection_name: str, data: List[Dict]) -> None:
    """
    连接到 MongoDB，选择指定数据库和集合，并插入数据。

    Parameters:
        collection_name (str): 要使用的集合名称。
        data (dict): 要插入的数据。

    Returns:
        None
    """
    # 连接到 MongoDB
    client = MongoClient(get_value_from_yaml_or_env("mongo.host"), int(get_value_from_yaml_or_env("mongo.port")))

    # 选择要使用的数据库（如果不存在，将自动创建）
    db = client[get_value_from_yaml_or_env("mongo.db_name")]

    # 获取一个集合
    collection = db[collection_name]

    # 插入数据
    result = collection.insert_many(data)

    print(f"插入 {len(result.inserted_ids)} 行")


def delete_from_mongo(collection_name: str, date: str) -> None:
    """
    连接到 MongoDB，选择指定数据库和集合，并删除指定日期的数据。

    Parameters:
        collection_name (str): 要使用的集合名称。
        date (str): 要删除的日期字符串，格式为'yyyymmdd'。

    Returns:
        None
    """
    # 连接到 MongoDB
    client = MongoClient(get_value_from_yaml_or_env("mongo.host"), int(get_value_from_yaml_or_env("mongo.port")))

    # 选择要使用的数据库（如果不存在，将自动创建）
    db = client[get_value_from_yaml_or_env("mongo.db_name")]

    # 获取指定的集合
    collection = db[collection_name]

    # 删除指定日期的数据
    result = collection.delete_many({"date": date})

    print(f"删除 {result.deleted_count} 行")


def get_data_from_mongo(collection_name: str, date: str) -> List[Dict[str, Any]]:
    """
    从 MongoDB 中获取指定日期的数据。

    参数:
    date (str): 指定日期。

    返回:
    List[Dict[str, Any]]: 查询到的数据列表。
    """
    # 连接到 MongoDB
    client = MongoClient(get_value_from_yaml_or_env("mongo.host"), int(get_value_from_yaml_or_env("mongo.port")))

    # 选择要使用的数据库（如果不存在，将自动创建）
    db = client[get_value_from_yaml_or_env("mongo.db_name")]

    # 获取指定的集合
    collection = db[collection_name]

    # 查询数据
    query = {"date": date}
    results = collection.find(query)

    # 将结果转换为列表并返回
    data = []
    for result in results:
        data.append(result)

    return data


# 使用示例

if __name__ == "__main__":
    # 使用示例
    # data = [
    #     {"name": "John", "age": 23, "date": "20240412"},
    #     {"name": "Alice", "age": 25, "date": "20240413"},
    #     {"name": "Bob", "age": 35, "date": "20240414"}
    # ]
    # insert_to_mongo("test", data)
    #
    # delete_from_mongo("test", "20240414")

    date = "20240601"
    data = get_data_from_mongo('xwlb', date)
    for item in data:
        print(item)
