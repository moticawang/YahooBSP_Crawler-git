# YahooBSP_Crawler-git


##### 執行範例
`cd YahooBSP_Crawler`

`python crawler.py`

##### 輸出
CSV
EXCEL

##### Query interface for crawled data
你可使用psql或是pgAdmin tool連線到PostgreSQL database來下SQL query
AWS RDS-PostgreSQL instance
DB_HOST = 'target-postgresql-instance-dms-demo.cdquinixcuuq.us-west-2.rds.amazonaws.com'
DB_PORT = "5432"
DB_DBNAME = "crawler_database"
DB_USER = "viewer"
DB_PWD = "viewer123"

取得yahoo BSP資訊
`SELECT * FROM latest_bsp_summary_v`

##### settings.py 參數設定說明
