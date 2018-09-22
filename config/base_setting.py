# -*- coding: utf-8 -*-

# 统一url前缀
URL_PREFIX = ""
# URL_PREFIX = "/system"

# 开发服务器配置
SERVER_PORT = 8080
DEBUG = True
# DEBUG = False

# sqlalchemy配置
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://test:*3!0CcEf@127.0.0.1:3306/qq_group_spider?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"

# qq账号配置
QQ_ACCOUNT_LIST = [
    {
        "qq_number": "3027677825",
        "qq_password": "Z3408x143c40823V?"
    }
]

# qq可执行文件路径配置
QQ_PATH = r"C:\Program Files (x86)\Tencent\QQ\Bin\QQ.exe"

# 保存导出消息原始数据文件的默认路径
MSG_PATH = r"C:\Users\GSXxg\Desktop"

# 消息状态字典
MESSAGE_STATUS_MAPPING = {
    0: "待跟进",
    -1: "已忽略",
    1: "已跟进"
}
