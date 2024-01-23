import os
import sys
import argparse
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import sessionmaker

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db

    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    meta_data = MetaData()
    
    folder_split = sys.path[0].split('\\')[0:-1]
    base_folder = '\\'.join(folder_split)
    data_folder = os.path.join(base_folder,'data')

    # Dropping Old Tables
    for item in ['games','players','season_averages','teams']:
        try:
            table = Table(item, meta_data, autoload_with=engine)
            table.drop(engine)
            print(f'Dropped: {item}')
        except NoSuchTableError:
            print(f'{item} - Table Does Not Exist')

    # Ingesting New Tables From Scratch
    for filename in os.listdir(data_folder):
        print(f'Ingesting: {filename}')
        table_name = filename.split('.')[0]
        df = pd.read_json(os.path.join(data_folder,filename))
        if filename.split('.')[0] == 'players':
            df = df[['id','first_name','last_name','position']]
        df.to_sql(name=table_name, con=engine, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest JSON data into Postgres')
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db for postgres')
    
    args = parser.parse_args()
    main(args)