# -*- coding: utf-8 -*-

# Scrapy settings for banana project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'banana (+http://www.yourdomain.com)'


LOG_LEVEL = "DEBUG"
DB_ENABLE = True
DB_HOST = 'target-postgresql-instance-dms-demo.cdquinixcuuq.us-west-2.rds.amazonaws.com'
DB_PORT = "5432"
DB_DBNAME = "crawler_database"
DB_USER = "crawler_ap_user"
DB_PWD = "app123"
DB_CRAWLED_DATA_TBL_NAME = "crawler_data_bt"
DB_LATEST_BSP_VIEW_NAME = "latest_bsp_summary_v"

CATEGORY_ID_LIST = [1,2,4,5,8,9,10,12,19,22,23,24,26,27,28,30,31,34,35,37,38,41,51,54,56,57,68,70,83,90,97,103,104,107,110,114,120,202,215,286,408,430,436,454,457,459,461,462,463,464,470,478,481,517,518,521,536,583,612,613]
START_URL = "https://tw.buy.yahoo.com/catalog/ajax/recmdHotNew?segmentId=999999&subId="


