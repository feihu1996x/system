#!/usr/bin/env python3

"""
@file: server.py
@brief: 启动生产服务器
@author: feihu1996.cn
@date: 18-09-23
@version: 1.0
"""

import os
import re
import sys

work_dir = os.getcwd()

# 启动web app
print("启动web app...")
gun_file = open("gun.conf", "rb")
temps = []
for line in gun_file.readlines():
    if "chdir" not in line.decode("utf8"):
        temps.append(line)
gun_file.close()
gun_file = open("gun.conf", "wb")
gun_file.writelines(temps)
gun_file.close()
os.system(r"""
echo chdir = \'{work_dir}\' >> gun.conf
""".format(work_dir=work_dir))
os.system(r"""
gunicorn -k gevent -c gun.conf manager:app
""")
