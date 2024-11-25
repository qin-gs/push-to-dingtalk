from typing import List, Dict, Any

import logging
import mysql.connector

from config import get_value_from_yaml_or_env

log = logging.getLogger(__name__)

"""
    这个文件不能命名为 mysql, 不然会冲突
"""


def get_mysql_config() -> Dict[str, str]:
    return {
        "database": get_value_from_yaml_or_env("mysql.db_name"),
        "username": get_value_from_yaml_or_env("mysql.username"),
        "password": get_value_from_yaml_or_env("mysql.password"),
        "host": get_value_from_yaml_or_env("mysql.host"),
        "port": get_value_from_yaml_or_env("mysql.port")
    }


def insert_to_mysql(table_name: str,
                    records: List[Dict[str, str]],
                    conn_params: Dict[str, str] = None
                    ) -> None:
    """
    插入多条记录到 MySql 数据库中的指定表格。

    参数:
        conn_params (Dict[str, str]): 包含连接信息的字典，例如：
            {
                "dbname": "testdb",
                "user": "username",
                "password": "password",
                "host": "localhost",
                "port": "5432"
            }
        table_name (str): 数据表名。
        records (List[Dict[str, str]]): 要插入的数据列表，每个元素是一个字典，其中字典的键为列名，值为相应的数据（已转为字符串格式）。

    返回:
        None
    """

    # 验证参数
    if conn_params is None:
        log.info("未传入参数，使用配置文件默认值")
        conn_params = get_mysql_config()
    if len(records) == 0:
        log.info("没有要插入的记录")
        return

    # 获取列名和对应的值
    columns = records[0].keys()
    values = [tuple(record[col] for col in columns) for record in records]

    # 动态生成 SQL 语句
    placeholders = ", ".join(["%s"] * len(columns))
    columns_str = ", ".join(columns)
    insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

    connection = None
    cursor = None
    try:
        # 连接数据库
        connection = mysql.connector.connect(**conn_params)
        cursor = connection.cursor()

        # 批量插入数据
        cursor.executemany(insert_query, values)
        connection.commit()

        log.info(f"成功插入 {cursor.rowcount} 条记录到表 {table_name}")

    except mysql.connector.Error as err:
        log.info(f"数据库操作失败，回滚: {err}")
        connection.rollback()

    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()


def delete_from_mysql(table_name: str,
                      target_date: str,
                      conn_params: Dict[str, str] = None) -> None:
    """
    删除指定表中 date 字段等于给定日期的记录。

    参数:
        conn_params (dict): 数据库连接参数，例如：
            {
                "dbname": "testdb",
                "user": "username",
                "password": "password",
                "host": "localhost",
                "port": "5432"
            }
        table_name (str): 要操作的表名。
        target_date (str): 目标日期字符串，格式应与表中 date 字段的格式相匹配。

    返回:
        None
    """

    # 验证参数
    if conn_params is None:
        conn_params = get_mysql_config()

    # 构造删除 SQL 查询
    delete_query = f"DELETE FROM {table_name} WHERE date = %s"
    connection = None
    cursor = None

    try:
        # 连接数据库

        connection = mysql.connector.connect(**conn_params)
        cursor = connection.cursor()

        # 执行删除操作
        cursor.execute(delete_query, (target_date,))
        connection.commit()

        log.info(f"成功删除 {cursor.rowcount} 条记录，从表 {table_name} 中")

    except mysql.connector.Error as err:
        log.info(f"数据库操作失败: {err}")
        connection.rollback()

    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()


def get_data_from_MySql(table_name: str,
                        date: str,
                        conn_params: Dict[str, str] = None) -> List[Dict[str, Any]]:
    """
    从 MySql 数据库中获取指定日期的数据。

    参数:
    date (str): 指定日期。

    返回:
    List[Dict[str, Any]]: 查询到的数据列表。
    """
    # 连接到 MySql 数据库
    # 验证参数
    if conn_params is None:
        conn_params = get_mysql_config()

    # 构造查询语句
    select_query = f"SELECT * FROM {table_name} WHERE date = %s order by id desc"
    connection = None
    cursor = None

    try:
        # 连接数据库
        connection = mysql.connector.connect(**conn_params)
        cursor = connection.cursor(dictionary=True)  # 返回字典格式的结果

        # 执行查询
        cursor.execute(select_query, (date,))
        result = cursor.fetchall()

        log.info(f"成功查询到 {len(result)} 条记录，从表 {table_name} 中")

        return result

    except mysql.connector.Error as err:
        log.info(f"数据库操作失败: {err}")
        return []

    finally:
        # 关闭连接
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()


# 使用示例
if __name__ == '__main__':
    # records = [
    #     {
    #         "id": 1,
    #         "date": "20240000",
    #         "image_url": "http://p1.img.cctvpic.com/photoAlbum/vms/standard/img/2024/4/14/VIDErVuY9y1cdNxz1rXTTedY240414.jmysql",
    #         "tags": "总体国家安全观 意识形态",
    #         "abstract": "【新思想引领新征程】坚持总体国家安全观，筑牢国家安全屏障。",
    #         "content": "央视网消息（新闻联播）：国家安全是安邦定国的重要基石，维护国家安全是全国各族人民根本利益所在。2014年4月15日，习近平总书记在中央国家安全委员会第一次会议上，创造性提出总体国家安全观，为做好新时代国家安全工作提供了根本遵循和行动指南。十年来，在总体国家安全观指引下，国家安全得到全面加强，经受住了来自政治、经济、意识形态、自然界等方面的风险挑战考验，为党和国家兴旺发达、长治久安，人民安居乐业提供了有力保证。日前，国家安全机关破获一起境外企业非法搜集窃取我国战略资源稀土领域国家秘密的案件，涉案人员被依法采取强制措施。近年来，类似这样危害国家安全的案件在我国经济、文化、科技、网络、粮食、生态、资源等领域时有发生，警示着当前我们所面临的国家安全问题的复杂程度、艰巨程度明显加大。党的十八大以来，以习近平同志为核心的党中央加强国家安全战略谋划和顶层设计，建立集中统一、高效权威的国家安全领导体制，设立中央国家安全委员会，习近平总书记亲自担任主席，推动国家安全工作实现从分散到集中、迟缓到高效、被动到主动的历史性变革。党的十九大将坚持总体国家安全观纳入新时代坚持和发展中国特色社会主义的基本方略，并写入党章。总体国家安全观关键在“总体”，强调“大安全”理念，涵盖政治、军事、国土、经济、粮食、文化、科技、网络、人工智能等诸多领域，而且随着社会发展不断动态调整。进入新时代，以习近平同志为核心的党中央坚定不移贯彻总体国家安全观，把维护国家安全贯穿党和国家工作各方面全过程，坚定维护政权安全、制度安全、意识形态安全，严密防范和严厉打击敌对势力渗透、破坏、颠覆、分裂活动，顶住和反击外部极端打压遏制，开展涉港、涉台、涉疆、涉藏、涉海等斗争，打赢多场硬仗，有效维护国家安全。今年3月19日，香港特区立法会全票通过《维护国家安全条例》，为香港实现由治及兴提供坚实支撑，翻开了“一国两制”事业新篇章。强国必须强军，军强才能国安。我们党鲜明提出党在新时代的强军目标，明确人民军队新时代使命任务，引领全军深入推进政治建军、改革强军、科技强军、人才强军、依法治军，全面加强练兵备战，国防和军队建设取得历史性伟大成就。金融安全是经济平稳健康发展的重要基础，我国坚持金融为实体经济服务，全面加强金融监管，防范化解经济金融领域风险，牢牢守住不发生系统性风险底线。无农不稳，无粮则乱。我国全面实施新一轮千亿斤粮食产能提升行动，扎实推进藏粮于地、藏粮于技，谋划实施高标准农田建设、种业振兴等支撑性重大工程，牢牢把握粮食安全主动权。能源攸关国计民生和国家安全。我国实施能源安全新战略，推动能源消费革命、能源供给革命、能源技术革命、能源体制革命，全方位加强能源国际合作，我国从能源大国向能源强国不断迈进。国家安全是民族复兴的根基，社会稳定是国家强盛的前提。党的二十大报告对“推进国家安全体系和能力现代化，坚决维护国家安全和社会稳定”作出战略部署。习近平总书记在二十届中央国家安全委员会第一次会议上强调，要全面贯彻党的二十大精神，深刻认识国家安全面临的复杂严峻形势，正确把握重大国家安全问题，加快推进国家安全体系和能力现代化，以新安全格局保障新发展格局，努力开创国家安全工作新局面。",
    #         "video_url": "https://tv.cctv.com/2024/04/14/VIDECU6q2ymvAv1P5aqgSIDj240414.shtml"
    #     },
    #     {
    #         "id": 2,
    #         "date": "20240000",
    #         "image_url": "http://p3.img.cctvpic.com/photoAlbum/vms/standard/img/2024/4/14/VIDEWZIqRtwx5D6hrSrKxhC8240414.jmysql",
    #         "tags": "科技创新 深海开发",
    #         "abstract": "科技创新引领深海开发新突破。",
    #         "content": "央视网消息（新闻联播）：今年以来，我国加大深海领域科研攻坚，深海装备技术不断升级，涌现出一批具有国际先进水平的深海装备，为深远海开发提供了有力保障。在深圳西南方海域约200公里处，我国自主设计实施的海上第一深井日前正式投产。测试日产原油超过700吨，这口井深度9508米，与垂直井有所不同，它的垂直深度不到2000米，但在海底地下的水平方向钻进长度达到8689米。就在这几天，在青岛，亚洲首艘圆筒型“海上油气加工厂”正在进行入海前的最后调试。5月初，它将被运送至珠江口盆地进行海上安装，为今后我国深海油气资源经济高效开发提供全新模式。近年来，我国启动实施了国家重点研发计划深海关键技术与装备重点专项，海洋科技瞄准深海的战略方向，一大批关键核心技术取得新突破。以“深海勇士”号等潜水器为代表的海洋探测运载作业技术实现质的飞跃。自主建造具有世界先进水平的“雪龙2”号破冰船，填补我国在极地科考重大装备领域的空白。目前，全国有超过40所高校开展与深海技术相关的教学与科研，构建起深海领域“洞—池—湖—海”试验体系。此外，国家启动了大科学工程，汇集各学科、各领域、各层次科技资源，建造海底科学观测网，多项海洋装备也将在今年加速升级换代，为下一步深海开发奠定了基础。",
    #         "video_url": "https://tv.cctv.com/2024/04/14/VIDEYi1R2znDNTCiDsMVFo7y240414.shtml"
    #     }
    # ]
    #
    # delete_from_mysql("xwlb", "20240000")
    # insert_to_mysql('xwlb', records)

    date = "20240601"
    data = get_data_from_MySql('tbl_xwlb', date, get_mysql_config())
    for item in data:
        print(item)
