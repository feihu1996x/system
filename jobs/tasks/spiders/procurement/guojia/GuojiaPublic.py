#!/usr/bin/python3

"""
@file: GuojiaPublic.py
@brief: 中国政府采购网 公开招标 项目信息爬取
@author: feihu1996.cn
@date: 18-09-17
@version: 1.0
"""

import time
import traceback
import urllib

from lxml import etree
from selenium import webdriver

from application import app, db
from common.libs.procurement.ProcurementService import ProcurementService
from common.models.procurement.ProcurementField import ProcurementField
from common.models.procurement.ProcurementFieldKey import ProcurementFieldKey


class JobTask():
    """
    python manager.py runjob -m spiders/procurement/guojia/GuojiaPublic
    中国政府采购网 公开招标 项目信息爬取
    """
    def __init__(self):  
        app.config.from_pyfile( 'config/procurement_guojia_public_setting.py' )
        self.interval = app.config['INTERVAL']
        self.entry_url_template = "http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=&buyerName=&projectId=&pinMu=&bidType=1&dbselect=bidx&kw={key_name}&start_time=2018%3A09%3A18&end_time=2018%3A09%3A25&timeType=2&displayZone=&zoneId=&pppStatus=0&agentName="
        self.project_url_xpath = '//ul[@class="vT-srch-result-list-bid"]/li/a/@href'  # 匹配项目url的XPATH表达式
        self.next_page_btn_xpath = '//p[@class="pager"]/a[@class="next"]'  # 匹配下一页按钮的XPATH表达式
        self.project_content_xpath = '//div[@class="vF_detail_main"]'  # 匹配项目内容的XPATH表达式

    def run ( self, params ):
        """
        运行任务
        """
        if self.interval: 
            app.logger.info( "定时器已开启，频率是%s秒..." %( str( self.interval ) ) ) 
            self.timer_task() 
        else:
            app.logger.info( "定时器未开启" )
            self.task()

    def timer_task( self ):
        """
        定时执行task
        """
        while True:
            self.task()
            time.sleep( self.interval )

    def task( self ):
        """
        爬取中国政府采购网公开招标项目信息
        """
        app.logger.info( "launching %s ..." % ( __name__ ) )
        browser = webdriver.Chrome()  # 打开浏览器

        procurement_field_model_list = ProcurementField.query.all()  # 采购领域model列表
        for procurement_field_model in procurement_field_model_list:  # 遍历采购领域model列表
            field = procurement_field_model.field_name  # 当前采购领域
            app.logger.info( "当前采购领域:%s" % field )
            procurement_field_key_model_list = ProcurementFieldKey.query.filter_by( field_id=procurement_field_model.id ).all()  # 当前采购领域关键词列表
            for procurement_field_key_model in procurement_field_key_model_list:  # 遍历当前采购领域关键词列表
                key_name = procurement_field_key_model.key_name  # 当前关键字
                app.logger.info( "当前关键词:%s" % key_name )
                target_url = self.entry_url_template.format( key_name=urllib.parse.quote( key_name ) )   # 使用关键字拼接当前目标url
                app.logger.info( "当前目标url：%s" % target_url ) 
                browser.get( target_url )  # 访问目标url
                i = 0
                while True:  # 自动翻页解析，若没有下一页，则退出循环
                    data = browser.page_source
                    treedata = etree.HTML(data)
                    app.logger.info( "正在处理第%d页" % (i+1) )
                    try:
                        project_url_list = treedata.xpath( self.project_url_xpath )  # 当前页面所有项目url列表
                        app.logger.info( "当前页共发现%d条项目信息" % len( project_url_list ) )
                        for project_url in project_url_list:  # 遍历项目url列表
                            try:
                                child_browser = webdriver.Chrome()  # 打开一个新的浏览器
                                child_browser.get( project_url )  # 访问当前项目url  
                                app.logger.info( "当前项目url:%s" % project_url )
                                project_data = child_browser.page_source
                                project_treedata = etree.HTML( project_data )
                                app.logger.info( "当前项目页面大小：%d" % len( project_data ) )
                                project_content_treedata = project_treedata.xpath( self.project_content_xpath )
                                if project_content_treedata:
                                    project_content_treedata = project_content_treedata[0]
                                    ProcurementService.process_project_content( project_content_treedata=project_content_treedata, project_url=project_url, field=field )
                                child_browser.quit()  # 关闭浏览器   
                            except:
                                traceback.print_exc()
                            # break # TODO                         
                    except:
                        traceback.print_exc()
                    finally:
                        if not treedata.xpath( self.next_page_btn_xpath ):  # 如果是最后一页,则退出循环
                            app.logger.info( "当前已经是最后一页" )
                            break
                        browser.find_element_by_xpath( self.next_page_btn_xpath ).click()  # 跳转到下一页
                        time.sleep(1)  # 翻页后等待1秒，等待页面数据加载完全                            
                        i += 1                
                    # break # TODO
                # break # TODO
            # break # TODO

        browser.quit() # 关闭浏览器
        app.logger.info( "finished %s" % ( __name__ ) )
