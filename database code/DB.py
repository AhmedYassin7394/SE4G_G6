from psycopg2 import connect
import json
import requests
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine


cleanup = (
        'DROP TABLE IF EXISTS system_table CASCADE',
        'DROP TABLE IF EXISTS comments_table',
        'DROP TABLE IF EXISTS data_table'
        )

commands =(
        """
        CREATE TABLE system_table (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(255)
            
        )
        """
        ,
        """
        CREATE TABLE comments_table (
            comment_id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created TIMESTAMP DEFAULT NOW(),
                title VARCHAR(350) NOT NULL,
                body VARCHAR(500) NOT NULL,
                FOREIGN KEY (user_id)
                    REFERENCES system_table (user_id)
        )
        """
        )

sqlCommands = (
        'INSERT INTO system_table (username, password, email) VALUES (%s, %s, %s) RETURNING user_id',
        'INSERT INTO comments_table (title, body, user_id) VALUES (%s, %s, %s)'
        )        
conn = connect("dbname=postgres user=postgres password=amay123")
cur = conn.cursor()
for command in cleanup :
    cur.execute(command)
for command in commands :
    cur.execute(command)
    print('execute command')
cur.execute(sqlCommands[0], ('boss', 'amay123','ahmedyassin7394@gmail.com'))
userId = cur.fetchone()[0]
cur.execute(sqlCommands[1], ('comment', 'hello', userId))
cur.execute('SELECT * FROM comments_table')
print(cur.fetchall())

cur.close()
conn.commit()
conn.close()

response = requests.get('https://five.epicollect.net/api/export/entries/solid-waste-management-amc')
raw_data = response.text
data   = json.loads(raw_data)
data_df = pd.json_normalize(data['data']['entries'])

data_df['id'] = data_df['title']
data_df['longintude'] = pd.to_numeric(data_df['4_Location_of_the_is.longitude'], errors='coerce')
data_df['latitude'] = pd.to_numeric(data_df['4_Location_of_the_is.latitude'], errors='coerce')
data_df['created time'] = data_df['created_at']


data_df['Remarks'] = data_df['5_Special_Remarks']
data_df['Type'] = data_df['3_Type']

data_df['Number'] = data_df['2_Part_Number']
data_df = data_df.loc[:,'id':'Number']

engine = create_engine('postgresql://postgres:amay123@localhost:5432/postgres')
data_df.to_sql('data_table', engine, if_exists = 'replace', index=False)
