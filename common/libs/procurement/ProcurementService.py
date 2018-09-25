#!/usr/bin/python3

"""
@file: ProcurementService.py
@brief: 采购项目信息爬虫公共服务类
@author: feihu1996.cn
@date: 18-09-25
@version: 1.0
"""  

from application import app, db
from common.libs.Helper import clean_string, md5_hash
from common.models.procurement.Procurement import Procurement


class ProcurementService:
    """
    采购项目信息爬虫公共服务类
    """
    @staticmethod
    def process_project_content( project_content_treedata=None, project_url=None, field=None ):
        """
        处理项目信息内容
        """
        app.logger.info( "executing %s.ProcurementService.process_project_content" % ( __name__ ) )

        if project_content_treedata and project_url and field:
            # 项目标题
            name_xpath = 'div[@class="vF_detail_header"]/h2[@class="tc"]/descendant-or-self::*/text()'
            name = clean_string( ''.join( project_content_treedata.xpath( name_xpath ) ) )
            app.logger.info( "项目名称：%s" % name )

            # 项目描述
            desc_xpath = '//div[@class="vF_detail_content"]/descendant-or-self::*/text()'
            desc = clean_string( ''.join( project_content_treedata.xpath( desc_xpath ) ) )
            app.logger.info( "项目描述：%s" % desc )

            if name and desc:
                # 项目指纹
                fingerprint = md5_hash( name + project_url + field )

                procurement_model = Procurement.query.filter_by( fingerprint=fingerprint ).first()
                if not procurement_model:  # 项目指纹不一致时才插入数据
                    app.logger.info( "正在插入新的采购项目：%s" % name )
                    procurement_model = Procurement()
                    procurement_model.fingerprint = fingerprint
                    procurement_model.name = name
                    procurement_model.field = field
                    procurement_model.desc = desc
                    procurement_model.source = project_url
                    db.session.add( procurement_model )
                    db.session.commit()                

        app.logger.info( "finished %s.ProcurementService.process_project_content" % ( __name__ ) )
