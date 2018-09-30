#!/usr/bin/python3

"""
@file: MessagesService.py
@brief: QQ群消息公共服务类
@author: feihu1996.cn
@date: 18-09-19
@version: 1.0
"""  

import re

from sqlalchemy import or_

from application import app, db
from common.libs.Helper import get_current_date, md5_hash
from common.models.messages.FirstFilterKeys import FirstFilterKey
from common.models.messages.Messages import Message
from common.models.messages.OriginalMessages import OriginalMessage
from common.models.messages.QqGroup import QqGroup
from common.models.messages.SecondFilterGroupnumber import \
    SecondFilterGroupnumber
from common.models.messages.SecondFilterQqnumber import SecondFilterQqnumber


class MessagesService:
    """
    QQ群消息公共服务类
    """
    @staticmethod
    def save_export_group_msgs( msgs=None ):
        """
        将导出的QQ群消息保存到数据库(original_messages表)
        """
        app.logger.info( "executing %s.MessagesService.save_export_group_msgs" % ( __name__ ) )
        if msgs: # msgs不为空的情况下再继续
            # 匹配所有QQ群的模式
            group_pattren = re.compile( "消息分组:我的QQ群(.*?)\\r\\n\\r\\n================================================================", re.S )

            # 匹配QQ群名称的模式（在当前QQ群范围内）
            group_name_pattern = re.compile( "消息对象:(.*?)\\r\\n", re.S )

            # 匹配所有消息块的模式（在当前QQ群范围内）
            msssage_block_pattern = re.compile( "\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}.*?\(\d{1,}\)\r\n.*?\r\n", re.S )

            # 匹配消息发布时间的模式（在当前消息块范围内）
            send_time_pattern = re.compile( "\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}" )

            # 匹配用户昵称的模式（在当前消息块范围内）
            sender_name_pattern = re.compile( "\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2} (.*?)\(\d{1,}\)" )

            # 匹配QQ号的模式（在当前消息块范围内）
            qq_number_pattern = re.compile( "\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}.*?\((\d{1,})\)" )

            # 匹配消息内容的模式（在当前消息块范围内）
            content_pattern = re.compile( "\d{4}-\d{2}-\d{2} \d{1,2}:\d{2}:\d{2}.*?\(\d{1,}\)\r\n(.*?)\r\n" )

            # 所有QQ群
            all_groups = group_pattren.findall( msgs )

            app.logger.info( "当前QQ群个数为" + str( len( all_groups ) ) )

            for group in all_groups:  # 遍历QQ群列表，单独处理每个QQ群的消息
                # QQ群名称
                group_name = group_name_pattern.findall( group )[0] if group_name_pattern.findall( group ) else ""
                app.logger.info( "group_name=" + group_name )

                if group_name:  # QQ群名称不为空的情况下再继续
                    # 填充（QQ群表），QQ号码后续再处理
                    qq_group_model = QqGroup.query.filter_by( group_name=group_name ).first()
                    if not qq_group_model:  # 匹配当前QQ群名称的记录
                        app.logger.info( "当前QQ群记录不存在..." )
                        qq_group_model = QqGroup()
                        qq_group_model.group_name = group_name
                        db.session.add( qq_group_model )
                        db.session.commit()

                # 当前QQ群中的所有消息块
                all_message_blocks = msssage_block_pattern.findall( group )
                app.logger.info( "当前QQ群消息块的个数为:" + str( len( all_message_blocks ) ) )

                for message_block in all_message_blocks:  # 遍历消息块列表，单独处理每个消息块
                    send_time = send_time_pattern.findall( message_block )[0] if send_time_pattern.findall( message_block ) else '暂时没有匹配到'
                    app.logger.info( "send_time=" + send_time )

                    sender_name = sender_name_pattern.findall( message_block )[0] if sender_name_pattern.findall( message_block ) else "暂时没有匹配到"
                    app.logger.info( "sender_name=" + sender_name )

                    qq_number = qq_number_pattern.findall( message_block )[0] if qq_number_pattern.findall( message_block ) else "暂时没有匹配到"
                    app.logger.info( "qq_number=" + qq_number )

                    content = content_pattern.findall( message_block )[0] if content_pattern.findall( message_block ) else "暂时没有匹配到"
                    app.logger.info( "content=" + content )

                    fingerprint = md5_hash( send_time + sender_name + qq_number + content )
                    app.logger.info( "fingerprint=" + fingerprint )

                    original_message_model = OriginalMessage.query.filter_by( fingerprint=fingerprint ).first()
                    if not original_message_model:  # 当前消息的指纹不存在时，才执行插入操作，从而实现增量插入
                        app.logger.info( "正在将消息入库..." )
                        original_message_model = OriginalMessage()
                        original_message_model.group_id = qq_group_model.id
                        original_message_model.sender_name = sender_name
                        original_message_model.qq_number = qq_number
                        original_message_model.content = content
                        original_message_model.send_time = send_time
                        original_message_model.fingerprint = fingerprint
                        db.session.add( original_message_model )
                        db.session.commit()

        app.logger.info( "finished %s.MessagesService.save_export_group_msgs" % ( __name__ ) )

    @staticmethod
    def filter_by_keys():
        """
        根据给定关键词，
        过滤原始消息记录表，
        只保留消息内容包含该关键词的消息记录，
        保存到messages表
        """
        app.logger.info( "executing %s.MessagesService.filter_by_keys" % ( __name__ ) )

        key_list = [ model.key_name for model in FirstFilterKey.query.all()]

        app.logger.info( "当前关键词参数列表的长度为:" + str( len( key_list ) ) )

        if key_list:
            filter_rule = or_( *[ OriginalMessage.content.ilike("%{0}%".format( key )) for key in key_list ] )
            original_message_model_list = OriginalMessage.query.filter( filter_rule ).all()
            for original_message_model in original_message_model_list:
                send_time = str( original_message_model.send_time )
                app.logger.info( "send_time=" + send_time )

                sender_name = original_message_model.sender_name
                app.logger.info( "sender_name=" + sender_name )

                qq_number = original_message_model.qq_number
                app.logger.info( "qq_number=" + qq_number )

                content = original_message_model.content
                app.logger.info( "content=" + content )

                fingerprint = md5_hash( send_time + sender_name + qq_number + content )
                app.logger.info( "fingerprint=" + fingerprint )

                message_model = Message.query.filter_by( fingerprint=fingerprint ).first()
                if not message_model:
                    app.logger.info( "消息正在入库..." )
                    message_model = Message()
                    message_model.group_id = original_message_model.group_id
                    message_model.sender_name = sender_name
                    message_model.qq_number = qq_number
                    message_model.content = content
                    message_model.send_time = send_time
                    message_model.fingerprint = fingerprint
                    db.session.add( message_model )
                    db.session.commit()
                
        app.logger.info( "finished %s.MessagesService.filter_by_keys" % ( __name__ ) )

    @staticmethod
    def filter_by_numbers():
        """
        根据给定的QQ/微信群号码或者QQ/微信号，
        过滤消息记录表，
        将QQ/微信群或者QQ/微信对应的消息记录删除
        """
        app.logger.info( "executing %s.MessagesService.filter_by_numbers" % ( __name__ ) )

        group_number_list = [ model.group_number for model in SecondFilterGroupnumber.query.all() ]
        group_id_list = [ model.id for model in [ QqGroup.query.filter_by( group_number=group_number ).first() for group_number in group_number_list ] if model ]
        app.logger.info( "过滤QQ群号码列表长度=" + str( len( group_id_list ) ) )

        qq_number_list = [ model.qq_number for model in SecondFilterQqnumber.query.all() ]
        app.logger.info( "过滤QQ号码列表长度=" + str( len( qq_number_list ) ) )

        if not group_id_list and not qq_number_list:
            app.logger.info( "过滤条件为空，不进行过滤" )
            app.logger.info( "finished %s.MessagesService.filter_by_numbers" % ( __name__ ) )
            return

        filter_rule = or_( *( [ Message.group_id == group_id for group_id in group_id_list ] + [ Message.qq_number == qq_number for qq_number in qq_number_list ] ) )
        message_model_list = Message.query.filter( filter_rule ).all()
        if message_model_list:
            app.logger.info( "正在删除消息记录..." )
            [ db.session.delete( message_model ) for message_model in message_model_list ]
            db.session.commit()

        app.logger.info( "finished %s.MessagesService.filter_by_numbers" % ( __name__ ) )

    @staticmethod
    def update_messages():
        """
        根据过滤关键字和过滤QQ/微信群、QQ/微信号码，
        过滤消息记录表
        """
        app.logger.info( "executing %s.MessagesService.update_messages" % ( __name__ ) )

        # 旧的消息记录集合
        old_message_model_list = set( Message.query.all() )

        key_list = [ model.key_name for model in FirstFilterKey.query.all()]
        filter_rule = or_( *[ Message.content.ilike("%{0}%".format( key )) for key in key_list ] )
        # 新的消息记录集合
        message_model_list = set( Message.query.filter( filter_rule ).all() )

        # 需要根据关键词过滤掉的消息记录集合 = 旧的消息记录集合 - 新的消息记录集合
        filtered_message_model_list = list( old_message_model_list - message_model_list )

        # 删除需要根据关键词过滤掉的消息记录
        [ db.session.delete( model ) for model in filtered_message_model_list ]
        db.session.commit()
        
        # 根据QQ群号码或者QQ号过滤消息记录
        MessagesService.filter_by_numbers()

        app.logger.info( "finished %s.MessagesService.update_messages" % ( __name__ ) )

    @staticmethod
    def save_wechat_group( group_name=None, group_number=None ):
        """
        微信群入库
        """
        app.logger.info( "executing %s.MessagesService.save_wechat_group" % ( __name__ ) )
        
        if group_name:
            group_name += "(微信群)"
            qq_group_model = QqGroup.query.filter_by( group_name=group_name ).first()
            if not qq_group_model:
                app.logger.info( '新的微信群正在入库...' )
                qq_group_model = QqGroup()
                qq_group_model.group_name = group_name    
                if group_number:
                    qq_group_model.group_number = group_number
                db.session.add( qq_group_model )
                db.session.commit()

        app.logger.info( "finished %s.MessagesService.save_wechat_group" % ( __name__ ) )

    @staticmethod
    def save_wechat_group_msg( **kwargs ):
        """
        微信群消息入库
        """
        app.logger.info( "executing %s.MessagesService.save_wechat_group_msg" % ( __name__ ) )

        group_name = kwargs.get( 'group_name', None )  # 群聊名称
        group_number = kwargs.get( 'group_number', None )  # 群聊号码
        sender_name = kwargs.get( 'sender_name', None )  # 用户昵称
        content = kwargs.get( 'content', None )  # 消息内容
        send_time = kwargs.get( 'send_time', None )  # 消息发布时间
        qq_number = kwargs.get( 'qq_number', None )  # 微信号

        if group_name:
            group_name += "(微信群)"
            qq_group_model = QqGroup.query.filter_by( group_name=group_name ).first()
            if not qq_group_model:
                app.logger.info( '新的微信群正在入库...' )
                qq_group_model = QqGroup()
                qq_group_model.group_name = group_name    
                if group_number:
                    qq_group_model.group_number = group_number
                db.session.add( qq_group_model )
                db.session.commit()        

            if sender_name and content:
                fingerprint = md5_hash( sender_name + content )  # 计算当前消息的指纹
                app.logger.info( '当前群消息的指纹是:%s' %( fingerprint ) )
                original_message_model = OriginalMessage.query.filter_by( fingerprint=fingerprint ).first()
                if not original_message_model:
                    app.logger.info( '新的群消息正在入库...' )
                    original_message_model = OriginalMessage()
                    original_message_model.group_id = qq_group_model.id
                    original_message_model.sender_name = sender_name
                    original_message_model.qq_number = qq_number if qq_number else '微信号暂无'
                    original_message_model.content = content
                    original_message_model.send_time = send_time if send_time else get_current_date()
                    original_message_model.fingerprint = fingerprint
                    db.session.add( original_message_model )
                    db.session.commit()

        app.logger.info( "finished %s.MessagesService.save_wechat_group_msg" % ( __name__ ) )
