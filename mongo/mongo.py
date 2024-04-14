from typing import List, Dict

from pymongo import MongoClient

from config import get_value_from_yaml


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
    client = MongoClient(get_value_from_yaml("mongo.host"), int(get_value_from_yaml("mongo.port")))

    # 选择要使用的数据库（如果不存在，将自动创建）
    db = client[get_value_from_yaml("mongo.db_name")]

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
    client = MongoClient(get_value_from_yaml("mongo.host"), int(get_value_from_yaml("mongo.port")))

    # 选择要使用的数据库（如果不存在，将自动创建）
    db = client[get_value_from_yaml("mongo.db_name")]

    # 获取指定的集合
    collection = db[collection_name]

    # 删除指定日期的数据
    result = collection.delete_many({"date": date})

    print(f"删除 {result.deleted_count} 行")


# 使用示例

if __name__ == "__main__":
    # 使用示例
    data = [
        {"name": "John", "age": 23, "date": "20240412"},
        {"name": "Alice", "age": 25, "date": "20240413"},
        {"name": "Bob", "age": 35, "date": "20240414"}
    ]
    insert_to_mongo("test", data)

    delete_from_mongo("test", "20240414")
