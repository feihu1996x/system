#!/usr/bin/python3

"""
@file: MessagesService.py
@brief: QQ群消息公共服务类
@author: feihu1996.cn
@date: 18-09-19
@version: 1.0
"""  

import re

from application import app, db
from common.libs.Helper import md5_hash
from common.models.messages.OriginalMessages import OriginalMessage
from common.models.messages.QqGroup import QqGroup


class MessagesService:
    """
    QQ群消息公共服务类
    """
    @staticmethod
    def save_export_group_msgs( msgs=None ):
        """
        将导出的QQ群消息保存到数据库
        """
        app.logger.info( "executing %s.MessagesService.save_export_group_msgs" % ( __name__ ) )
        if msgs: # msgs不为空的情况下再继续
            # 匹配所有QQ群的模式
            group_pattren = re.compile( "消息分组:我的QQ群(.*?)\\r\\n\\r\\n================================================================", re.S )

            # 匹配QQ群名称的模式（在当前QQ群范围内）
            group_name_pattern = re.compile( "消息对象:(.*?)\\r\\n", re.S )

            # 匹配所有发言时间的模式（在当前QQ群范围内）
            send_time_pattern = re.compile( "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}" )

            # 匹配所有发言人昵称的模式（在当前QQ群范围内）
            sender_name_pattern = re.compile( '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (.*?)\(\d{1,}\)' )

            # 匹配所有QQ号的模式（在当前QQ群范围内）
            qq_number_pattern = re.compile( '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} .*?(\d{1,})' )

            # 匹配所有消息内容的模式（在当前QQ群范围内）
            content_pattern = re.compile( '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} .*?\(\d{1,}\)[\r\n]*(.*?)\\r\\n[\r\n]*', re.S )

            # 所有QQ群
            all_groups = group_pattren.findall( msgs )

            print( len( all_groups ) )

            for group in all_groups:  # 遍历QQ群列表，单独处理每个QQ群的消息
                # QQ群名称
                group_name = group_name_pattern.findall( group )[0] if group_name_pattern.findall( group ) else ""
                app.logger.info( "group_name:" + group_name )

                if group_name:  # QQ群名称不为空的情况下再继续
                    # 填充（QQ群表），QQ号码后续再处理
                    qq_group_model = QqGroup.query.filter_by( group_name=group_name ).first()
                    if not qq_group_model:  # 匹配当前QQ群名称的记录
                        app.logger.info( "当前QQ群记录不存在..." )
                        qq_group_model = QqGroup()
                        qq_group_model.group_name = group_name
                        try:
                            db.session.add( qq_group_model )
                            db.session.commit()
                        except:
                            import traceback
                            traceback.print_exc()
                            db.session.rollback()
                
                # 当前QQ群所有发言时间
                all_send_times = send_time_pattern.findall( group )
                
                # 当前QQ群所有发言人昵称
                all_sender_names = sender_name_pattern.findall( group )

                # 当前QQ群所有QQ号
                all_qq_numbers = qq_number_pattern.findall( group )

                # 当前QQ群所有消息内容
                # TODO: content_pattern有些特殊情况匹配不到
                all_contents = content_pattern.findall( group )

                for i in range( 0, len( all_send_times ) ):  # 处理QQ群的每条消息
                    # 消息发布时间
                    send_time = all_send_times[i]
                    app.logger.info( "send_time:" + send_time )    

                    # 用户昵称
                    sender_name = all_sender_names[i]
                    app.logger.info( "sender_name:" + sender_name )

                    # QQ号
                    qq_number = all_qq_numbers[i]
                    app.logger.info( "qq_number:" + qq_number )

                    # 消息内容
                    content = all_contents[i]
                    app.logger.info( "content:" + content )

                    # 指纹
                    fingerprint = md5_hash( send_time + sender_name + qq_number + content )
                    app.logger.info( "fingerprint:" + fingerprint )

                    # 填充原始消息记录表
                    original_message_model = OriginalMessage.query.filter_by( fingerprint=fingerprint ).first()
                    if not original_message_model:  # 指纹不一致的情况下才写入消息
                        app.logger.info( "当前消息不存在..." )
                        original_message_model = OriginalMessage()
                        original_message_model.group_id = qq_group_model.id
                        original_message_model.sender_name = sender_name
                        original_message_model.qq_number = qq_number
                        original_message_model.content = content
                        original_message_model.send_time = send_time
                        original_message_model.fingerprint = fingerprint

                        try:
                            db.session.add( original_message_model )
                            db.session.commit()
                        except:
                            import traceback
                            traceback.print_exc()
                            db.session.rollback()


        app.logger.info( "finished %s.MessagesService.save_export_group_msgs" % ( __name__ ) )
