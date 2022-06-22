import json
import requests
import pandas as pd
from psycopg2 import connect
from sqlalchemy import create_engine


cleanup = (
        'DROP TABLE IF EXISTS system_table CASCADE',
        'DROP TABLE IF EXISTS data_table',
        'DROP TABLE IF EXISTS post'
        )

commands =(
        """
        CREATE TABLE system_table (
            userid SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            address VARCHAR(255)
        )
        """
        ,
        """ 
        CREATE TABLE post (
                post_id SERIAL PRIMARY KEY,
                author_id INTEGER NOT NULL,
                created TIMESTAMP DEFAULT NOW(),
                title VARCHAR(350) NOT NULL,
                body VARCHAR(500) NOT NULL,
                FOREIGN KEY (author_id)
                    REFERENCES system_table (userid)
        )
        """
        )

sqlCommands = (
        'INSERT INTO system_table (username, password, address) VALUES (%s, %s, %s) RETURNING userid',
        'INSERT INTO post (title, body, author_id) VALUES (%s, %s, %s)'
        )

conn = connect("dbname=waste user=postgres password=ALJANA")
cur = conn.cursor()
for command in cleanup :
    cur.execute(command)
for command in commands :
    cur.execute(command)
    print('execute command')

cur.execute(sqlCommands[0], ('Rida', 'ALJANA','sudan'))
userId = cur.fetchone()[0]
cur.execute(sqlCommands[1], ('post', 'hello', userId))
cur.execute('SELECT * FROM post')
print(cur.fetchall())


cur.close()
conn.commit()
conn.close()





response = requests.get('https://five.epicollect.net/api/export/entries/solid-waste-management-amc?per_page200')
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

engine = create_engine('postgresql://postgres:ALJANA@localhost:5432/waste')
data_df.to_sql('data_table', engine, if_exists = 'replace', index=False)