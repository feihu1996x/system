#!/usr/bin/python3

"""
@file: ImportFilterKeys.py
@brief: 将一次过滤关键词导入数据库
@author: feihu1996.cn
@date: 18-09-20
@version: 1.0
"""

from application import app, db
from common.models.messages.FirstFilterKeys import FirstFilterKey


class JobTask():
    """
    python manager.py runjob -m ImportFilterKeys
    将一次过滤关键词导入数据库
    """
    def __init__(self):  
        self.key_list = [
            '谁家有',
            '谁那有',
            '谁有',
            '谁家',
            '谁在',
            '谁会',
            '哪位',
            '哪家',
            '哪位',
            '哪里有',
            '那家',
            '那个',
            '有谁',
            '有人',
            '有的',
            '有做',
            '有搞',
            '有能',
            '有在',
            '有没',
            '有卖',
            '有么有',
            '有没有',
            '有没得',
            '有会做',
            '有木有',
            '有现成',
            '有朋友',
            '有出的',
            '有这种',
            '有类似',
            '有可以',
            '能做',
            '能搞',
            '做过',
            '求',
            '求购',
            '买',
            '收',
            '收购',
            '采购',
            '购买',
            '需要',
            '需求',
            '项目',
            '外包',
            '发包',
            '接单',
            '接活',
            '寻找',
            '想找',
            '想寻找',
            '想做',
            '预算',
            '交付',
            '急求',
            '私聊',
            '私信我',
            '联系我',
            '找',
            '怎么收费',
            '请问',
            '群里有',
            '大家有',
            '资源'
        ]

    def run(self, params):
        app.logger.info( 'executing %s' % ( __name__ ) )
        
        for key_name in self.key_list:
            filter_key_model = FirstFilterKey.query.filter_by( key_name=key_name ).first()
            if not filter_key_model:  # 当前关键词记录不存在的情况，才执行插入
                app.logger.info( "正在将关键词%s入库..." % ( key_name ) )
                filter_key_model = FirstFilterKey()
                filter_key_model.key_name = key_name
                db.session.add( filter_key_model )
                db.session.commit()

        app.logger.info( "finished %s" % ( __name__ ) )
