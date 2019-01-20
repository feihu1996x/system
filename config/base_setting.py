# -*- coding: utf-8 -*-

# 统一url前缀
URL_PREFIX = ""
# URL_PREFIX = "/system"

# 开发服务器配置
SERVER_PORT = 8088
DEBUG = True
# DEBUG = False

# sqlalchemy配置
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://test:*3!0CcEf@127.0.0.1:3306/system?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"

# 消息状态字典
MESSAGE_STATUS_MAPPING = {
    0: "待跟进",
    -1: "已忽略",
    1: "已跟进"
}
