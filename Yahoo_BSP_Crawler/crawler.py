# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import requests
import time
import json
import psycopg2
import pandas as pd
from settings import *
from log import lib_core_log

YahooBSP_log = lib_core_log(name="YahooBSP")

class YahooBestSellProductCrawler(object):

    def __init__(self):
        self.parse_start_url()        
        
    def format_category_information(self, response):
    
        category_ids = response['billboard']['subId'].split(',')        
        category_information = list()
        for tab in response['billboard']['tabs']:
            tab['category_id'] = category_ids[tab['idx']]
            category_information.append(tab)

        for tab in response['billboard']['othertab']:
            tab['category_id'] = category_ids[tab['idx']]
            category_information.append(tab)

        return category_information

    def format_price(self, price):
        
        rst_price = BeautifulSoup(price, features="html.parser").findAll("span",{"class": "shpprice"})[0].string
        return rst_price

    def fetch_bsp_data(self, response, category_information):
        
        bsp_data = list()
        for each_category in category_information:

            # top-1 item
            each_bsp_data = each_category    
            each_bsp_data['pd_descr'] = response['billboard']['panels'][each_category['idx']]['mainitem']['desc']
            each_bsp_data['pd_id'] = response['billboard']['panels'][each_category['idx']]['mainitem']['pdid']            
            each_bsp_data['pd_price'] = self.format_price(response['billboard']['panels'][each_category['idx']]['mainitem']['price'])
            each_bsp_data['rank'] = 1
            bsp_data.append(each_bsp_data.copy())

            # top 2-5 items
            for pditem in response['billboard']['panels'][each_category['idx']]['pditem']:
                each_bsp_data = each_category
                each_bsp_data['pd_descr'] = pditem['desc']
                each_bsp_data['pd_id'] = pditem['pdid']
                each_bsp_data['pd_price'] = self.format_price(pditem['price'])
                each_bsp_data['rank'] = pditem['rank']
                bsp_data.append(each_bsp_data.copy())
                
        return bsp_data

    def export_bsp_to_csv_and_excel(self, bsp_data):
        
        if EXPORT_TO_EXCEL :    
            with pd.ExcelWriter('yahooBSP_excel_output.xlsx') as writer:            
                bsp_data.to_excel(writer,'Sheet1')
                writer.save()
        if EXPORT_TO_CSV:
            export_csv = bsp_data.to_csv("yahooBSP_csv_output.csv",index = None, header=True)

    def parse_start_url(self):

        bsp_data = list()
        for cid in range(0,len(CATEGORY_ID_LIST),10):
            
            target_url = START_URL +','.join(map(str, CATEGORY_ID_LIST[cid:cid+10]))
            
            YahooBSP_log.logger.debug("Processing url %s" % target_url)
        
            response = requests.get(target_url).json()
            
            category_information = self.format_category_information(response)
            
            each_bsp_data = self.fetch_bsp_data(response, category_information)
            
            bsp_data = bsp_data + each_bsp_data
            
        bsp_data = pd.DataFrame(bsp_data)
        YahooBSP_log.logger.debug("number of BSP data : %s" % len(bsp_data.index))
        
        self.export_bsp_to_csv_and_excel(bsp_data)
        
        if DB_ENABLE :
            try:
                db_conn = psycopg2.connect(database=DB_DBNAME, user=DB_USER, password=DB_PWD, host=DB_HOST, port=DB_PORT)
                YahooBSP_log.logger.debug("Connect database succeed")
            except:
                YahooBSP_log.logger.error("Connect database failed")   
            else:
                change_dsp_data= self.fetch_latest_bsp_and_compare(db_conn, bsp_data)
                YahooBSP_log.logger.debug("number of changed BSP data : %s" % len(change_dsp_data.index))
                if len(change_dsp_data.index) :
                    rst = self.write_bsp_change_to_db(db_conn, change_dsp_data)                    
                db_conn.close()          
                
        return bsp_data.to_json(orient='records')

    def fetch_latest_bsp_and_compare(self, db_conn, bsp_data):
        
        latest_bsp_data = pd.read_sql("SELECT * FROM %s" % DB_LATEST_BSP_VIEW_NAME, con=db_conn)
        latest_bsp_data[['category_id', 'pd_id']] = latest_bsp_data[['category_id', 'pd_id']].astype('str')
        
        change_dsp_data = bsp_data.merge(latest_bsp_data,on=['category_id','pd_id','pd_price','rank','pd_descr'],how='left')
        change_dsp_data = change_dsp_data[change_dsp_data.db_insert_time.isnull()]

        return change_dsp_data

    def write_bsp_change_to_db(self, db_conn, change_dsp_data):

        try:
            cur = db_conn.cursor()
            sql_insert_values_list = list()           
            
            for index, row in change_dsp_data.iterrows():                            
                sql_insert_values_list.append("('{}','{}','{}','{}','{}','{}')".format(row['label'],row['category_id'],row['pd_id'],row['pd_descr'],row['pd_price'],row['rank']))            
            cur.execute("INSERT INTO {} (category_name, category_id, pd_id, pd_descr, pd_price, rank) VALUES {} ".format( DB_CRAWLED_DATA_TBL_NAME, ','.join(map(str, sql_insert_values_list))))
            db_conn.commit()
            YahooBSP_log.logger.debug("Write to DB succeed")
        except Exception as e:            
            YahooBSP_log.logger.error("Write to DB failed : " % str(e))
            return False

        return True

if __name__ == '__main__':
    
    c = YahooBestSellProductCrawler()


