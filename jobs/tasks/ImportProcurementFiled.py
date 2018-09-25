#!/usr/bin/python3

"""
@file: ImportProcurementFiled.py
@brief: 数据库初始化：插入采购领域及其对应的关键词
@author: feihu1996.cn
@date: 18-09-25
@version: 1.0
"""
import time

from application import app, db
from common.models.procurement.ProcurementFiled import ProcurementFiled
from common.models.procurement.ProcurementFiledKey import ProcurementFiledKey


class JobTask():
    """
    python manager.py runjob -m ImportProcurementFiled
    数据库初始化：插入采购领域及其对应的关键词
    """
    def __init__(self):  
        self.target = {
            "ARVR": [
                "VR",
                "虚拟现实",
                "虚拟",
                "航拍",
                "全景",
                "摄影",
                "实景",
                "漫游",
                "无人机",
                "公关传媒",
                "媒体公关",
                "活动策划",
                "公关营销",
                "3D",
                "模型",
                "建模",
                "CG",
                "Maya",
                "3dMax",
                "动画",
                "美术",
                "大空间行走",
                "行为捕捉",
                "动作捕捉",
                "体感互动",
                "Kinect",
                "U3D",
                "Unity",
                "UE4",
                "虚幻引擎",
                "增强",
                "增强现实",
                "AR",
                "OpenCV",
                "SLAM",
                "ARKit",
                "ARCore",
                "Metaio美桃",
                "vision based",
                "Vuforia",
                "EasyAR",
                "ARToolKit",
                "QQ AR",
                "Wikitude",
                "HiAR",
                "VoidAR",
                "MR",
                "混合现实",
                "全息",
                "投影",
                "HTC Vive",
                "Oculus Rift",
                "Gear",
                "PSVR",
                "体验店",
                "体验馆",
                "DK2",
                "大朋",
                "Matterport",
                "Hololens",
                "联想MR",
                "Magic leap",
                "Google Glass"
            ],
            "人工智能": [
                "人工智能",
                "智能",
                "AI",
                "机器视觉",
                "语音识别",
                "深度学习",
                "神经网络",
                "自然语音处理",
                "智慧旅游",
                "智能音箱",
                "TensorFlow",
                "PaddlePaddle",
                "智慧城市",
                "特色小镇",
                "物联网",
                "IOT",
                "智能家居",
                "智慧家居",
                "智能家电",
                "工业制造",
                "工业4.0",
                "智能制造",
                "智慧教育",
                "智慧金融",
                "新能源",
                "能源矿产",
                "智能汽车",
                "无人驾驶",
                "无人车",
                "新零售",
                "智能营销"
            ],
            "智能医疗": [
                "可穿戴设备",
                "虚拟助手",
                "智能医疗",
                "智慧医疗",
                "智能健康",
                "医学影像",
                "智能医疗",
                "智能血糖仪",
                "智能血压计",
                "智能心电仪",
                "智能温度计",
                "智能秤",
                "智能按摩器",
                "智能手表",
                "智能手环"
            ],
            "机器人": [
                "机器人",
                "工业机器人",
                "服务机器人",
                "教育机器人",
                "水下机器人",
                "建筑机器人",
                "安全营救机器人",
                "消防机器人",
                "工业自动化",
                "发那科"
            ],
            "3D打印": [
                "3D打印"
            ]
        }

    def run(self, params):
        app.logger.info( 'executing %s' % ( __name__ ) )
        
        for field_name,field_key_list in self.target.items():
            procurement_filed_model = ProcurementFiled.query.filter_by( filed_name=field_name ).first()
            if not procurement_filed_model:
                app.logger.info( "正在插入新的采购领域" )
                procurement_filed_model = ProcurementFiled()
                procurement_filed_model.filed_name = field_name
                db.session.add( procurement_filed_model )
                db.session.commit()
            for key_name in field_key_list:
                procurement_filed_key_model = ProcurementFiledKey.query.filter_by( key_name=key_name ).first()
                if not procurement_filed_key_model:
                    app.logger.info( "正在插入新的%s采购领域关键词" % field_name )
                    procurement_filed_key_model = ProcurementFiledKey()
                    procurement_filed_key_model.field_id = procurement_filed_model.id
                    procurement_filed_key_model.key_name = key_name
                    db.session.add( procurement_filed_key_model )
                    db.session.commit()

        app.logger.info( "finished %s" % ( __name__ ) )
