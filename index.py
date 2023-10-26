import configparser
from utils.helper import create_bucket
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
config = configparser.ConfigParser()
import logging
import redshift_connector

from sql_statement.create import dev_tables 
from sql_statement.transform import transformed_tables
from sql_statement.transform import transformation_queries



config .read('.env')

access_key = config['AWS']['access_key']
secret_key = config['AWS']['access_key'] 
bucket_name = config['AWS']['bucket_name']
region = config['AWS']['bucket_name']

db_host= config['DB_CONN']['db_host']
db_user = config['DB_CONN']['db_user'] 
db_database = config['DB_CONN']['db_database']
db_password = config['DB_CONN']['db_password']



dwh_host= config['DWH_CONN']['dwh_host']
dwh_user = config['DWH_CONN']['dwh_user'] 
dwh_database = config['DWH_CONN']['dwh_database']
dwh_password = config['DWH_CONN']['dwh_password']



#--- 1 create S3 bucket (Data lake)

create_bucket(access_key, secret_key,bucket_name, region)



# ---2Extract  data from postgresql  Data lake 

conn = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}r@{db_host}:5432/{db_database}')

db_tables = ['dev_call_log', 'dev_callclean_details']



for table in db_tables:
    query = f'SELECT * FROM {table}'
    logging.info(f'======================EXecuting{query}')
    df = pd.read_sql_query(query, conn)
    
    df.to_csv(
      f' s3//:{bucket_name}/{table}.csv'  
        , index=False
        ,storage_options={
            'key':access_key
        ,'secret':secret_key
        }
    )
    
    
    
    # ---step 3 load intial schema
    
    dwh_conn = redshift_connector.connect(
    host=dwh_host,
    database=dwh_database ,
    user='user',
    password='dwh_password'
    
 )

print('DWH Connection Established')
cursor = dwh_conn.cursor()

dev_schema ='dev'
staging_schema = 'staging'

 #----Create a dev schema 
     
cursor.execute('''CREATE SCHEMA{dev_schema};''')

dwh_conn.commit()
     
# ---- Create a table 
for query in dev_tables:
    print(f'--------------------{query[:50]}')
    cursor.execute(query)
    dwh_conn.commit()
    
    # -----COPY TABLE FROM S3
    for table in db_tables:
        cursor.execute(f'''
                       
          COPY {dev_schema}.{table}
          FROM
                's3://{bucket_name}/{table}.csv'       
                       
                IAM ROLE '{role}'
                DELIMETER ','
                IGNOREHEADER 1;
                    
''')
        dwh_conn.commit()



     # Step4:Create the fact and dimension   table 
     
     
     
     # ----- create schema
     
    cursor.execute('''CREATE SCHEMA{staging_schema};''')

    dwh_conn.commit()
     
     #-----Create star schema fact and dimension
    for query in transformed_tables:
        print(f'--------------------{query[:50]}')
        cursor.execute(query)
    dwh_conn.commit()
    #  #----- insert data into   facts and dimensions     
           
    for query in transformation_queries:
        print(f'--------------------{query[:50]}')
        cursor.execute()
        dwh_conn.commit()
        